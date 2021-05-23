from flask import Flask, request, jsonify
import json

app= Flask(__name__)

class database(object):
    def __init__(self, file):
        self.file = file
        
    def load(self):
        with open('app/db.json') as json_file:
            db = json.load(json_file)
            return db
    
    def update(self, db):
        with open('app/db.json', 'w') as outfile:
            json.dump(db, outfile)

DB = database("db.json")

@app.route("/")
def all():
      db = DB.load()
      print([s["label"] for s in db])
      return jsonify(db)
    
@app.route("/<string:sensor>")
def sensor(sen):
      return jsonify([s for s in DB.load() if sen == s["label"]][0])

@app.route("/new", methods=["POST"])
def postNewSensor():
    post = request.json
    db = DB.load()
    exist = ["True" for s in db if post["label"] == s["label"]]
    if len(exist) > 0:
          return jsonify({"error": "'"+post["label"]+"' alrredy exists"})
    else:
          db.append(post)
          DB.update(db)
          return jsonify(DB.load())
    # products.append(nuevo)
    # return jsonify({"message":"Añadido correctamente","products": products})






@app.route("/products/<string:producto>", methods=["PUT"])
def editProduct(producto):
    res = []
    for item in products:
        if producto == item["name"]:
            res.append(item)
    if len(res) > 0:
        res[0]["name"] =  request.json["name"]
        res[0]["price"] = request.json["price"]
        res[0]["quantity"] = request.json["quantity"]
        return jsonify({"result":"Hecho","producto actualizado":res[0]})
    else:
        return jsonify({"result":"Producto no encontrado"})

@app.route("/products/<string:producto>", methods=["DELETE"])
def deleteProduct(producto):
    res = []
    for item in products:
        if producto == item["name"]:
            res.append(item)
    if len(res) > 0:
        products.remove(res)
        return jsonify({"result":"Eliminado","producto eliminado": res})
    else:
        return jsonify({"result":"Producto no encontrado"})
      
@app.route("/products")
def getProducts():
    return jsonify(products)

@app.route("/products/<string:producto>")
def getProduct(producto):
    res = []
    for item in products:
        if producto == item["name"]:
            res.append(item)
    return jsonify(res)
