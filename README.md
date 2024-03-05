# Fonsek-st0263
Tópicos de telemática
David Fonseca Lara, dfonsecal@eafit.edu.co
Alvaro Ospina

# P2P: Comunicación entre procesos mediante API REST y RPC - Tópicos de telemática
Se cumplió con:
- La comunicación peer-servidor usando gRPC
- La comunicación peer-peer usando API REST
- Todas las funcionalidades propuestas por el profesor como lo fueron:
  - login(), indexar(), buscar(), logout(). De lado del servidor central
  - descargar(), enviar(). De lado de la comunicación entre peers
- Poder implementar el código de acuerdo al diagrama

# Arquitectura
![image](https://github.com/DavidFonsek/fonsek-st0263/assets/99446757/8bcedfb8-d072-4ed7-8d6a-02f8f26331a6)

# Ambiente de desarrollo
Use venv como ambiente virtual para la instalación de todas las librerías en pip, las cuales son:
![image](https://github.com/DavidFonsek/fonsek-st0263/assets/99446757/8ab5d1cc-0011-425a-8a40-a64dbd6951b1)

- Utilicé python como lenguaje de programación tanto para los peers, como para el servidor

# Videos del código funcionando
Funcionalidades: https://youtu.be/N6b4hjSKQBM
Después de la dockerización: https://youtu.be/CXO2kt3wlmk

# Referencias
- https://docs.python.org/3/library/threading.html
- https://protobuf.dev/programming-guides/proto3/
- https://grpc.io/docs/
- https://www.docker.com/blog/how-to-dockerize-your-python-applications/
- https://www.cloudbees.com/blog/using-docker-compose-for-python-development

