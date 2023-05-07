import sqlalchemy as db
from sqlalchemy.orm import Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship



engine = db.create_engine('sqlite:///safetybot.db', echo=True)
connection = engine.connect()
session = Session(engine)

Base = declarative_base()


class SBdata(Base):
    __tablename__ = "registration"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    password = db.Column(db.String)
    camera = relationship("Camera")



class Camera(Base):
    __tablename__ = 'cameras'

    id = db.Column(db.Integer, primary_key=True)
    ip = db.Column(db.String(100), nullable=False)
    place = db.Column(db.String(100), nullable=False)
    state = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('registration.id'))