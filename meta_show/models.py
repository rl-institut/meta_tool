
import datetime as dt
import sqlalchemy as sqla
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

SCHEMA = 'public'


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()
    if instance:
        return instance
    else:
        instance = model(**kwargs)
        session.add(instance)
        session.flush()
        return instance


class Run(Base):
    __tablename__ = 'run'
    __table_args__ = {'schema': SCHEMA}

    run_id = sqla.Column(
        sqla.Integer,
        primary_key=True
    )
    timestamp = sqla.Column(sqla.DateTime, default=dt.datetime.utcnow)
    sources = relationship("Source", back_populates='run')
    owners = relationship("Owner", back_populates='run')


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
    owner_id = sqla.Column(
        sqla.ForeignKey(f'{SCHEMA}.owner.owner_id')
    )
    owner = relationship("Owner", back_populates="metas")
    parent_id = sqla.Column(
        sqla.Integer, sqla.ForeignKey(f'{SCHEMA}.meta.meta_id'), nullable=True)
    children = relationship('Meta')


class Source(Base):
    __tablename__ = 'source'
    __table_args__ = {'schema': SCHEMA}

    source_id = sqla.Column(
        sqla.Integer,
        primary_key=True
    )
    run_id = sqla.Column(
        sqla.ForeignKey(f'{SCHEMA}.run.run_id')
    )
    run = relationship("Run", back_populates="sources")
    root_id = sqla.Column(sqla.ForeignKey(f'{SCHEMA}.meta.meta_id'))
    root = relationship("Meta", uselist=False)
    type = sqla.Column(sqla.VARCHAR)
    name = sqla.Column(sqla.VARCHAR)
    info = sqla.Column(sqla.VARCHAR, nullable=True)


class Owner(Base):
    __tablename__ = 'owner'
    __table_args__ = {'schema': SCHEMA}

    owner_id = sqla.Column(
        sqla.Integer,
        primary_key=True
    )
    run_id = sqla.Column(sqla.ForeignKey(f'{SCHEMA}.run.run_id'))
    run = relationship("Run", uselist=False, back_populates='owners')
    name = sqla.Column(
        sqla.VARCHAR
    )
    metas = relationship("Meta", back_populates='owner')
