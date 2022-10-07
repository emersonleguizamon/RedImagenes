

import hashlib
from flask import Flask, render_template, request, redirect, url_for
app=Flask(__name__)

import sqlite3
from werkzeug.utils import secure_filename
import os



FOLDER_IMAGES=os.path.join('static','img')
app.config['UPLOAD_FOLDER']=FOLDER_IMAGES


#Endpoint principal, dirige al home
@app.route("/", methods=["GET"])
def home ():
    return render_template("index.html")

#Endpoint para redireccionar a vista para loguearse (vista2), o registrarse (vista3)
@app.route("/login", methods=["POST"])
def login():
    if 'btnIniciar'in request.form:
        return render_template("vista2.html")
    if'btnRegistrar'in request.form:
        return render_template("vista3.html")
    return "Seleccione una opción"

#Endpoint para loguearse en vista 2
@app.route("/loguearse", methods=["POST"])
def ingreso():
    usuario=request.form["txtUsuario"]
    contrasena=request.form["txtPassword"]
    if not usuario or not contrasena:
        return "Usuario o contraseña requeridos"
    if len(usuario)>20:
        return "Usuario excede longitud maxima permitida"
   
    #Codificacion / cifrado contraseña
    clave=hashlib.sha256(contrasena.encode())
    pwd=clave.hexdigest()

    #Conexión a base de datos
    with sqlite3.connect("basedatos.db") as con:
        cur=con.cursor()
        cur.execute("select 1 from Usuarios where Username= ? and Password= ?",[usuario, pwd])
        if cur.fetchone():
             return render_template("vista4.html")
    return "Usuario invalido!!!"

#Endpoint para registarse en vista 3
@app.route("/registro", methods=["POST"])
def registro():
    id=request.form["txtId"]
    nombre=request.form["txtNombre"]
    apellido=request.form["txtApellido"]
    correo=request.form["txtCorreo"]
    username=request.form["txtUsuario"]
    password=request.form["txtPassword"]
    if not id or not nombre or not apellido or not correo or not password:
        return "Falta ingresar un dato de registro" 

    clave=hashlib.sha256(password.encode())
    pwd=clave.hexdigest()
    #Conexión BD
    with sqlite3.connect("basedatos.db") as con:
        cur=con.cursor()
        #Verificar si ya existe el usuario
        cur.execute("SELECT Username from Usuarios where Username= ?", [username])
        if cur.fetchone():
            return "El usuario ya existe"
        
        #Crear el nuevo usuario
        cur.execute("INSERT INTO Usuarios (Id, Nombre, Apellido, Correo, Username, Password) VALUES (?,?,?,?,?,?)",[id, nombre, apellido, correo, username, pwd])
        con.commit()
        """ return "El Usuario ha sido creado - Proceso completado con exito" """
        return render_template("vista2.html")


#Endpoints para presentar opciones usuario una vez se ha logueado con exito

#Para seleccionar imagenes por témas de interés.
@app.route("/mi_espacio_temasinteres", methods=["POST"])
def temas_interes():
    if ("txtTemasinteres"=="Paisajes"):
        return render_template("vista4_TI_Paisajes.html")
    if ("txtTemasinteres"=="Vehículos"):
        return render_template("vista4_TI_Vehiculos.html")
    return ""

#Para buscar a otros usuarios
@app.route("/mi_espacio_otrosusuarios", methods=["POST"])
def otros_usuarios():
    return "Estamos trabajando en ello"

#Para subir una imagen
@app.route("/mi_espacio_subirimagen", methods=["POST"])
def subir_imagen():
    if 'btnSubirimagen' in request.form:
        return render_template("vista5.html") 






if __name__ == '__main__':
    app.run(debug ="TRUE")