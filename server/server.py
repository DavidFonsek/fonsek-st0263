from concurrent import futures

import re
import grpc
import Service_pb2
import Service_pb2_grpc
from Service_pb2 import Credenciales

HOST = '[::]:8080'


def parsear_mensaje(mensaje, posicion):
    mensaje_dividido = str(mensaje).split()
    mensaje_parseado = mensaje_dividido[int(posicion)].strip("'\"")

    return mensaje_parseado


def parsear_lista(texto):
    nombres_archivos = re.findall(r'archivos: "(.*?)"', texto)

    return nombres_archivos


# "Base de datos"
base_datos = {}
peer_puerto = {}
peer_host = {}


class PrincipalService(Service_pb2_grpc.PrincipalServicer):

    def Login(self, request: Credenciales, context: grpc.ServicerContext):
        print("Recibido del cliente: " + str(request))
        usuario_peer = request.usuarioPeer
        nombre_peer = request.nombrePeer
        puerto = request.puerto
        host_peer = request.hostname
        base_datos[nombre_peer] = ''
        peer_puerto[nombre_peer] = puerto
        peer_host[nombre_peer] = host_peer
        print(f"{nombre_peer} ha sido añadido a la base de datos.")
        print("Base de datos: ", base_datos)
        print("Relaciones ", f'{host_peer}:{puerto}')

        return Service_pb2.Confirmacion(respuesta=f"{usuario_peer} ha sido añadido a la base de datos.")

    def Logout(self, request, context):
        print("Recibido del cliente: " + str(request))
        nombre_peer = parsear_mensaje(request, -1)

        if nombre_peer in base_datos:
            del base_datos[nombre_peer]
            print(f"{nombre_peer} ha sido eliminado de la base de datos.")

        print("Base de datos: ", base_datos)

        return Service_pb2.Confirmacion(respuesta="Adiós logout realizado con éxito")

    def Indexar(self, request, context):
        print("Archivos recibidos del cliente: " + str(request))
        archivos = parsear_lista(str(request))
        nombre_peer = parsear_mensaje(request, -1)
        base_datos[nombre_peer] = archivos
        print("Base de datos: ", base_datos)

        return Service_pb2.Confirmacion(respuesta="He recibido tus archivos con éxito")

    def Buscar(self, request, context):
        print("Archivo solicitado por el cliente: " + str(request))
        archivo_a_buscar = parsear_mensaje(request, -1)

        peer_posesor = ''

        for clave, arreglo in base_datos.items():
            if archivo_a_buscar in arreglo:
                peer_posesor = str(clave)

        if peer_posesor == '':
            return Service_pb2.PeerPosesor(peer="Ningún peer tiene ese archivo")
        else:
            puerto = int(peer_puerto[peer_posesor])
            host = peer_host[peer_posesor]
            return Service_pb2.PeerPosesor(peer=f"El Archivo lo tiene: {peer_posesor}", host_name=host, puerto=puerto)


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=4))
    Service_pb2_grpc.add_PrincipalServicer_to_server(PrincipalService(), server)
    server.add_insecure_port(HOST)
    print("El servidor está corriendo... ")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
