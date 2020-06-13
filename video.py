from appJar import gui
import threading
import servidor_descubrimiento
import queue
import socket
import cv2
import numpy as np
from PIL import Image, ImageTk
import time 
from threading import Lock

"""
    Clase encargada de hacer cosas de video.

    Entre sus funcionalidades se encuentran:
        1.- establecer conexion UDP
        2.- Enviar video
        3.- Recibir video
        4.- Finalizar la llamada/emision y recepcion de video
"""

class video():
    def __init__(self, gui, puerto_udp_envia = 0): # Por defecto le pongo el puerto 6000. Comprobar
        """
            Procedimiento para inicializar

            1.- Guardamos los puertos en los que escuchamos, recibimos info
            2.- Creamos una cola to guapa para enviar
            3.- Creamos el socket para enviar (El otro hará lo mismo)
        """

        self.gui = gui.app
        self.session_user = servidor_descubrimiento.read_session_user()
        self.calling_user = servidor_descubrimiento.read_calling_user()

        self.puerto_udp_envia = puerto_udp_envia

        while puerto_udp_envia < 65535:
            try:
                self.socket_in.bind(('0.0.0.0', puerto_udp_envia))
                self.puerto_udp_envia = puerto_udp_envia
                break
            except:
                puerto_udp_envia += 1

        self.frame_count = 0
        self.gui.startSubWindow("Video")
        # self.gui.setGeometry(800,520)

        msg = "Redes2 - P2P - " + self.session_user['nickname'] + "Recibiendo info de "+self.calling_user['nickname']
        self.gui.addLabel("subtitle", msg)

        # Imagen en la que se van a mostrar el video de nuestra camara y el del otro usuario
        self.gui.addImage("imagen_stream", "imgs/webcam.gif")

        self.frame = cv2.VideoCapture(0)
        self.gui.setPollTime(20)

        self.cola_imagenes = queue.Queue()

        self.gui.cola_imagenes = self.cola_imagenes

        self.gui.addButtons(["colgar"],self.buttonsCallback)

    # FUNCION: iniciar
	# ARGS_IN: self
	# DESCRIPCION: Inicia el envio y recepcion de video
	# ARGS_OUT:
    
    def iniciar(self):
        self.gui.stopSubWindow()
        self.gui.showSubWindow("Video")
        self.enviando = True
        self.recibiendo = True

        self.inicializacion_hilos()
    
    # FUNCION: finalizar
	# ARGS_IN: self
	# DESCRIPCION: finaliza el envio y recepcion de video
	# ARGS_OUT:

    def finalizar(self):
        self.enviando = False
        self.recibiendo = False

        self.gui.destroySubWindow("Video")
        self.cola_imagenes = None

    # FUNCION: buttonsCallback
	# ARGS_IN: self, button - el boton pulsado
	# DESCRIPCION: gestiona lo que hacen los botones
	# ARGS_OUT: 

    def inicializacion_hilos(self):
        """
        Simplemente iniciamos dos hilos:
            Uno de ellos recibe video y lo muestra
            El otro lo envia
        """

        # Hilo de enviar video
        t = threading.Thread(target=self.enviar_video)
        t.daemon = False
        t.start()
        t = threading.Thread(target=self.recibir_video)
        t.daemon = False
        t.start()

    def buttonsCallback(self, button):

        if button == "colgar":
            msg = "CALL_END " +self.session_user['nickname']

            my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            address = (self.calling_user['ip'],int(self.calling_user['puerto']))
            my_socket.connect(address)

            my_socket.send(msg.encode(encoding='utf-8'))
            my_socket.close()


            self.gui.destroySubWindow("Video")
            self.cola_imagenes = None
    
    # FUNCION: enviar_video
	# ARGS_IN: self
	# DESCRIPCION: gestiona el envio de video con su correspondiente socket
	# ARGS_OUT: 

    def enviar_video(self):
        """
            Cogemos de la cola de envio lo que haya y lo enviamos por el socker udp
        """
        session_user = servidor_descubrimiento.read_session_user()
        calling_user = servidor_descubrimiento.read_calling_user()
        # Abrimos el socket
        my_socket = socket.socket(socket.AF_INET,  socket.SOCK_DGRAM) # Modo UDP
        while self.enviando:
            
            try:
                img = self.cola_imagenes.get(timeout=0.2)
                self.frame_count += 1
                timestamp = str(time.time())
                MESSAGE = str(self.frame_count)+"#"+timestamp + \
                    "#"+"640x480"+"#"+str(5)+"#"
                MESSAGE = MESSAGE.encode("utf-8") + img
                my_socket.sendto(
                    MESSAGE, (calling_user['ip'], calling_user['puerto_udp_escucha']))
            except:
                pass

        my_socket.close()

    # FUNCION: recibir_video
	# ARGS_IN: self
	# DESCRIPCION: gestiona la recepcion de video con su correspondiente socket
	# ARGS_OUT: 

    def recibir_video(self):
        """
            Leemos del socket UDP y lo mostramos en la gui
        """
        session_user = servidor_descubrimiento.read_session_user()
        calling_user = servidor_descubrimiento.read_calling_user()

        # self.gui.infoBox("ESCUCHO EN",str(self.puerto_udp_envia))

        #TODO no hacer bucle infinito. Que se termine al colgar
        my_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # En modo UDP
        my_socket.bind((session_user['ip'], session_user['puerto_udp_escucha']))

        while self.recibiendo:
            
            try:
                data, _ = my_socket.recvfrom(80000)
                img = data.split(b"#", 4)[4]

                # Descompresión de los datos, una vez recibidos
                decimg = cv2.imdecode(np.frombuffer(img, np.uint8), 1)
                frame_compuesto = decimg

                # Conversión de formato para su uso en el GUI
                cv2_im = cv2.cvtColor(frame_compuesto, cv2.COLOR_BGR2RGB)
                img_tk = ImageTk.PhotoImage(Image.fromarray(cv2_im))

                # Lo mostramos en el GUI                                
                # self.gui.setImageSize("imagen_stream", 640, 360)
                self.gui.setImageData("imagen_stream", img_tk, fmt='PhotoImage')

            except socket.timeout:
                pass
        my_socket.close()