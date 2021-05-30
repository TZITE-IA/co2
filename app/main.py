from flask import Flask, request, jsonify, redirect, url_for, render_template, flash
from datetime import datetime
from sharedTools import *
from flask_cors import CORS

app= Flask(__name__)
DB = database("db")
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)

@app.route("/") #actualizado
def all():
      return jsonify(DB.load())

@app.route("/in") #actualizado
def allIn():
      db = []
      for i, d in enumerate(DB.load()):
            db.append({"name":d["name"], "series":d["params"][0]["series"]})
      return jsonify(db)

@app.route("/out") #actualizado
def allOut():
      db = []
      for i, d in enumerate(DB.load()):
            db.append({"name":d["name"], "series":[]})
            for j, b in enumerate([d["params"][1]]):
                  db[i]["series"].append(b["series"])
                  j+=1
            i+=1
      return jsonify(db)
    
@app.route("/<string:sen>") #actualizado
def sensor(sen):
      for s in DB.load():
            if sen == s["name"]:
                  return jsonify(s)
      return jsonify({"error":"'"+sen+"' not exist"})
            
@app.route("/last/<string:val>")
def lastVal(val): #actualizado
      try:
            val = int(val)
      except Exception:
            return jsonify({"error": val +" no es una entrada valida"})
      db = []
      for i, d in enumerate(DB.load()):
            db.append({"name":d["name"], "series":[]})
            for j, b in enumerate(d["params"]):
                  for series in b["series"][::-1][:int(val)]:
                        db[i]["series"].append(series)
                  j+=1
            i+=1
      return jsonify(db)

@app.route("/new/<string:sen>") #actualizado
def postNewSensor(sen):
      db = DB.load()
      if exist(sen, db):
            return jsonify({"error": "'"+sen+"' alrredy exists"})
      else:
            db.append({"name":sen,"params": [{"name": "Adentro", "series": []},{"name": "Afuera", "series": []}]})
            DB.update(db)
            return jsonify({"sucess": "'"+sen+"' fue creado correctamente"})
      
@app.route("/clear/<string:sen>") #actualizado
def clearValues(sen):
      db = DB.load()
      exist = [i for i, s in enumerate(db) if sen == s["name"]]
      if len(exist) == 0:
            return jsonify({"error": "'"+sen+"' does not exists"})
      else:
            db[exist[0]]["params"]= [{"name":"Adentro","series":[]},{"name":"Afuera","series":[]}]
            DB.update(db)
            return jsonify({"sucess": "'"+sen+"' fue limpiado correctamente"})

@app.route("/update", methods=["PUT"]) #actualizado
def updateValues():
      """
      request - 
      {
        "name": "nombre",
        "site": "ubicación"
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
            now = datetime.now()
            for i, ub in enumerate(db[exist[0]]["params"]):
                  if ub["name"] == post["site"]:
                        db[exist[0]]["params"][i]["series"].append({"value": post["series"]["value"], "name":str(now.date())+"/"+str(now.time())})
            DB.update(db)
            return jsonify({"sucess": "'"+post["name"]+"' fue actualizado correctamente"})
      

@app.route("/delete/<string:sen>", methods=["DELETE"])
def deleteSensor(sen): #actualizado
      db = DB.load()
      exist = [i for i, s in enumerate(db) if sen == s["name"]]
      if len(exist) == 0:
            return jsonify({"error": "'"+sen+"' does not exists"})
      else:
            db.pop(exist[0])
            DB.update(db)
            return jsonify({"sucess": "'"+sen+"' was deleted"})

@app.route("/ach")
def ach():
      temp = []
      for sens in DB.load():
            try:   
                  inicio = sens["params"][0]["series"][::-1][1]
                  final = sens["params"][0]["series"][::-1][0]
                  afuera_i = sens["params"][1]["series"][::-1][1]
                  afuera_f = sens["params"][1]["series"][::-1][0]
                  temp.append({"name":sens["name"]+"-ACH", "ACH": ACH(inicio, final, afuera_i, afuera_f) , "time": sens["params"][0]["series"][::-1][0]["name"]})
            except Exception:
                  temp.append({"name":sens["name"]+"-ACH", "ACH": "Faltan datos" , "time": "Sin fecha"})
      return jsonify(temp)
      