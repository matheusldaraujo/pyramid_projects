from sqlalchemy import (
    Column,
    Integer,
    Text,
    DateTime,
    )

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import (
    scoped_session,
    sessionmaker,
    )

from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class MyModel(Base):
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value

class HitModel(Base):
    __tablename__ = "hit"
    id = Column(Integer,primary_key=True)
    ip = Column(Text,nullable=False)
    date = Column(DateTime,nullable=False)
    userAgent = Column(Text,nullable=True)

    def __init__(self, ip, date, userAgent):
        self.ip = ip
        self.date = date
        self.userAgent = userAgent
