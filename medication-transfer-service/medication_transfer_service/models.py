"""Data models."""
from email.policy import default
from sre_parse import State
from . import db, ma
import datetime


class Drone(db.Model):

    __tablename__    = 'drones'
    __table_args__   = {'extend_existing': True}
    id               = db.Column( db.Integer, primary_key=True, autoincrement=True )
    serial_no        = db.Column( db.String(100), index=False, unique=True, nullable=False )
    model            = db.Column( db.Enum("Lightweight", "Middleweight", "Cruiserweight", "Heavyweight", name="model_enum") )
    weight           = db.Column( db.Numeric(5,2), index=False, nullable=False )
    battery_capacity = db.Column( db.Integer(), nullable=False )
    state            = db.Column( db.Enum("IDLE", "LOADING", "LOADED", "DELIVERING", "DELIVERED", name="state_enum"), default="IDLE" )
    created_on       = db.Column( db.DateTime(), default=datetime.datetime.utcnow )
    updated_on       = db.Column( db.DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow )

    def __repr__(self):
        return f'serial number: {self.serial_no} model: {self.model} weight: {self.weight} battery capacity: {self.battery_capacity} state: {self.state} created on: {self.created_on} updated on: {self.updated_on}'


class Medication(db.Model):

    __tablename__    = 'medications'
    __table_args__   = {'extend_existing': True}
    id               = db.Column( db.Integer, primary_key=True, autoincrement=True )
    name             = db.Column( db.String(255), nullable=False )
    weight           = db.Column( db.Numeric(5,2), index=False, nullable=False )
    code             = db.Column( db.String(255), nullable=False, unique=True )
    image            = db.Column( db.String(255) )
    created_on       = db.Column( db.DateTime(), default=datetime.datetime.utcnow)
    updated_on       = db.Column( db.DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    def __repr__(self):
        return f'name: {self.name} weight: {self.weight} code: {self.code} image: {self.image} created on: {self.created_on} updated on: {self.updated_on}'

class DroneSchema(ma.Schema):
    class Meta:
        model        = Drone
        sqla_session = db.session

class DroneMeds(db.Model):

    __tablename__    = 'drone_with_medication'
    __table_args__   = {'extend_existing': True}
    id               = db.Column( db.Integer, primary_key=True, autoincrement=True )
    drone_serial_no  = db.Column(db.Integer, db.ForeignKey('drones.serial_no'))
    meds_code        = db.Column(db.Integer, db.ForeignKey('medications.code'))
    created_on       = db.Column( db.DateTime(), default=datetime.datetime.utcnow )
    updated_on       = db.Column( db.DateTime(), default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow )