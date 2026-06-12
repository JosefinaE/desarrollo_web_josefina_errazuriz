import json
import os
import uuid

from flask import (
    Flask,
    flash,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    send_from_directory,
    url_for,
)
from sqlalchemy import create_engine, func, select
from sqlalchemy.orm import Session, selectinload
from werkzeug.utils import secure_filename

from models import Actividad, Comentario, Comuna, Foto, Miembro, Region
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

                ruta_relativa = os.path.join(
                    CARPETA_FOTOS, nombre_final
                )  # relativo a root de proyecto
                nueva_foto = Foto(
                    actividad_id=act.id,
                    ruta_archivo=ruta_relativa,
                    nombre_archivo=nombre_seguro,
                )
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
        "miembros/miembros.html", miembros=miembros, map_tipo_miembro=map_tipo_miembro
    )


@app.route("/estadisticas")
def estadisticas():
    grafo1 = url_for(
        "static", filename="img/gatoingeniero.jpg"
    )  # cambiar por url a imagen de verdad
    grafo2 = url_for(
        "static", filename="img/grafo2.png"
    )  # cambiar por url a imagen de verdad
    return render_template(
        "estadisticas/estadisticas.html", grafo1=grafo1, grafo2=grafo2
    )


@app.route("/show_photo")
def show_photo():
    ruta = request.args.get("ruta", "").strip()

    if not ruta:
        flash("foto no especificada", "error")
        return redirect(url_for("home"))

    session = getSession()
    foto = session.scalar(select(Foto).where(Foto.ruta_archivo == ruta))
    if not foto:
        flash("La foto no existe en la base de datos.", "error")
        return redirect(url_for("home"))

    ruta_os = os.path.join(app.root_path, foto.ruta_archivo)
    nombre_archivo = os.path.basename(foto.ruta_archivo)
    carpeta = os.path.dirname(ruta_os)

    if not os.path.isfile(ruta_os):
        flash(f"Foto {ruta} no existe.", "error")
        return redirect(url_for("home"))

    return send_from_directory(carpeta, nombre_archivo)


# --------------------- API -----------------------
@app.route("/api/actividades/tipos")
def actividades_por_tipo():
    session = getSession()
    result = (
        session.query(Actividad.tipo, func.count(Actividad.id))
        .group_by(Actividad.tipo)
        .all()
    )
    session.close()
    data = [{"tipo": tipo, "total": total} for tipo, total in result]
    return jsonify(data)


@app.route("/api/miembros/por-dia")
def miembros_por_dia_route():
    session = getSession()
    result = (
        session.query(func.date(Miembro.fecha_registro), func.count(Miembro.id))
        .group_by(func.date(Miembro.fecha_registro))
        .order_by(func.date(Miembro.fecha_registro))
        .all()
    )
    session.close()
    result = [{"dia": str(dia), "total": total} for dia, total in result]
    return jsonify(result)


@app.route("/api/actividades/comunas")
def actividades_comunas():
    session = getSession()
    result = (
        session.query(Comuna.nombre, func.count(Actividad.id))
        .select_from(Actividad)
        .join(Miembro)
        .join(Miembro.comuna)
        .group_by(Comuna.nombre)
        .all()
    )

    session.close()
    result = [{"comuna": comuna, "total": total} for comuna, total in result]
    print(result)
    return jsonify(result)


# -------------------------- COMENTARIOS
@app.route("/comentarios/table/<int:actividad_id>")
def comentarios_table(actividad_id):
    session = getSession()
    stmt = (
        select(Actividad)
        .where(Actividad.id == actividad_id)
        .options(selectinload(Actividad.comentarios))
    )
    act = session.scalars(stmt).one_or_none()
    return render_template("miembros/_comentarios_table.html", act=act)


@app.route("/comentarios/form_comentarios", methods=["GET"])
def form_comentarios():
    actividad_id = request.args.get("actividad_id")
    return render_template("miembros/_form_comentarios.html", actividad_id=actividad_id)


@app.route("/comentarios/create", methods=["POST"])
def create_comentario():
    nombre = request.form.get("nombre")
    texto = request.form.get("texto")
    actividad_id = request.form.get("actividad_id")
    errors = []
    if not nombre:
        errors.append("Nombre requerido")
    if not texto:
        errors.append("Texto requerido")
    if not actividad_id:
        errors.append("Actividad inválida")
    if errors:
        return render_template("miembros/_comentario_error.html", errors=errors), 200
    try:
        comentario = Comentario(
            nombre=nombre, texto=texto, actividad_id=int(actividad_id)
        )
        session = getSession()
        session.add(comentario)
        session.commit()
    except Exception as e:
        return render_template("miembros/_comentario_error.html", errors=[str(e)]), 200

    # trigger from here, not frontend
    response = make_response("", 200)
    response.headers["HX-Trigger"] = json.dumps({
        f"commentSaved-{actividad_id}": True
    })
    return response
# _-------------------------------------------------
if __name__ == "__main__":
    upload_dir = os.path.join(app.root_path, CARPETA_FOTOS)
    os.makedirs(upload_dir, exist_ok=True)
    app.run()
