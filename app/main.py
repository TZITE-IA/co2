from flask import Flask, request, jsonify
from sharedTools import *
from flask_cors import CORS


app= Flask(__name__)
DB = database("db")
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)
#cors = CORS(app, resources={r"/*":{"origins": "*"}})

@app.route("/")
def all():
      db = DB.load()
      return jsonify(db)
    
@app.route("/<string:sen>")
def sensor(sen):
      for s in DB.load():
            if sen == s["name"]:
                  return jsonify(s)

@app.route("/new/<string:sen>")
def postNewSensor(sen):
      #return jsonify({"respuesta": "funciona aqui"})
      db = DB.load()
      
      exist = ["True" for i, s in enumerate(db) if sen == s["name"]]
      if len(exist) > 0:
            return jsonify({"error": "'"+sen+"' alrredy exists"})
      else:
            db.append({"name":sen,"series":[ {"value" : 0,"name": "0"}]})
            DB.update(db)
            return jsonify({"sucess": "'"+sen+"' fue creado correctamente"})

@app.route("/update", methods=["PUT"])
def updateValues():
      """
      request - 
      {
        "name": "nombre",
        "series": {
          "value": number,
          "name": string
          }
      }
      """
      post = request.json
      db = DB.load()
      exist = [i for i, s in enumerate(db) if post["name"] == s["name"]]
      if len(exist) == 0:
            return jsonify({"error": "'"+post["name"]+"' does not exists"})
      else:
            db[exist[0]]["series"].append(post["series"])
            DB.update(db)
            return jsonify({"sucess": "'"+post["name"]+"' fue actualizado correctamente"})

@app.route("/delete/<string:sen>", methods=["DELETE"])
def deleteSensor(sen):
      db = DB.load()
      exist = [i for i, s in enumerate(db) if sen == s["name"]]
      if len(exist) == 0:
            return jsonify({"error": "'"+sen+"' does not exists"})
      else:
            db.pop(exist[0])
            DB.update(db)
            return jsonify({"sucess": "'"+sen+"' was deleted"})
  