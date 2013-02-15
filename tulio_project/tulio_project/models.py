from pyramid.security import Allow
from pyramid.security import Everyone

from sqlalchemy import (
    Column,
    Integer,
    Text,
    Binary,
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
    print "models"
    __tablename__ = 'models'
    id = Column(Integer, primary_key=True)
    name = Column(Text, unique=True)
    value = Column(Integer)

    def __init__(self, name, value):
        self.name = name
        self.value = value

class UserModel(Base):
    print "UserModel"
    __acl__ = [ (Allow, Everyone, 'view'),
            (Allow, 'group:editors', 'edit') ]
            
    __tablename__ = 'usuarios'
    id = Column(Integer, primary_key=True)
    name = Column(Text,nullable=False)
    login = Column(Text, unique=True,nullable=False)
    senha = Column(Text, nullable=False)

    def __init__(self, name, login, senha):
        self.name = name
        self.login = login
        self.senha = senha

# class ImageModel(Base):
#     print "ImageModel"
#     __tablename__ = 'imagens'
#     id = Column(Integer, primary_key=True)
#     file = Column(Binary, nullable=True)
#     name = Column(Text)

#     def __init__(self, name, file = None):
#         self.name = name
#         self.file = file
