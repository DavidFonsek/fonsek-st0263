import os

# Archivo de configuración
NOMBRE = 'peer1'
HOST_GRPC = os.environ.get("HOST_GRPC", 'localhost:8080')
HOST_FLASK_PROPIO = 8081
HOST_FLASK_VISITANTE = 8000
HOST_PEER = ''
ARCHIVO_BUSQUEDA = ''

# Banderas
BANDERA = True
BANDERA_LOGIN = False

# "Base de datos"
LISTA_ARCHIVOS = ["archivo1.txt", "archivo2.txt", "archivo3.txt"]
