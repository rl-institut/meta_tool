
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
    root = relationship("Meta", secondary=f'{SCHEMA}.roots')


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
        nullable=True
    )
    owner = sqla.Column(
        sqla.VARCHAR,
        nullable=True
    )
    parent_id = sqla.Column(
        sqla.Integer, sqla.ForeignKey(f'{SCHEMA}.meta.meta_id'), nullable=True)


class Roots(Base):
    __tablename__ = 'roots'
    __table_args__ = {'schema': SCHEMA}

    run_id = sqla.Column(
        sqla.ForeignKey(f'{SCHEMA}.run.run_id'),
        primary_key=True
    )
    meta_id = sqla.Column(
        sqla.ForeignKey(f'{SCHEMA}.meta.meta_id'),
        primary_key=True
    )
