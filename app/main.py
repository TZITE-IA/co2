from flask import Flask, request, jsonify
from sharedTools import *
import logging
try:
    from flask_cors import CORS  # The typical way to import flask-cors
except ImportError:
    # Path hack allows examples to be run without installation.
    import os
    parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.sys.path.insert(0, parentdir)

    from flask_cors import CORS


app= Flask(__name__)
DB = database("db")
logging.basicConfig(level=logging.INFO)
logging.getLogger('flask_cors').level = logging.DEBUG
CORS(app)

@app.route("/")
def all():
      db = DB.load()
      return jsonify(db)
    
@app.route("/<string:sen>")
def sensor(sen):
      for s in DB.load():
            if sen == s["name"]:
                  return jsonify(s).headers.add("Access-Control-Allow-Origin", "*")

@app.route("/new/<string:sen>", methods=["POST"])
def postNewSensor(sen):
      db = DB.load()
      exist = ["True" for i, s in enumerate(db) if sen == s["name"]]
      if len(exist) > 0:
            return jsonify({"error": "'"+sen+"' alrredy exists"}).headers.add("Access-Control-Allow-Origin", "*")
      else:
            db.append({"name":sen,"series":[ {"value" : 0,"name": "0"}]})
            DB.update(db)
            return jsonify({"sucess": "'"+sen+"' fue creado correctamente"}).headers.add("Access-Control-Allow-Origin", "*")

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
            return jsonify({"error": "'"+post["name"]+"' does not exists"}).headers.add("Access-Control-Allow-Origin", "*")
      else:
            db[exist[0]]["series"].append(post["series"])
            DB.update(db)
            return jsonify({"sucess": "'"+post["name"]+"' fue actualizado correctamente"}).headers.add("Access-Control-Allow-Origin", "*")

@app.route("/delete/<string:sen>", methods=["DELETE"])
def deleteSensor(sen):
      db = DB.load()
      exist = [i for i, s in enumerate(db) if sen == s["name"]]
      if len(exist) == 0:
            return jsonify({"error": "'"+sen+"' does not exists"}).headers.add("Access-Control-Allow-Origin", "*")
      else:
            db.pop(exist[0])
            DB.update(db)
            return jsonify({"sucess": "'"+sen+"' was deleted"}).headers.add("Access-Control-Allow-Origin", "*")
  