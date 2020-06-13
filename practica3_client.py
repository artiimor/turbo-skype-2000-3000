# import the library
from appJar import gui
from PIL import Image, ImageTk
import numpy as np
import cv2
import threading

import servidor_descubrimiento
import conexion


session_user = {}

class VideoClient(object):

	def __init__(self, window_size):
		
		# Creamos una variable que contenga el GUI principal
		self.app = gui("Redes2 - P2P", window_size)
		self.app.setGuiPadding(10,10)
		self.cola_imagenes = None
		self.video = None

		# Primero necesitamos cosas para registrarnos
		self.app.addLabelEntry("Nickname")
		self.app.addLabelEntry("Password")
		self.app.addLabelEntry("Puerto")
		self.app.addLabelEntry("Protocolo")

		# Boton que recoge la informacion anterior
		self.app.addButton("Identificarse",self.buttonsCallback)

		# Preparación del interfaz
		self.app.addLabel("title", "Cliente Multimedia P2P - Redes2 ")
		self.app.addImage("video", "imgs/webcam.gif")



		# Registramos la función de captura de video
		# Esta misma función también sirve para enviar un vídeo
		self.cap = cv2.VideoCapture(0)
		self.app.setPollTime(20)
		self.app.registerEvent(self.capturaVideo)

		# Añadir los botones
		self.app.addButtons(["Conectar", "Salir"], self.buttonsCallback)
		
		# Barra de estado
		# Debe actualizarse con información útil sobre la llamada (duración, FPS, etc...)
		self.app.addStatusbar(fields=2)

	def start(self):
		self.app.go()

	# FUNCION: capturaVideo
	# ARGS_IN: self
	# DESCRIPCION: Comienza la captura de video
	# ARGS_OUT: 
	def capturaVideo(self):

		# Capturamos un frame de la cámara o del vídeo
		ret, frame = self.cap.read()

		frame = cv2.resize(frame, (640,480))
		cv2_im = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
		img_tk = ImageTk.PhotoImage(Image.fromarray(cv2_im))

		# Compresión JPG al 50% de resolución (se puede variar)
		encode_param = [cv2.IMWRITE_JPEG_QUALITY, 50]
		result, encimg = cv2.imencode('.jpg', frame, encode_param)

		if result == False:
			print('Error al codificar imagen')

		encimg = encimg.tobytes()
		# Añadimos a la cola de los cojones
		if (self.cola_imagenes is not None):
			self.cola_imagenes.put(encimg)
		self.app.setImageData("video", img_tk, fmt = 'PhotoImage')

		#if frame is not None:
		#	frame = cv2.resize(frame, (640,480))
		#	cv2_im = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
		#	img_tk = ImageTk.PhotoImage(Image.fromarray(cv2_im))			

		#	# Lo mostramos en el GUI
		#	self.app.setImageData("video", img_tk, fmt = 'PhotoImage')


	# FUNCION: buttonsCallback
	# ARGS_IN: self, button - el boton pulsado
	# DESCRIPCION: gestiona lo que hacen los botones
	# ARGS_OUT: 
	def buttonsCallback(self, button):

		#______________________________________________
		#______________________________________________
		# OPCION PARA SALIR DE LA APLICACION
		#______________________________________________
		#______________________________________________"
		if button == "Salir":
			# Salimos de la aplicación
			self.app.stop()
		#______________________________________________
		#______________________________________________
		# OPCION PARA CONECTAR CON UN USUARIO
		#______________________________________________
		#______________________________________________
		elif button == "Conectar":
			# Entrada del nick del usuario a conectar	
			nickname = self.app.textBox("Conexión", "Introduce el nick del usuario a buscar")	
			# Lo buscamos
			usuario = servidor_descubrimiento.query(nickname)

			# Si no se encuentra sale un mensaje de error
			if usuario == -1:
				usuario.app.errorBox("CONECTAR", "No existe el usuario con nickname: " +nickname)
			else:
				# Si se encuentra, exponemos la info que hemos recaudado
				# info = " ->Nickname: " +usuario['nickname'] +"\n ->Ip: " +usuario['ip'] +"\n ->Puerto: " +usuario['puerto'] +"\n ->Protocolo: " +usuario['protocolos']
				# self.app.infoBox("Informacion del usuario",info)
				session_user = servidor_descubrimiento.read_session_user()
				if (not session_user):
					self.app.infoBox("ERROR","Debes identificarte antes de iniciar una llamada")
				else:
					servidor_descubrimiento.save_calling_user(usuario)
					conexion.llamar(self)
		#______________________________________________
		#______________________________________________
		# OPCION PARA IDENTIFICARSE COMO USUARIO
		#______________________________________________
		#______________________________________________
		elif button == "Identificarse":
			#Obtenemos las cosas
			nickname = self.app.getEntry("Nickname")
			password = self.app.getEntry("Password")
			puerto = self.app.getEntry("Puerto")
			protocolo = self.app.getEntry("Protocolo")

			if len(nickname) == 0 or len(password) == 0 or len(puerto) == 0 or len(protocolo) == 0:
				return self.app.errorBox("REGISTRO", "Introduce todos los datos requeridos")
			
			# Ahora, registramos al usuario
			# logueo = servidor_descubrimiento.list_users()
			logueo = servidor_descubrimiento.register(nickname, puerto, password, protocolo)

			# Si algo falla
			if logueo == -1 or logueo == "NOK UNKNOWN_COMMAND":
				return self.app.errorBox("REGISTRO", "Los datos introducidos son incorrectos")

			# Thread para escuchar
			listen_thread = threading.Thread(target=conexion.escuchar, args=(self,),
												 daemon=False)

			# Comenzamos el thread de escucha
			listen_thread.start()
			
		#______________________________________________
		#______________________________________________
		# OPCION PARA OBTENER UN LISTADO DE TODOS LOS NICKNAMES DE USUARIO
		#______________________________________________
		#______________________________________________
		elif button == "Obtener Listado":

			# Lo buscamos
			usuarios = servidor_descubrimiento.list_users()

			# Si no se encuentra sale un mensaje de error
			if usuarios == -1:
				usuario.app.errorBox("OBTENER LISTADO", "Algo ha ido mal (Servidor de descubrimiento)")
			else:
				# Si se encuentra, exponemos la info que hemos recaudado
				self.app.infoBox("Informacion de usuarios",usuarios)


if __name__ == '__main__':

	vc = VideoClient("640x520")

	# Crear aquí los threads de lectura, de recepción y,
	# en general, todo el código de inicialización que sea necesario
	# ...


	# Lanza el bucle principal del GUI
	# El control ya NO vuelve de esta función, por lo que todas las
	# acciones deberán ser gestionadas desde callbacks y threads
	vc.start()