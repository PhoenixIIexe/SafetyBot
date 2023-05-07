import sqlalchemy as db
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

engine = db.create_engine('sqlite:///date.db', echo=True)
connection = engine.connect()
session = Session(engine)

Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    tg_id = db.Column(db.Integer)
    camera = relationship("Camera")


class Camera(Base):
    __tablename__ = 'camera'
    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
