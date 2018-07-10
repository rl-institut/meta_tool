
import datetime as dt
import sqlalchemy as sqla
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SCHEMA = 'public'


class Run(Base):
    __tablename__ = 'run'
    __table_args__ = {'schema': SCHEMA}

    run_id = sqla.Column(
        sqla.Integer,
        primary_key=True
    )
    timestamp = sqla.Column(sqla.DateTime, default=dt.datetime.utcnow)
    sources = relationship("Source")


class Source(Base):
    __tablename__ = 'source'
    __table_args__ = {'schema': SCHEMA}

    source_id = sqla.Column(
        sqla.Integer,
        primary_key=True
    )
    name = sqla.Column(
        sqla.VARCHAR,
    )
    run_id = sqla.Column(sqla.Integer, sqla.ForeignKey(f'{SCHEMA}.run.run_id'))
    metas = relationship("Meta")


class Meta(Base):
    __tablename__ = 'meta'
    __table_args__ = {'schema': SCHEMA}

    meta_id = sqla.Column(
        sqla.Integer,
        primary_key=True
    )
    location = sqla.Column(
        sqla.VARCHAR,
    )
    json = sqla.Column(
        sqla.JSON,
    )
    owner = sqla.Column(
        sqla.VARCHAR,
    )
    source_id = sqla.Column(
        sqla.Integer, sqla.ForeignKey(f'{SCHEMA}.source.source_id'))
