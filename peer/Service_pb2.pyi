from google.protobuf.internal import containers as _containers
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class Credenciales(_message.Message):
    __slots__ = ("usuarioPeer", "contraPeer", "nombrePeer", "puerto", "hostname")
    USUARIOPEER_FIELD_NUMBER: _ClassVar[int]
    CONTRAPEER_FIELD_NUMBER: _ClassVar[int]
    NOMBREPEER_FIELD_NUMBER: _ClassVar[int]
    PUERTO_FIELD_NUMBER: _ClassVar[int]
    HOSTNAME_FIELD_NUMBER: _ClassVar[int]
    usuarioPeer: str
    contraPeer: str
    nombrePeer: str
    puerto: int
    hostname: str
    def __init__(self, usuarioPeer: _Optional[str] = ..., contraPeer: _Optional[str] = ..., nombrePeer: _Optional[str] = ..., puerto: _Optional[int] = ..., hostname: _Optional[str] = ...) -> None: ...

class Confirmacion(_message.Message):
    __slots__ = ("respuesta",)
    RESPUESTA_FIELD_NUMBER: _ClassVar[int]
    respuesta: str
    def __init__(self, respuesta: _Optional[str] = ...) -> None: ...

class ArchivosPeer(_message.Message):
    __slots__ = ("archivos", "nombrePeer")
    ARCHIVOS_FIELD_NUMBER: _ClassVar[int]
    NOMBREPEER_FIELD_NUMBER: _ClassVar[int]
    archivos: _containers.RepeatedScalarFieldContainer[str]
    nombrePeer: str
    def __init__(self, archivos: _Optional[_Iterable[str]] = ..., nombrePeer: _Optional[str] = ...) -> None: ...

class Solicitud(_message.Message):
    __slots__ = ("peticion", "nombrePeer")
    PETICION_FIELD_NUMBER: _ClassVar[int]
    NOMBREPEER_FIELD_NUMBER: _ClassVar[int]
    peticion: str
    nombrePeer: str
    def __init__(self, peticion: _Optional[str] = ..., nombrePeer: _Optional[str] = ...) -> None: ...

class SolicitudBusqueda(_message.Message):
    __slots__ = ("peticion", "nombreArchivo")
    PETICION_FIELD_NUMBER: _ClassVar[int]
    NOMBREARCHIVO_FIELD_NUMBER: _ClassVar[int]
    peticion: str
    nombreArchivo: str
    def __init__(self, peticion: _Optional[str] = ..., nombreArchivo: _Optional[str] = ...) -> None: ...

class PeerPosesor(_message.Message):
    __slots__ = ("peer", "puerto", "host_name")
    PEER_FIELD_NUMBER: _ClassVar[int]
    PUERTO_FIELD_NUMBER: _ClassVar[int]
    HOST_NAME_FIELD_NUMBER: _ClassVar[int]
    peer: str
    puerto: int
    host_name: str
    def __init__(self, peer: _Optional[str] = ..., puerto: _Optional[int] = ..., host_name: _Optional[str] = ...) -> None: ...
