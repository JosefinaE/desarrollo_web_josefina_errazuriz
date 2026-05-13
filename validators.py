import re
import time

from models import DEPTOS, DIAS, TIPO_MIEMBRO, TIPOS


def validar_miembro(data, id_comunas):
    nombre = data.get("nombre")
    email = data.get("email")
    fono = data.get("fono")
    tipo = data.get("tipo")
    depto = data.get("depto")
    id_comuna = int(data.get("id_comuna"))

    fono = fono.replace(" ", "").replace("+", "")
    valid_name = 3 <= len(nombre.strip()) < 200
    valid_fono = 7 <= len(fono) <= 15 
    try:
        int(fono)
    except Exception:
        valid_fono = False

    email_re = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    valid_email = re.fullmatch(email_re, email) is not None

    valid_tipos = tipo in TIPO_MIEMBRO
    if tipo != "funcionario":
        valid_depto = depto in DEPTOS
    else:
        valid_depto = depto == "" or depto is None

    valid_comuna = id_comuna in id_comunas

    v = [
        [valid_name, "Nombre inválido (mínimo 3 caracteres)"],
        [valid_email, "Email inválido"],
        [valid_fono, "Teléfono inválido (entre 7 y 14 digitos)"],
        [valid_tipos, "Debe seleccionar el tipo de miembro"],
        [valid_depto, "Debe seleccionar un deptartamento"],
        [valid_comuna, "Debe seleccionar una comuna"],
    ]
    return v


# Source - https://stackoverflow.com/a/1322524
# Posted by Nadia Alramli
# Retrieved 2026-05-12, License - CC BY-SA 2.5
# (gracias python por tener una libreria de datetime buena)
def isTimeFormat(input):
    try:
        time.strptime(input, "%H:%M")
        return True
    except ValueError:
        return False


def validar_actividad(data, id_miembros, files):
    miembro_id = data.get("miembro_id")
    dia = data.get("dia")
    hora_inicio = data.get("hora_inicio")
    duracion = data.get("duracion")
    tipo = data.get("tipo")
    nombre = data.get("nombre")
    descripcion = data.get("descripcion", "").strip()

    try:
        miembro_id = int(miembro_id)
    except Exception as e:
        miembro_id = -1  # así seguimos validando otras cosas

    valid_miembro = miembro_id in id_miembros
    valid_dia = dia in DIAS
    valid_tipo = tipo in TIPOS

    nombre = nombre.strip() if nombre else ""
    valid_nombre = 3 <= len(nombre) <= 45

    valid_descripcion = len(descripcion) <= 500

    valid_hora_inicio = isTimeFormat(hora_inicio)
    valid_duracion = isTimeFormat(duracion)

    valid_files = len(files) > 0
    # referencia: https://www.geeksforgeeks.org/python/find-the-mime-type-of-a-file-in-python/
    for file in files:
        if file.filename == "":
            continue
        mime = file.mimetype.lower()
        if not mime.startswith("image/"):
            valid_files = False
            break

    v = [
        [valid_miembro, "Debe seleccionar un miembro válido"],
        [valid_dia, "Debe seleccionar un día válido"],
        [valid_hora_inicio, "Hora de inicio inválida"],
        [valid_duracion, "Duración inválida"],
        [valid_tipo, "Debe seleccionar un tipo válido"],
        [valid_nombre, "Nombre inválido (3 a 45 caracteres)"],
        [valid_descripcion, "Descripción inválida (máximo 500 caracteres)"],
        [valid_files, "Archivos inválidos (solo imágenes)"],
    ]

    return v
