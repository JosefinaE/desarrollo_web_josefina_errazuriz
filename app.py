import os
import uuid

from flask import Flask, flash, redirect, render_template, request, url_for
from sqlalchemy import create_engine, select
from sqlalchemy.orm import Session
from werkzeug.utils import secure_filename

from models import Actividad, Comuna, Foto, Miembro, Region
from validators import validar_actividad, validar_miembro

app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.config["SECRET_KEY"] = "ñkdalksdo0akoriqworkdaslmlkadpñ"

map_tipo_miembro = {
    "estudiante_pre": "Estudiante Pregrado",
    "estudiante_post": "Estudiante Postgrado",
    "funcionario": "Funcionario",
    "academico": "Academico",
}

CARPETA_FOTOS = "images"

def getSession():
    connection_string = "mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2"
    engine = create_engine(connection_string, echo=True)
    return Session(engine)


@app.route("/")
def home():
    session = getSession()
    last_5_miembros = session.scalars(
        select(Miembro).order_by(Miembro.fecha_registro.desc()).limit(5)
    )
    return render_template(
        "index.html", miembros=last_5_miembros, map_tipo_miembro=map_tipo_miembro
    )


@app.route("/register", methods=["POST", "GET"])
def registrar_miembro():

    session = getSession()
    comunas = session.scalars(select(Comuna).order_by(Comuna.nombre)).all()
    if request.method == "POST":
        data = request.form
        id_comunas = [c.id for c in comunas]
        valid_messages = validar_miembro(data, id_comunas)

        ret = False
        for valid, msg in valid_messages:
            if not valid:
                flash(msg, "error")
                ret = True
        if ret:
            return redirect(url_for("registrar_miembro"))
        # Insert into db
        if data.get("tipo") == "funcionario":
            depto = None
        else:
            depto = data.get("depto")
        fono = data.get("fono").replace(" ", "").replace("+", "")

        new_miembro = Miembro(
            nombre=data.get("nombre"),
            email=data.get("email"),
            telefono=fono,
            tipo=data.get("tipo"),
            departamento=depto,
            comuna_id=data.get("id_comuna"),
        )
        try:
            session.add(new_miembro)
            session.commit()
            flash("Se ha registrado un nuevo miembro!", "info")
            return redirect(url_for("home"))
        except Exception as e:
            flash(f"Error al registrar miembro {e}", "error")
            session.rollback()
    return render_template("registro.html", comunas=comunas)


@app.route("/registrar_actividad", methods=["GET", "POST"])
def registrar_actividad():
    session = getSession()
    miembros = session.scalars(select(Miembro).order_by(Miembro.fecha_registro.desc()))
    if request.method == "POST":
        data = request.form
        id_miembros = [m.id for m in miembros]
        archivos = request.files.getlist("archivos")

        valid_messages = validar_actividad(data, id_miembros, archivos)

        ret = False
        for valid, msg in valid_messages:
            if not valid:
                flash(msg, "error")
                ret = True
        if ret:
            return redirect(url_for("registrar_miembro"))
        # insert en db
        archivos_guardados = []
        try:
            act = Actividad(
                miembro_id=data.get("miembro_id"),
                dia=data.get("dia"),
                hora_inicio=data.get("hora_inicio"),
                duracion=data.get("duracion"),
                tipo=data.get("tipo"),
                nombre=data.get("nombre").strip(),
                descripcion=data.get("descripcion").strip() or None,
            )

            session.add(act)
            session.flush()  # 'simula' agregar, sin commit
            
            for archivo in archivos:
                if archivo.filename == "":
                    continue

                nombre_seguro = secure_filename(archivo.filename)  # sanitizar input
                extension = os.path.splitext(nombre_seguro)[1].lower()

                nombre_final = f"{uuid.uuid4().hex}{extension}"  # renombrar a uuid
                
                upload_dir = os.path.join(app.root_path, CARPETA_FOTOS)
                ruta_archivo = os.path.join(upload_dir, nombre_final)
                archivo.save(ruta_archivo)
                archivos_guardados.append(ruta_archivo)

                ruta_relativa = os.path.join(CARPETA_FOTOS, nombre_final) # relativo a root de proyecto
                nueva_foto = Foto(actividad_id=act.id, ruta_archivo=ruta_relativa, nombre_archivo=nombre_seguro)
                session.add(nueva_foto)

            session.commit()
            flash("Actividad registrada correctamente", "info")
            return redirect(url_for("home"))

        except Exception as e:
            session.rollback()
            flash(f"Error al registrar actividad: {e}", "error")
            return render_template("actividades.html", miembros=miembros)

    return render_template("actividades.html", miembros=miembros)


@app.route("/listado_miembros")
def listado_miembros():
    session = getSession()
    miembros = session.scalars(select(Miembro).order_by(Miembro.nombre)).all()

    return render_template(
        "miembros.html", miembros=miembros, map_tipo_miembro=map_tipo_miembro
    )


@app.route("/estadisticas")
def estadisticas():
    return render_template("estadisticas.html")


if __name__ == "__main__":
    # Run the app in debug mode for easier development
    upload_dir = os.path.join(app.root_path, CARPETA_FOTOS)
    os.makedirs(upload_dir, exist_ok=True) 
    app.run(debug=True)
