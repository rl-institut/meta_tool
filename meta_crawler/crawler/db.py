
import json
import sqlalchemy as sqla
import sqlahelper
import transaction
import logging

from meta_show import settings
from meta_show.models import Meta, Run, Source, Owner, get_or_create


def get_comment_from_db(engine, schema=None, table=None):
    if table is not None:
        sql = (
            'SELECT '
            'obj_description(pg_class.oid) '
            'FROM pg_class '
            'JOIN pg_namespace ON pg_class.relnamespace = pg_namespace.oid '
            'WHERE relname = %(table)s AND nspname = %(schema)s'
        )
    elif schema is not None:
        sql = (
            'SELECT '
            "obj_description(oid) "
            'FROM pg_namespace '
            'WHERE nspname=%(schema)s'
        )

    else:
        # Get json from database:
        sql = (
            'SELECT '
            "shobj_description(oid, 'pg_database') "
            'FROM pg_database '
            'WHERE datname=%(database)s'
        )

    params = {
        'database': engine.url.database,
        'schema': schema,
        'table': table
    }
    return engine.execute(sql, params).next()[0]


def get_owner_from_db(engine, schema=None, table=None):
    if table is not None:
        sql = (
            'SELECT '
            'pg_catalog.pg_get_userbyid(relowner) '
            'FROM pg_catalog.pg_class '
            'JOIN pg_catalog.pg_namespace ON relnamespace = pg_namespace.oid '
            'WHERE nspname = %(schema)s AND relname = %(table)s'
        )
    elif schema is not None:
        sql = (
            'SELECT '
            'pg_catalog.pg_get_userbyid(nspowner) '
            'FROM pg_catalog.pg_namespace '
            'WHERE nspname = %(schema)s'
        )
    else:
        sql = (
            'SELECT '
            'pg_catalog.pg_get_userbyid(d.datdba) '
            'FROM pg_catalog.pg_database d '
            'WHERE d.datname=%(database)s'
        )
    params = {
        'database': engine.url.database,
        'schema': schema,
        'table': table
    }
    return engine.execute(sql, params).next()[0]


def check_json(text):
    if text is None:
        return None
    try:
        js = json.loads(text)
    except ValueError:
        return None
    return js


def get_meta_from_db():
    session = sqlahelper.get_session()
    run = Run()
    session.add(run)

    engines = sqlahelper._engines
    engine_count = len(engines)
    for e, engine_name in enumerate(engines):
        if engine_name in settings.deactivated_sources:
            continue

        logging.info(f'Engine ({e + 1}/{engine_count}): {engine_name}')
        engine = sqlahelper.get_engine(engine_name)
        inspect = sqla.inspect(engine)

        source_info = settings.config['SOURCES'][engine_name]
        info = '{ENGINE}://{HOST}:{PORT}'.format(
            **settings.config['DATABASES'][source_info['CONNECTION']])
        source = Source(
            type=source_info['TYPE'],
            name=engine_name,
            info=info
        )
        run.sources.append(source)
        session.flush()

        owner_name = get_owner_from_db(engine)
        owner = get_or_create(session, Owner, name=owner_name, run=run)
        session.flush()
        comment = get_comment_from_db(engine)
        js = check_json(comment)
        meta_database = Meta(
            location=source_info['DATABASE'],
            json=js,
            owner=owner
        )
        source.root = meta_database
        session.add(meta_database)
        session.flush()

        schemas = [
            schema
            for schema in inspect.get_schema_names()
            if schema not in source_info.get('EXCLUDE_SCHEMAS', [])
        ]
        schema_count = len(schemas)
        for s, schema in enumerate(schemas):
            logging.info(f'- Schema ({s + 1}/{schema_count}): {schema}')

            owner_name = get_owner_from_db(engine, schema)
            owner = get_or_create(session, Owner, name=owner_name, run=run)
            comment = get_comment_from_db(engine, schema)
            js = check_json(comment)
            meta_schema = Meta(
                location=schema,
                parent_id=meta_database.meta_id,
                json=js,
                owner=owner
            )
            session.add(meta_schema)
            session.flush()

            tables = inspect.get_table_names(schema)
            table_count = len(tables)
            for t, table in enumerate(tables):
                logging.info(f'  - Table ({t + 1}/{table_count}): {table}')

                owner_name = get_owner_from_db(engine, schema, table)
                owner = get_or_create(session, Owner, name=owner_name, run=run)
                comment = get_comment_from_db(engine, schema, table)
                js = check_json(comment)
                meta_table = Meta(
                    location=table,
                    parent_id=meta_schema.meta_id,
                    json=js,
                    owner=owner
                )
                session.add(meta_table)
    try:
        transaction.commit()
    except:
        session.rollback()
    finally:
        session.close()


if __name__ == '__main__':
    get_meta_from_db()
