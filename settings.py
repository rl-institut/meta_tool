
import os
from configobj import ConfigObj
import sqlalchemy
import sqlalchemy_utils
import sqlahelper
import logging

from models import Base


logging.basicConfig(level=logging.INFO)


config = ConfigObj(os.environ['CONFIG_PATH'])
db_url = '{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'


def setup_meta_engine():
    meta_connection = config['DATABASES']['META_CONNECTION']
    meta_url = db_url.format(
        NAME=config['DATABASES']['META_DATABASE'],
        **config['DATABASES'][meta_connection]
    )
    return sqlalchemy.create_engine(meta_url)


def setup_source_engines():
    for source_name, source_data in config['SOURCES'].items():
        if source_data['TYPE'] == 'DB':
            db_connection = config['DATABASES'][source_data['CONNECTION']]
            current_db_url = db_url.format(
                NAME=source_data['DATABASE'],
                **db_connection
            )
            engine = sqlalchemy.create_engine(current_db_url)
            sqlahelper.add_engine(engine, source_name)


def create_db_structure(engine):
    # Init Meta-Database:
    if not sqlalchemy_utils.database_exists(engine.url):
        sqlalchemy_utils.create_database(engine.url)
    Base.metadata.bind = engine
    Base.metadata.create_all()


meta_engine = setup_meta_engine()
create_db_structure(meta_engine)
setup_source_engines()


