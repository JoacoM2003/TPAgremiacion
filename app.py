from . import app, db
from flask import request, make_response, render_template, url_for, redirect
from .models import *
from sqlalchemy import select

@app.route("/")
def index():
    odontologos = Odontologo.query.all()
    return render_template('odontologos/index_v13.html', odontologos=odontologos)

@app.route("/create")
def create():
    odontologos = Odontologo.query.all()
    return render_template('odontologos/create_v13.html')

@app.route("/store", methods=['POST'])
def store():
    _dni = request.form["txtDNI"]
    _matricula = request.form['txtMatricula']
    _nombre = request.form['txtNombre']
    _apellido = request.form['txtApellido']
    _correo = request.form['txtCorreo']

    if _dni == '' or _matricula == '' or _nombre == '' or _apellido == '' or _correo == '':
        flash('Faltan datos del odontólogo.')
        return redirect(url_for('create'))

    odontologo = Odontologo(
        dni = _dni,
        matricula = _matricula,
        nombre = _nombre,
        apellido = _apellido,
        correo = _correo
    )

    db.session.add(odontologo)
    db.session.commit()

    return redirect("/")

@app.route("/delete/<int:id>")
def delete(id):
    odontologo = Odontologo.query.filter_by(id = id).first()
    db.session.delete(odontologo)
    db.session.commit()
    return redirect("/")

@app.route("/odontologo/<int:id>")
def odontologo(id):
    odontologo = Odontologo.query.filter_by(id = id).first()
    direcciones = Direccion.query.filter_by(odontologo_id = odontologo.id).all()
    for direccion in direcciones:
        localidad = Localidad.query.filter_by(id = direccion.localidad_id).first()
        provincia = Provincia.query.filter_by(id = localidad.provincia_id).first()
    return render_template('odontologos/odontologo.html', odontologo=odontologo, direcciones = direcciones, localidad = localidad, provincia = provincia)

@app.route("/agregarDireccion/<int:id>")
def agregarDireccion(id):
    odontologo = Odontologo.query.filter_by(id = id).first()
    return render_template("odontologos/direcciones.html", odontologo = odontologo)

@app.route("/guardarDireccion", methods=["POST"])
def guardarDireccion():
    _provincia = request.form['txtProvincia']
    _localidad = request.form['txtLocalidad']
    _direccion = request.form['txtCalle']
    _numero = request.form['txtNumero']
    _departamento = request.form['txtDepartamento']
    o_id = request.form['txtID']

    provincia = Provincia(
        nombre = _provincia
    )
    db.session.add(provincia)
    db.session.commit()

    localidad = Localidad(
        nombre = _localidad,
        provincia_id = provincia.id
    )
    db.session.add(localidad)
    db.session.commit()

    direccion = Direccion(
        calle = _direccion,
        numero = _numero,
        departamento = _departamento,
        localidad_id = localidad.id,
        odontologo_id = o_id
    )
    db.session.add(direccion)
    db.session.commit()
    
    return redirect("/")


if __name__ == '__main__':
    app.debug = True
    app.run()
