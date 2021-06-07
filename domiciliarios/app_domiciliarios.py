from flask import Flask, url_for, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_cors import  cross_origin

app_domiciliarios = Flask(__name__)
app_domiciliarios.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///domiciliarios.db'
app_domiciliarios.config['SECRET_KEY'] = "123"
cors = CORS(app_domiciliarios)
app_domiciliarios.config['CORS_HEADERS'] = "Content-Type"

db = SQLAlchemy(app_domiciliarios)

class domiciliario(db.Model):
    id_domiciliario  = db.Column("id_domiciliario", db.Integer, primary_key=True)
    nombre_domiciliario = db.Column(db.String(100))
    direccion_domiciliario = db.Column(db.String(100))
    telefono_domiciliario = db.Column(db.Integer)

    def __init__(self, datos):
        self.nombre_domiciliario = datos["nombre_domiciliario"]
        self.direccion_domiciliario = datos["direccion_domiciliario"]
        self.telefono_domiciliario = datos["telefono_domiciliario"]

@app_domiciliarios.route("/")
@cross_origin()

def principal():
    data = domiciliario.query.all()
    diccionario_domiciliarios = {}
    for d in data:
        p = {"id_domiciliario": d.id_domiciliario,
             "nombre_domiciliario": d.nombre_domiciliario,
             "direccion_domiciliario": d.direccion_domiciliario,
             "telefono_domiciliario": d.telefono_domiciliario
            }
        diccionario_domiciliarios[d.id_domiciliario] = p
    return diccionario_domiciliarios

@app_domiciliarios.route("/agregar/<nombre_domiciliario>/<direccion_domiciliario>/<int:telefono_domiciliario>")
@cross_origin()

def agregar(nombre_domiciliario, direccion_domiciliario, telefono_domiciliario):
    datos = {"nombre_domiciliario": nombre_domiciliario,
             "direccion_domiciliario": direccion_domiciliario,
             "telefono_domiciliario": telefono_domiciliario
            }
    p = domiciliario(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))


@app_domiciliarios.route("/eliminar/<int:id_domiciliario>")
@cross_origin()

def eliminar(id_domiciliario):
    p = domiciliario.query.filter_by(id_domiciliario=id_domiciliario).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))


@app_domiciliarios.route("/actualizar/<int:id_domiciliario><nombre_domiciliario>/<direccion_domiciliario>/<int:telefono_domiciliario>")
@cross_origin()

def actualizar (id_domiciliario, nombre_domiciliario, direccion_domiciliario,telefono_domiciliario):
    p = domiciliario.query.filter_by(id_domiciliario=id_domiciliario).first()
    p.nombre_domiciliario = nombre_domiciliario
    p.direccion_domiciliario = direccion_domiciliario
    p.telefono_domiciliario = telefono_domiciliario
    db.session.commit()
    return redirect(url_for('principal'))


@app_domiciliarios.route("/buscar/<int:id_domiciliario>")
@cross_origin()

def buscar(id_domiciliario):
    d = domiciliario.query.filter_by(id_domiciliario=id_domiciliario).first()
    p = {"id_domiciliario": d.id_domiciliario,
         "nombre_domiciliario": d.nombre_domiciliario,
         "direccion_domiciliario": d.direccion_domiciliario,
         "telefono_domiciliario": d.telefono_domiciliario
        }
    return p

if __name__ =="__main__":
            db.create_all()
            app_domiciliarios.run(debug=True)






