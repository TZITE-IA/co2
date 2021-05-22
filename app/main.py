from flask import Flask, jsonify, request

app= Flask(__name__)

@app.route("/")
def ping():
    return jsonify({"result":"Pong!"})

# @app.route("/products")
# def getProducts():
#     return jsonify(products)

# @app.route("/products/<string:producto>")
# def getProduct(producto):
#     res = []
#     for item in products:
#         if producto == item["name"]:
#             res.append(item)
#     return jsonify(res)

# @app.route("/products", methods=["POST"])
# def postProduct():
#     nuevo = {
#         "name": request.json["name"],
#         "price": request.json["price"],
#         "quantity": request.json["quantity"]
#     }
#     products.append(nuevo)
#     return jsonify({"message":"Añadido correctamente","products": products})

# @app.route("/products/<string:producto>", methods=["PUT"])
# def editProduct(producto):
#     res = []
#     for item in products:
#         if producto == item["name"]:
#             res.append(item)
#     if len(res) > 0:
#         res[0]["name"] =  request.json["name"]
#         res[0]["price"] = request.json["price"]
#         res[0]["quantity"] = request.json["quantity"]
#         return jsonify({"result":"Hecho","producto actualizado":res[0]})
#     else:
#         return jsonify({"result":"Producto no encontrado"})

# @app.route("/products/<string:producto>", methods=["DELETE"])
# def deleteProduct(producto):
#     res = []
#     for item in products:
#         if producto == item["name"]:
#             res.append(item)
#     if len(res) > 0:
#         products.remove(res)
#         return jsonify({"result":"Eliminado","producto eliminado": res})
#     else:
#         return jsonify({"result":"Producto no encontrado"})