import re

from models import DEPTOS, TIPO_MIEMBRO


def validar_miembro(data, id_comunas):
    nombre = data.get("nombre")
    email = data.get("email")
    fono = data.get("fono")
    tipo = data.get("tipo")
    depto = data.get("depto")
    id_comuna = int(data.get("id_comuna"))
    
    fono = fono.replace(" ", "").replace("+","")

    valid_name = 3 <= len(nombre.strip()) < 200
    valid_fono = 7 <= len(fono) <= 15

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
        [valid_fono,"Teléfono inválido (entre 7 y 14 digitos)"],
        [valid_tipos, "Debe seleccionar el tipo de miembro"],
        [valid_depto, "Debe seleccionar un deptartamento"],
        [valid_comuna, "Debe seleccionar una comuna"],
    ]
    return v
