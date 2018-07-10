
import json
import sqlalchemy as sqla
import sqlahelper
import transaction

from settings import meta_engine
from models import Meta, Run


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


def check_json(text):
    # TODO: Check if it is usable json
    if text is None:
        return None
    js = json.dumps(text)
    return js


def get_meta_from_db():
    session = sqlahelper.get_session()
    run = Run()
    session.add(run)

    engines = sqlahelper._engines
    engine_count = len(engines)
    for e, engine_name in enumerate(engines):
        print(f'Engine ({e}/{engine_count}): {engine_name}')
        engine = sqlahelper.get_engine(engine_name)
        inspect = sqla.inspect(engine)

        comment = get_comment_from_db(engine)
        js = check_json(comment)
        meta_database = Meta(location=engine_name)
        run.root.append(meta_database)
        session.add(meta_database)

        schemas = inspect.get_schema_names()
        schema_count = len(schemas)
        for s, schema in enumerate(schemas):
            print(f'- Schema ({s}/{schema_count}): {schema}')

            comment = get_comment_from_db(engine, schema)
            js = check_json(comment)
            meta_schema = Meta(
                location=schema,
                parent_id=meta_database.meta_id
            )
            session.add(meta_schema)

            tables = inspect.get_table_names(schema)
            table_count = len(tables)
            for t, table in enumerate(tables):
                print(f'  - Table ({t}/{table_count}): {table}')
                comment = get_comment_from_db(engine, schema, table)
                meta_table = Meta(
                    location=table,
                    parent_id=meta_schema.meta_id)
                session.add(meta_table)

    transaction.commit()


if __name__ == '__main__':
    get_meta_from_db()
