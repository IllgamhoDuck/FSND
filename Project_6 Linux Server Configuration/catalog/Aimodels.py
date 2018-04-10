from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from passlib.apps import custom_app_context as pwd_context

import random
import string

from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import BadSignature, SignatureExpired

Base = declarative_base()
secret_key = ''.join(random.choice(string.ascii_uppercase +
                                   string.digits) for x in range(32))


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(250), index=True, nullable=False)
    email = Column(String(250), nullable=False)
    picture = Column(String)
    password_hash = Column(String(250))
    provider = Column(String(250))
    aicatalog = relationship("AiCatalog", backref="user",
                             cascade="all, delete, delete-orphan")
    aicustom = relationship("AiCustom", backref="user",
                            cascade="all, delete, delete-orphan")
    ai = relationship("Ai", backref="user",
                      cascade="all, delete, delete-orphan")
    aibook = relationship("AiBook", backref="user",
                          cascade="all, delete, delete-orphan")
    ainews = relationship("AiNews", backref="user",
                          cascade="all, delete, delete-orphan")
    aimatch = relationship("AiMatch", backref="user",
                           cascade="all, delete, delete-orphan")

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration):
        s = Serializer(secret_key, expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        print("secret key " + secret_key)
        s = Serializer(secret_key)
        try:
            data = s.loads(token)
        except SignatureExpired:
            # Valid Token, but expired
            return None
        except BadSignature:
            # Invalid Token
            return None
        user_id = data['id']
        return user_id

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
                'name': self.name,
                'email': self.email,
                'picture': self.picture,
                'id': self.id,
                }


class AiCatalog(Base):
    __tablename__ = 'aicatalog'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    description = Column(String(250))
    picture = Column(String(250))
    user_id = Column(Integer, ForeignKey('user.id'))
    aicustom = relationship("AiCustom", backref="aicatalog",
                            cascade="all, delete, delete-orphan")
    ai = relationship("Ai", backref="aicatalog",
                      cascade="all, delete, delete-orphan")
    aibook = relationship("AiBook", backref="aicatalog",
                          cascade="all, delete, delete-orphan")
    ainews = relationship("AiNews", backref="aicatalog",
                          cascade="all, delete, delete-orphan")
    aimatch = relationship("AiMatch", backref="aicatalog",
                           cascade="all, delete, delete-orphan")

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'description': self.description,
            'picture': self.picture,
            'id': self.id,
        }

# User custom made catalog. Has just simple function


class AiCustom(Base):
    __tablename__ = 'aicustom'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    picture = Column(String(250))
    description = Column(String(250))
    aicatalog_id = Column(Integer, ForeignKey('aicatalog.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'picture': self.picture,
            'description': self.description,
            'id': self.id,
        }

# 4 catagory's related to Ai under AiCatalog


class Ai(Base):
    __tablename__ = 'ai'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    picture = Column(String(250))
    description = Column(String(250))
    aicatalog_id = Column(Integer, ForeignKey('aicatalog.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'picture': self.picture,
            'description': self.description,
            'id': self.id,
        }


class AiBook(Base):
    __tablename__ = 'aibook'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    author = Column(String(80))
    price = Column(String(8))
    picture = Column(String(250))
    description = Column(String(250))
    aicatalog_id = Column(Integer, ForeignKey('aicatalog.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'author': self.author,
            'price': self.price,
            'picture': self.picture,
            'description': self.description,
            'id': self.id,
        }


class AiNews(Base):
    __tablename__ = 'ainews'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    picture = Column(String(250))
    description = Column(String(2000))
    aicatalog_id = Column(Integer, ForeignKey('aicatalog.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'picture': self.picture,
            'description': self.description,
            'id': self.id,
        }


class AiMatch(Base):
    __tablename__ = 'aimatch'

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    participant_A = Column(String(80), nullable=False)
    participant_B = Column(String(80), nullable=False)
    place = Column(String(250))
    picture = Column(String(250))
    description = Column(String(250))
    aicatalog_id = Column(Integer, ForeignKey('aicatalog.id'))
    user_id = Column(Integer, ForeignKey('user.id'))

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'name': self.name,
            'participant_A': self.participant_A,
            'participant_B': self.participant_B,
            'place': self.place,
            'picture': self.picture,
            'description': self.description,
            'id': self.id,
        }

if __name__ == '__main__':

    # PostgreSQL
    engine = create_engine('postgresql://catalog:ducky@localhost/ai')

    # SQlite
    # engine = create_engine('sqlite:///Ai.db')
    Base.metadata.create_all(engine)

    print("Making ai database done!")
