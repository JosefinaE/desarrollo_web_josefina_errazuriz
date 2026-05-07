from flask import Flask, render_template, request
from sqlalchemy import select
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from models import Actividad, Comuna, Foto, Miembro, Region

app = Flask(__name__, template_folder="./templates", static_folder="./static")


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
    if request.method == 'POST':
        form = request.form
        print(form.get("nombre"))
    return render_template("registro.html")


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
