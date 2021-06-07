from flask import Flask, url_for, redirect
from flask.helpers import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_cors import  cross_origin

app_pedidos = Flask(__name__)
app_pedidos.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///pedidos.db'
app_pedidos.config['SECRET_KEY'] = "123"
cors = CORS(app_pedidos)
app_pedidos.config['CORS_HEADERS'] = "Content-Type"

db = SQLAlchemy(app_pedidos)

class pedido(db.Model):
    id_pedido  = db.Column("id_pedido", db.Integer, primary_key=True)
    id_producto = db.Column(db.Integer)
    id_cliente = db.Column(db.Integer)
    id_domiciliario= db.Column(db.String(100))
    cantidad_articulos = db.Column(db.Integer)

    def __init__(self, datos):
        self.id_producto = datos["id_producto"]
        self.id_cliente = datos["id_cliente"]
        self.id_domiciliario = datos["id_domiciliario"]
        self.cantidad_articulos = datos["cantidad_articulos"]

@app_pedidos.route("/")
@cross_origin()

def principal():
    data = pedido.query.all()
    diccionario_pedidos = {}
    for d in data:
        p = {"id_pedido": d.id_pedido,
             "id_producto": d.id_producto,
             "id_cliente": d.id_cliente,
             "id_domiciliario": d.id_domiciliario,
             "cantidad_articulos": d.cantidad_articulos
            }
        diccionario_pedidos[d.id_pedido] = p
    return diccionario_pedidos

@app_pedidos.route("/agregar/<int:id_producto>/<int:id_cliente>/<int:id_domiciliario>/<int:cantidad_articulos>")
@cross_origin()

def agregar(id_producto, id_cliente, id_domiciliario,cantidad_articulos ):
    datos = {"id_producto": id_producto,
             "id_cliente": id_cliente,
             "id_domiciliario": id_domiciliario,
             "cantidad_articulos": cantidad_articulos
            }
    p = pedido(datos)
    db.session.add(p)
    db.session.commit()
    return redirect(url_for('principal'))


@app_pedidos.route("/eliminar/<int:id_pedido>")
@cross_origin()

def eliminar(id_pedido):
    p = pedido.query.filter_by(id_pedido=id_pedido).first()
    db.session.delete(p)
    db.session.commit()
    return redirect(url_for('principal'))


@app_pedidos.route("/actualizar/<int:id_pedido>/<int:id_producto>/<int:id_cliente>/<int:id_domiciliario>/<int:cantidad_articulos>")
@cross_origin()

def actualizar (id_pedido, id_producto, id_cliente,id_domiciliario, cantidad_articulos):
    p = pedido.query.filter_by(id_pedido=id_pedido).first()
    p.id_producto = id_producto
    p.id_cliente = id_cliente
    p.id_domiciliario = id_domiciliario
    p.cantidad_articulos = cantidad_articulos
    db.session.commit()
    return redirect(url_for('principal'))


@app_pedidos.route("/buscar/<int:id_pedido>")
@cross_origin()

def buscar(id_pedido):
    d = pedido.query.filter_by(id_pedido=id_pedido).first()
    p = {"id_pedido": d.id_pedido,
         "id_producto": d.id_producto,
         "id_cliente": d.id_cliente,
         "id_domiciliario": d.id_domiciliario,
         "cantidad_articulos": d.id_domiciliario
        }
    return p

if __name__ =="__main__":
            db.create_all()
            app_pedidos.run(debug=True)






