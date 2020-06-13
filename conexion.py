import socket
import servidor_descubrimiento
import video

"""
    Funcion para comenzar la llamada a otro usuario.
    Tenemos en cuenta el usuario que somos y el usuario al que llamamos
    Consiste en:
        1.- abrir un socket TCP 
        2.- usar CALLING
        3.- Cosas que me de cuenta y no vea en el esquema del enunciado

    usuario => El usuario al que llamo.

    Return:
        - Mensaje de error si algo sale mal
        - diccionario con el nombre del usuario destino y el puerto al que quiere que le llamemos
    
    Luego en la aplicación se mostrará el mensaje de error si la liamos.
    El return esta para depurar, pero no lo coy a utilizar
"""

# FUNCION: llamar
# ARGS_IN: gui - la gui
# DESCRIPCION: Funcion para comenzar la llamada a otro usuario
# ARGS_OUT: mensaje de error o el usuario y el puerto al que llamamos

def llamar(gui):

    session_user = servidor_descubrimiento.read_session_user()
    usuario_destino = servidor_descubrimiento.read_calling_user()

    # Comprobamos los argumentos
    if (not usuario_destino['ip']) or (not usuario_destino['puerto']):
        return "[LLAMAR] Error en los parametros del usuario destino"
    
    if (not session_user['nickname']):
        return "[LLAMAR] Error en los parametro del usuario origen"

    # Construimos la peticion CALLING mi_nombre puerto udp
    peticion = "CALLING " + session_user['nickname'] + " " + str(session_user['puerto_udp_escucha']) # TODO ver si este puerto vale. Pero vamos, notificamos que escuchamos en el str(5100)
    # Nos conectamos al usuario_destino. Copiado al 100% de servidor_descubrimiento    
    address = (usuario_destino['ip'],int(usuario_destino['puerto']))

    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    my_socket.connect(address)

    #enviamos la peticion.
    my_socket.send(peticion.encode(encoding='utf-8'))

    #obtenemos la respuesta
    respuesta = my_socket.recv(2048).decode(encoding='utf-8')

    # Cerramos el socket
    my_socket.close()

    # Vemos que nos ha contestado


    respuesta_aux = respuesta.split(" ")

    if respuesta_aux[0] == "CALL_DENIED":
        gui.app.infoBox("RESPUESTA","CALL_DENIED")
        return -1
    elif respuesta_aux[0] == "CALL_BUSY":
        gui.app.infoBox("RESPUESTA","CALL_BUSY")
        return -1
    elif respuesta_aux[0] == "CALL_ACCEPTED":
        # calling_user = servidor_descubrimiento.query(respuesta_aux[1])

        usuario_destino['puerto_udp_escucha'] = int(respuesta_aux[2])

        servidor_descubrimiento.save_calling_user(usuario_destino)

        # TODO iniciar transmision de video
        my_video = video.video(gui)
        gui.cola_imagenes = my_video.cola_imagenes
        gui.video = my_video

        my_video.iniciar()
        return 1

    return (respuesta)
    
"""
    Una vez nos logueamos iniciamos un thread encargado de escuchar.
    Adivina a que funcion llama ese thread
    ...
    ...
    ...
    Si, a esta!

    return:
        - 0 Si todo va bien
        - -1 Si algo falla
"""

# FUNCION: escuchar
# ARGS_IN: gui - la gui
# DESCRIPCION: Funcion para comenzar a escuchar
# ARGS_OUT: 0 si todo OK. -1 si algo falla

def escuchar(gui):

    session_user = servidor_descubrimiento.read_session_user()

    # Comprobacion de argumentos
    if (not session_user['ip']) or (not session_user['puerto']):
        return -1

    # Volvemos a copiar de servidor_descubrimiento 
    my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


    address = (session_user['ip'], int(session_user['puerto']))
    my_socket.bind(address)

    # Supongo que solo escucharé una peticion
    my_socket.listen(1)

    conn, address = my_socket.accept()

    # El loop
    while(1):
        # Recogemos la peticion
        peticion = conn.recv(1024) # Espero que baste

        """
            Posibilidades:
                -CALLING <usuario>:
                    + Rechazamos => CALL_DENIED <nuestro nickname>
                    + Aceptamos => CALL_ACCEPTED <nuestro nickname>
                      Le buscamos
                      empezamos a transmitir video.
                
                -CALL_BUSY:
                    + informamos y a otra cosa
                
                -CALL_END:
                    + informamos y a otra cosa
                
                -CALL_DENIED:
                    + informamos y a otra cosa
        """

        peticion_aux = peticion.decode(encoding='utf-8').split(" ")


        # Caso CALLING
        if peticion_aux[0] == "CALLING":

            # Estamos recibiendo una llamada, respndemos con si o no
            acepta = gui.app.yesNoBox("LLAMADA","Aceptar la llamada de "+peticion_aux[1]+" ?")
            # Caso no acepta
            if acepta == False:
                msg = "CALL_DENIED " +session_user['nickname']

                conn.sendall(msg.encode(encoding='utf-8'))
            # Caso acepta
            else:
                calling_user = servidor_descubrimiento.query(peticion_aux[1])

                
                msg = "CALL_ACCEPTED " + session_user['nickname'] +" "+str(session_user['puerto_udp_escucha']) # TODO str(5100) = puerto UDP escucha
                calling_user['puerto_udp_escucha'] = int(peticion_aux[2])
                servidor_descubrimiento.save_calling_user(calling_user)
                conn.sendall(msg.encode(encoding='utf-8'))

                # iniciar transmision de video
                my_video = video.video(gui)
                gui.cola_imagenes = my_video.cola_imagenes
                gui.video = my_video
                my_video.iniciar()

                return 1

        # Caso CALL_BUSY
        elif peticion_aux[0] == "CALL_BUSY":
            gui.app.infoBox("LLAMADA","CALL_BUSY.")
            return 1
        
        # Caso CALL_END
        elif peticion_aux[0] == "CALL_END":
            gui.video.finalizar()
            gui.app.infoBox("LLAMADA","CALL_END.")
            return 1
        
        # Caso CALL_DENIED
        elif peticion_aux[0] == "CALL_DENIED":
            gui.app.infoBox("LLAMADA","CALL_DENIED.")
            return 1
