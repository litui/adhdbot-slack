"""SQLAlchemy setup

Probably overkill for what we need here, but it's been on the to-learn
list for awhile.
"""

from sqlalchemy import create_engine, orm
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

_Base = declarative_base()
_engine = create_engine('sqlite:///bot.db')
_SM = orm.sessionmaker(bind=_engine, autoflush=True, autocommit=False)
session = _SM()


class Config(_Base):
    __tablename__ = 'config'
    key = Column(String(30), primary_key=True)
    value = Column(String(30), nullable=False)
