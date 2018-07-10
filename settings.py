
import os
from configobj import ConfigObj
import sqlalchemy
import sqlalchemy_utils
import sqlahelper

from models import Base


config = ConfigObj(os.environ['CONFIG_PATH'])
db_url = '{ENGINE}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}'
meta_engine = None

# Establish database connections for all sources:
for source_name, source_data in config['SOURCES'].items():
    if source_data['TYPE'] == 'DB':
        db_connection = config['DATABASES'][source_data['CONNECTION']]
        current_db_url = db_url.format(
            NAME=source_data['DATABASE'],
            **db_connection
        )
        if source_name == config['DATABASES']['META_DATABASE']:
            meta_engine = sqlalchemy.create_engine(current_db_url)
        else:
            engine = sqlalchemy.create_engine(current_db_url)
            sqlahelper.add_engine(engine, source_name)

# Init Meta-Database:
if not sqlalchemy_utils.database_exists(meta_engine.url):
    sqlalchemy_utils.create_database(meta_engine.url)
Base.metadata.bind = meta_engine
Base.metadata.create_all()
