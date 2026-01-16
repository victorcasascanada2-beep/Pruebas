# usuarios.py
# Aquí puedes añadir más mecánicos fácilmente en el futuro
VENDEDORES = {
    "V1": {"nombre": "Víctor", "id": "001"},
    "M1": {"nombre": "Mecánico Taller 1", "id": "002"},
}

def validar_usuario(codigo):
    return VENDEDORES.get(codigo.upper(), None)
