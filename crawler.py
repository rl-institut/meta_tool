
import sqlalchemy as sqla
from settings import meta_engine
import sqlahelper


for engine_name in sqlahelper._engines:
    engine = sqlahelper.get_engine(engine_name)
    inspect = sqla.inspect(engine)
    for schema in inspect.get_schema_names():
        for table in inspect.get_table_names(schema):
            print(table)
