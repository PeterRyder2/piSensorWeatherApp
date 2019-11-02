from app import db
from datetime import datetime

class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    MoistureRead = db.relationship('MoistureRead', backref='person', lazy=True)
    UserSignIn = db.relationship('UserSignIn', backref='person', lazy=True)
    MinValue = db.relationship('MinValue', backref='person', lazy= True)

class MoistureRead(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    MReading = db.Column(db.REAL, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)

class LightTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Lightreading  = db.Column(db.REAL, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)

class HumidityTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    humidReading = db.Column(db.REAL, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)

class TemperatureTable(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tempReading = db.Column(db.REAL, nullable=False)
    pub_date = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)


class UserSignIn(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    SignInDate = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)


class MinValue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dateOfChange = db.Column(db.DateTime, nullable=False,
        default=datetime.utcnow)
    changeTo =  db.Column(db.Integer, nullable=False)
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
        nullable=False)
