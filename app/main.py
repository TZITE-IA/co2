from flask import Flask, request, jsonify, redirect, url_for, render_template, flash
from datetime import datetime
from sharedTools import *
from ach import *
from flask_cors import CORS
import numpy as np

app= Flask(__name__)
DB = database("db")
log = database("login")
app.config['CORS_HEADERS'] = 'Content-Type'
CORS(app)


#Iot de CO2s

@app.route("/") #Actualizada
def all():
      return jsonify(DB.load())

@app.route("/central") #Actualizada
def allCentral():
      db = {}
      d = DB.load()
      for key in d.keys():
            db[key] = d[key]["central"]
      return jsonify(db)

@app.route("/lateral") #Actualizada
def allLateral():
      db = {}
      d = DB.load()
      for key in d.keys():
            db[key] = d[key]["lateral"]
      return jsonify(db)

@app.route("/<string:sen>") #Actualizado
def sensor(sen):
      db = DB.load()
      if exist(sen, db):
            return jsonify(db[sen])
      else:
            return jsonify({"error":"'"+sen+"' not exist"})

@app.route("/last/<string:val>")
def lastVal(val): #falta actualizar
      try:
            val = int(val)
      except Exception:
            return jsonify({"error": val +" no es una entrada valida"})
      db = {}
      d = DB.load()
      for key in d.keys():
            db[key] = {"central":{"DATE": d[key]["central"]["DATE"][::-1][::val],
                                  "HUM":d[key]["central"]["HUM"][::-1][::val],
                                  "PPM":d[key]["central"]["PPM"][::-1][::val],
                                  "TEMP":d[key]["central"]["TEMP"][::-1][::val]},
                       "lateral":{"DATE":d[key]["central"]["DATE"][::-1][::val],
                                  "HUM":d[key]["central"]["HUM"][::-1][::val],
                                  "PPM":d[key]["central"]["PPM"][::-1][::val],
                                  "TEMP":d[key]["central"]["TEMP"][::-1][::val]}}
      return jsonify(db)

@app.route("/new/<string:sen>") #Actualizado
def postNewSensor(sen):
      db = DB.load()
      if exist(sen, db):
            return jsonify({"error": "'"+sen+"' alrredy exists"})
      else:
            db[sen] = {"central":{"DATE":[],"HUM":[],"PPM":[],"TEMP":[]},"lateral":{"DATE":[],"HUM":[],"PPM":[],"TEMP":[]}}
            DB.update(db)
            return jsonify({"sucess": "'"+sen+"' fue creado correctamente"})

@app.route("/clear/<string:sen>") #Actualizado
def clearValues(sen):
      db = DB.load()
      if exist(sen, db):
            db[sen] = {"central":{"DATE":[],"HUM":[],"PPM":[],"TEMP":[]},"lateral":{"DATE":[],"HUM":[],"PPM":[],"TEMP":[]}}
            DB.update(db)
            return jsonify({"sucess": "'"+sen+"' fue limpiado correctamente"})
      else:
            return jsonify({"error": "'"+sen+"' does not exists"})

@app.route("/update", methods=["PUT"]) #Actualizado
def updateValues():
      """
      request - 
      {
        "name": "nombre",
        "site": "ubicación"
        "series": {
            "HUM": [],
            "PPM": [],
            "TEMP": []
          }
      }
      """
      post = request.json
      db = DB.load()
      if exist(post["name"], db):
            now = datetime.now()
            db[post["name"]][post["site"]]["PPM"].append(post["series"]["PPM"])
            db[post["name"]][post["site"]]["HUM"].append(post["series"]["HUM"])
            db[post["name"]][post["site"]]["TEMP"].append(post["series"]["TEMP"])
            db[post["name"]][post["site"]]["DATE"].append(str(now.date())+"/"+str(now.time()))
            DB.update(db)
            return jsonify({"sucess": "'"+post["name"]+"' fue falta actualizar correctamente"})
      else:
            return jsonify({"error": "'"+post["name"]+"' does not exists"})

@app.route("/delete/<string:sen>", methods=["DELETE"])
def deleteSensor(sen): #Actualizado
      db = DB.load()
      if exist(sen, db):
            db.pop(sen)
            DB.update(db)
            return jsonify({"sucess": "'"+sen+"' was deleted"})
      else:
            return jsonify({"error": "'"+sen+"' does not exists"})

#Cálculo de ACH

@app.route("/ach") 
def ach():   #falta actualizar
      temp = []
      x = []
      for sens in DB.load():
            x.append(ach.ach_computing(sens))
            # try:   
            #       inicio = sens["params"][0]["series"][::-1][1]
            #       final = sens["params"][0]["series"][::-1][0]
            #       afuera_i = sens["params"][1]["series"][::-1][1]
            #       afuera_f = sens["params"][1]["series"][::-1][0]
            #       temp.append({"name":sens["name"]+"-ACH", "ACH": ACH(inicio, final, afuera_i, afuera_f) , "time": sens["params"][0]["series"][::-1][0]["name"]})
            # except Exception:
            #       temp.append({"name":sens["name"]+"-ACH", "ACH": "Faltan datos" , "time": "Sin fecha"})
      print(x)
      return jsonify({"ach":x})

#Access login

@app.route("/login/validate", methods=["POST"])
def validate():
      """
      request - 
      {
            "user": "name",
            "pwd" : "password"
      }
      """
      post = request.json
      users = log.load()
      for user in users:
            if post["user"] == user["user"]:
                  if post["pwd"] == user["pwd"]:
                        return jsonify({"error": "Acceso concedido", "acess": True})
                  else:
                        return jsonify({"error": "Contraseña incorrecta", "acess": False})
      return jsonify({"error": "Usuario no existe", "acess": False})

@app.route("/login/add", methods=["POST"])
def addUser():
      """
      request - 
      {
            "user": "name"
      }
      """
      post = request.json
      users = log.load()
      for user in users:
            if post["user"] == user["user"]:
                  return jsonify({"error": "Usuario ya existe"})
      try:
            users.append({"user": post["user"], "pwd" : post["pwd"]})
            log.update(users)
            return jsonify({"success": "Usuario registrado exitosamente"})
      except Exception:
            return jsonify({"error": "Entrada inválida"})

@app.route("/login/delete", methods=["DELETE"])
def deleteUser():
      post = request.json
      users = log.load()
      for i, user in enumerate(users):
            if post["user"] == user["user"]:
                  users.pop(i)
                  log.update(users)
                  return jsonify({"success": "Usuario eliminado correctamente"})
      return jsonify({"error": "Este usuario no existe"})