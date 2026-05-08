from flask import Flask, render_template, request, flash, redirect, url_for
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Actividad, Comuna, Foto, Miembro, Region
from validators import validar_miembro

app = Flask(__name__, template_folder="./templates", static_folder="./static")
app.config["SECRET_KEY"] = "ñkdalksdo0akoriqworkdaslmlkadpñ"

def getSession():
    connection_string = "mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2"
    engine = create_engine(connection_string, echo=True)
    return Session(engine)


@app.route("/")
def home():
    session = getSession()
    last_5_miembros = session.scalars(select(Miembro).order_by(Miembro.fecha_registro.desc()).limit(5))
    return render_template("index.html", miembros=last_5_miembros)


@app.route("/register", methods=['POST', 'GET'])
def registrar_miembro():

    session = getSession()
    comunas = session.scalars(select(Comuna).order_by(Comuna.nombre))
    if request.method == 'POST':
        data = request.form
        id_comunas = [c.id for c in comunas]
        valid_messages = validar_miembro(data, id_comunas)

        ret = False
        for valid, msg in valid_messages:
            if not valid:
                flash(msg, 'error')
                ret = True
        if ret:
            return redirect(url_for('registrar_miembro'))
        # Insert into db
        new_miembro = Miembro(
            nombre = data.get("nombre"),
            email = data.get("email"),
            telefono = data.get("fono"),
            tipo = data.get("tipo"),
            departamento = data.get("depto"),
            comuna_id = data.get("id_comuna")
        )
        try:
            session.add(new_miembro)
            session.commit()
        except Exception as e:
            flash(f"Error al registrar miembro {e}", 'error')
            session.rollback()
    return render_template("registro.html", comunas=comunas)


@app.route("/")
def registrar_actividad():
    return render_template("actividades.html")


@app.route("/")
def listado_miembros():
    return render_template("miembros.html")

@app.route("/")
def estadisticas():
    return render_template("estadisticas.html")



if __name__ == "__main__":
    # Run the app in debug mode for easier development
    app.run(debug=True)
