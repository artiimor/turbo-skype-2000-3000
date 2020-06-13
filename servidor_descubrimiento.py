import socket
import sys
import json

address = ("vega.ii.uam.es",8000)

ip = "192.168.1.99"
puerto_udp_escucha = 5100

# FUNCION: establecer_conexion
# ARGS_IN: 
# DESCRIPCION: comienza la conexion con el server vega.ii.uam.es
# ARGS_OUT: 

def establecer_conexion():
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    my_socket.connect(address)

    return my_socket

"""
    El servidor de descubrimiento soporta los siguientes mensajes:

    -REGISTER:
        Registra a un usuario

        retorno:
            -OK WELCOME nick ts
            -NOK WRONG_PASS

    -QUERY:
        Obtiene la IP y Puerto dado un nick

        retorno:
            -OK USER_FOUND nick ip_adress port protocols
            -NOK USER_UNKNOWN

    -LIST_USERS:
        Te da todos los usuarios

        retorno:
            -OK USERS_LIST user1#user2...
            -NOK USER_UNKNOWN

    -QUIT:
        Se cierra la conexión con el servidor

        retorno:
            -BYE
"""
# FUNCION: register
# ARGS_IN: nickname - nombre del usuario
#          puerto - puerto del usuario
#          password - password del usuario
#          protocolo - protocolo introducido
# DESCRIPCION: registra al usuario en el server vega.ii.uam.es
# ARGS_OUT: 0 si todo OK. -1 si falla algo

def register (nickname, puerto, password, protocolo):

    # Control de parametros
    if ((not nickname) or (not puerto) or (not password) or (not protocolo)):
        return -1

    # Primero nos conectamos
    my_socket = establecer_conexion()

    # Creamos la peticion
    peticion = "REGISTER " + nickname + " " + ip + " " + str(puerto) + " " + password + " " + protocolo
    # La enviamos
    my_socket.send(peticion.encode(encoding='utf-8'))

    # Si todo ha ido bien
    respuesta = my_socket.recv(2048) # Esperemos que 2048 sea suficiente

    if respuesta.decode(encoding='utf-8') == "NOK UNKNOWN_COMMAND":
        return -1
    else:
        session_user = {}
        session_user['nickname'] = nickname
        session_user['ip'] = ip
        session_user['puerto'] = puerto
        session_user['protocolo'] = protocolo
        session_user['puerto_udp_escucha'] = puerto_udp_escucha # Escuchamos en el puerto 5100
        save_session_user(session_user)
        return 0
    
    return -1

# FUNCION: query
# ARGS_IN: nickname - nombre del usuario a buscar
# DESCRIPCION: busca al usuario
# ARGS_OUT: los datos del usuario

def query (nickname):

    # Control de parametros
    if ((not nickname)):
        return -1

    # Primero nos conectamos
    my_socket = establecer_conexion()

    # Creamos la peticion
    peticion = "QUERY " + nickname

    # La enviamos
    my_socket.send(peticion.encode(encoding='utf-8'))

    # Si todo ha ido bien
    respuesta = my_socket.recv(2048) # Esperemos que 2048 sea suficiente

    if respuesta.decode(encoding='utf-8') == "NOK UNKNOWN_COMMAND":
        return -1
    else:
        # spliteamos la respuesta
        datos = respuesta.decode(encoding='utf-8').split()
        nick = datos[2]
        ip = datos[3]
        puerto = str(datos[4])
        protocolos = datos[5]

        # Lo devolvemos en un diccionario
        dict = {}
        
        dict["nickname"] = nick
        dict["ip"] = ip
        dict["puerto"] = puerto
        dict["protocolos"] = protocolos 

        return dict
    
    return -1

# FUNCION: list_users
# ARGS_IN:
# DESCRIPCION: lista a los usuarios
# ARGS_OUT: la lista de usuarios

def list_users():

    # Control de parametros

    # Primero nos conectamos
    my_socket = establecer_conexion()

    # Creamos la peticion
    peticion = "LIST_USERS"

    # La enviamos
    my_socket.send(peticion.encode(encoding='utf-8'))

    # Si todo ha ido bien
    respuesta = my_socket.recv(2048) # Esperemos que 2048 sea suficiente

    if respuesta.decode(encoding='utf-8') == "NOK USER_UNKNOWN":
        return -1
    else:
        # spliteamos la respuesta
        datos = respuesta.decode(encoding='utf-8').split("#") # Esta separado por "#"
        
        # Lo devolvemos en una lista
        list = []
        for i in datos:
            list.append(i)
        
        return list
    
    return -1

# FUNCION: quit
# ARGS_IN:
# DESCRIPCION: envia QUIT
# ARGS_OUT: 0

def quit():

    # Control de parametros

    # Primero nos conectamos
    my_socket = establecer_conexion()

    # Creamos la peticion
    peticion = "QUIT"

    # La enviamos
    my_socket.send(peticion.encode(encoding='utf-8'))

    # Si todo ha ido bien
    respuesta = my_socket.recv(2048) # Esperemos que 2048 sea suficiente

    # Cerramos el socket
    my_socket.close()
    
    return 0

"""
    Guarda la informacion del usuario de la session.
    Lo que había lo sobreescribe
"""

# FUNCION: save_session_user
# ARGS_IN: session_user - El usuario a guardar
# DESCRIPCION: Guarda la informacion del usuario de la session
# ARGS_OUT:

def save_session_user(session_user):
    if (session_user is None):
        print("ERROR, no se ha introducido session_user")
        return -1
    with open('files/session_user.txt', 'w+') as my_file:
        json.dump(session_user, my_file)

"""
    Guarda la informacion del usuario al que llamamos/nos llama.
    Lo que había lo sobreescribe
"""
# FUNCION: save_calling_user
# ARGS_IN: calling_user - El usuario a guardar
# DESCRIPCION: Guarda la informacion del usuario al que llama
# ARGS_OUT:

def save_calling_user(calling_user):
    if (calling_user is None):
        print("ERROR, no se ha introducido session_user")
        return -1
    with open('files/calling_user.txt', 'w+') as my_file:
        json.dump(calling_user, my_file)

"""
    Obtiene la informacion del session_user leyendolo del Json
"""

# FUNCION: read_session_user
# ARGS_IN:
# DESCRIPCION: Obtiene la informacion del usuario de la sesion
# ARGS_OUT: el usuario

def read_session_user():
    with open('files/session_user.txt') as json_file:
        session_user = json.load(json_file)
        return session_user

"""
    Obtiene la informacion del calling_user leyendolo del Json
"""

# FUNCION: read_calling_user
# ARGS_IN:
# DESCRIPCION: Obtiene la informacion del usuario al que llamamos
# ARGS_OUT: el usuario

def read_calling_user():
    with open('files/calling_user.txt') as json_file:
        calling_user = json.load(json_file)
        return calling_user