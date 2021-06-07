from flask import Flask, url_for, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_cors import  cross_origin

app_clientes = Flask(__name__)
app_clientes.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clientes.db'
app_clientes.config['SECRET_KEY'] = "123"
cors = CORS(app_clientes)
app_clientes.config['CORS_HEADERS'] = "Content-Type"

db = SQLAlchemy(app_clientes)

class cliente(db.Model):
    id_cliente  = db.Column("id_cliente", db.Integer, primary_key=True)
    nombre_cliente = db.Column(db.String(100))
    direccion_cliente = db.Column(db.String(100))
    telefono_cliente = db.Column(db.Integer)

    def __init__(self, datos):
        self.nombre_cliente = datos["nombre_cliente"]
        self.direccion_cliente = datos["direccion_cliente"]
        self.telefono_cliente = datos["telefono_cliente"]

@app_clientes.route("/")
@cross_origin()

def principal():
    data = cliente.query.all()
    diccionario_clientes = {}
    for d in data:
        p = {"id_cliente": d.id_cliente,
             "nombre_cliente": d.nombre_cliente,
             "direccion_cliente": d.direccion_cliente,
             "telefono_cliente": d.telefono_cliente
            }
        diccionario_clientes[d.id_cliente] = p
    return diccionario_clientes

@app_clientes.route("/agregar/<nombre>/<direccion>/<int:telefono>")
@cross_origin()

def agregar(nombre, direccion, telefono):
    datos = {"nombre_cliente": nombre,
             "direccion_cliente": direccion,
             "telefono_cliente": telefono
            }
    p = cliente(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))


@app_clientes.route("/eliminar/<int:id_cliente>")
@cross_origin()

def eliminar(id_cliente):
    p = cliente.query.filter_by(id_cliente=id_cliente).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))


@app_clientes.route("/actualizar/<int:id_cliente><nombre>/<direccion>/<int:telefono>")
@cross_origin()

def actualizar (id_cliente, nombre, direccion,telefono):
    p = cliente.query.filter_by(id_cliente=id_cliente).first()
    p.nombre_cliente = nombre
    p.direccion_cliente = direccion
    p.telefono_cliente = telefono
    db.session.commit()
    return redirect(url_for('principal'))


@app_clientes.route("/buscar/<int:id_cliente>")
@cross_origin()

def buscar(id_cliente):
    d = cliente.query.filter_by(id_cliente=id_cliente).first()
    p = {"id_cliente": d.id_cliente,
         "nombre_cliente": d.nombre_cliente,
         "direccion_cliente": d.direccion_cliente,
         "telefono_cliente": d.telefono_cliente
        }
    return p

if __name__ =="__main__":
            db.create_all()
            app_clientes.run(debug=True)






