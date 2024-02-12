from . import db
from sqlalchemy.sql import func

class Odontologo(db.Model):
    __tablename__ = "Odontologo"
    id = db.Column(db.Integer, primary_key=True)
    dni = db.Column(db.Integer)
    matricula = db.Column(db.String(100))
    nombre = db.Column(db.String(100))
    apellido = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    direcciones = db.relationship('Direccion', backref="Odontologo")

class Direccion(db.Model):
    __tablename__ = "Direccion"
    id = db.Column(db.Integer, primary_key = True)
    calle = db.Column(db.String(100))
    departamento = db.Column(db.String(50))
    numero = db.Column(db.Integer)
    localidad_id= db.Column(db.Integer, db.ForeignKey("Localidad.id"))
    odontologo_id= db.Column(db.Integer, db.ForeignKey("Odontologo.id"))



class Localidad(db.Model):
    __tablename__ = "Localidad"
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100))
    provincia_id= db.Column(db.Integer, db.ForeignKey("Provincia.id"))
    direcciones = db.relationship('Direccion', backref="Localidad")


class Provincia(db.Model):
    __tablename__ = "Provincia"
    id = db.Column(db.Integer, primary_key = True)
    nombre = db.Column(db.String(100))
    localidades = db.relationship('Localidad', backref="Provincia")

