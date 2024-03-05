import importlib
import threading
import sys
import requests
from flask import Flask, jsonify, request

import grpc
import Service_pb2
import Service_pb2_grpc

import signal
import os

# Inicialización y configuración de Flask
app = Flask(__name__)


@app.route('/', methods=['POST'])
def recibir_mensaje():
    data = request.get_json()
    nombre_archivo = data.get('nombre_archivo')

    if data and data.get('mensaje') == "descargar" and nombre_archivo in config.LISTA_ARCHIVOS:
        respuesta = {"mensaje": f"El archivo '{nombre_archivo}' lo tengo y te he enviado el archivo :D", "archivo": nombre_archivo}
    elif data and data.get('mensaje') == "descargar":
        respuesta = {"mensaje": f"El archivo '{nombre_archivo}' no existe en mi lista de archivos D:"}
    else:
        respuesta = {"mensaje": "Mensaje no reconocido."}

    return jsonify(respuesta), 200


def descargar(config, nombre_archivo):
    if config.HOST_FLASK_VISITANTE == 8000:
        print("No puedes pedir el archivo, porque no sabes quien lo tiene")
    elif str(config.ARCHIVO_BUSQUEDA) == str(nombre_archivo):
        url = f"http://{config.HOST_PEER}:{config.HOST_FLASK_VISITANTE}/"
        mensaje = {"mensaje": "descargar", "nombre_archivo": nombre_archivo}
        response = requests.post(url, json=mensaje)

        if response.status_code == 200:
            print(f"Respuesta recibida del peer ({config.HOST_FLASK_VISITANTE}):", response.json().get('mensaje'))
            config.LISTA_ARCHIVOS.append(str(response.json().get('archivo')))
            print(f"Tus archivos {config.LISTA_ARCHIVOS}")
        else:
            print("Error al comunicarse con el peer")
    else:
        print("Ese no es el archivo que buscaste!")


def iniciar_servidor_flask(config):
    app.run(host='127.0.0.1', port=config.HOST_FLASK_PROPIO, debug=False, threaded=True)


def parsear_mensaje(mensaje: str):
    mensaje_parseado = mensaje.split()

    return mensaje_parseado


def logout(stub, config):
    if config.BANDERA_LOGIN:  # Asegúrate de que haya un nombre de usuario para hacer logout
        try:
            response_logout = stub.Logout(Service_pb2.Solicitud(peticion="logout", nombrePeer=config.NOMBRE))
            print(response_logout.respuesta)
        except grpc.RpcError as e:
            print(f"Error al hacer logout: {e}")


def signal_handler(sig, frame):
    print('Recibido Ctrl+C! Haciendo logout antes de salir...')
    channel = grpc.insecure_channel(config.HOST_GRPC)
    stub = Service_pb2_grpc.PrincipalStub(channel)
    logout(stub, config)
    sys.exit(0)


def run(config):

    while config.BANDERA:
        channel = grpc.insecure_channel(config.HOST_GRPC)
        stub = Service_pb2_grpc.PrincipalStub(channel)

        entrada = input()
        entrada_parseada = parsear_mensaje(entrada)

        # Después del login
        if config.BANDERA_LOGIN:
            if entrada_parseada[0] == "logout" and len(entrada_parseada) == 1:
                response_logout = stub.Logout(Service_pb2.Solicitud(peticion=entrada_parseada[0], nombrePeer=config.NOMBRE))
                print(response_logout.respuesta)
                config.BANDERA = False

            elif entrada_parseada[0] == "indexar" and len(entrada_parseada) == 1:
                response_indexar = stub.Indexar(Service_pb2.ArchivosPeer(archivos=config.LISTA_ARCHIVOS, nombrePeer=config.NOMBRE))
                print(response_indexar.respuesta)

            elif entrada_parseada[0] == "buscar" and len(entrada_parseada) == 2:
                response_buscar = stub.Buscar(Service_pb2.SolicitudBusqueda(peticion=entrada_parseada[0], nombreArchivo=entrada_parseada[1]))
                print(response_buscar.peer)

                if "El Archivo lo tiene" in response_buscar.peer:
                    config.HOST_FLASK_VISITANTE = response_buscar.puerto
                    config.HOST_PEER = response_buscar.host_name
                    config.ARCHIVO_BUSQUEDA = entrada_parseada[1]
                    print(f"El puerto del peer es: {config.HOST_FLASK_VISITANTE}")

            elif entrada_parseada[0] == "crear" and len(entrada_parseada) == 2:
                config.LISTA_ARCHIVOS.append(entrada_parseada[1])
                print("Archivo creado con éxito")
                print("Tus archivos: ", config.LISTA_ARCHIVOS)

            # funciones de flask
            elif entrada_parseada[0] == "descargar" and len(entrada_parseada) == 2:
                descargar(config, entrada_parseada[1])

            else:
                print("Comando desconocido")

        # login
        if entrada_parseada[0] == "login" and len(entrada_parseada) == 3:
            if config.BANDERA_LOGIN:
                print("O ya estás loggeado :)")
            else:
                response_login = stub.Login(Service_pb2.Credenciales(usuarioPeer=entrada_parseada[1],
                                                                     contraPeer=entrada_parseada[2],
                                                                     nombrePeer=config.NOMBRE,
                                                                     puerto=config.HOST_FLASK_PROPIO,
                                                                     hostname=os.environ.get('HOST_NAME', 'localhost')))
                print(response_login.respuesta)
                config.BANDERA_LOGIN = True
        elif not config.BANDERA_LOGIN:
            print("Todavía no haz hecho login. Para poder realizarlo escribe: login + tu_usuario + tu contraseña. Separados de un espacio")


if __name__ == '__main__':

    # Argumentos
    if len(sys.argv) != 2:
        print("Usage: python peer.py <config_module_name>")
        sys.exit(1)

    config_module_name = sys.argv[1]
    config = importlib.import_module(config_module_name)

    # Ctrl + c
    signal.signal(signal.SIGINT, signal_handler)

    # Hilos
    flask_thread = threading.Thread(target=iniciar_servidor_flask, args=(config,))
    flask_thread.daemon = True
    flask_thread.start()

    # Correr el cliente
    run(config)
