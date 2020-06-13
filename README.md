# Turbo-Skype-2000-3000

## Construido con

* [C](https://en.wikipedia.org/wiki/C_%28programming_language%29)

## Developers

* **Javier Lougedo** - [JLougedo](https://github.com/JLougedo)
* **Arturo Morcillo** - [artiimor](https://github.com/artiimor)

## Introducción
Práctica 3 de la asignatura de Redes de Comunicaciones 2 de los alumnos Arturo Morcillo y Javier Lougedo, correspondiente a la creación de un servicio de videollamadas. Hemos denominado a todos nuestos proyectos "Turbo" para tener una cierta linealidad y punto en común para todos los proyectos, por lo que este tiene el sobrenombre de Turbo Videollamadas. La WiKi comprende las siguientes secciones:

Funcionamiento, donde explicamos como funciona la práctica e incluimos un pequeño video demostrativo.
Decisiones de diseño.
Código, con una breve descripción del mismo.
Troubleshooting, donde explicamos los problemas más propensos de ocurrir y como solucionarlos.
Conclusiones.

Esta práctica la comenzamos durante el periodo de cuarentena, alrededor de finales de mayo, ya que empleamos el tiempo principalmente en otras asignaturas que nos corrían más prisa hasta entonces. De nuevo esta práctica tratamos de organizarnos evitando a toda costa todas las solapaciones posibles. De esta forma, la organización que decidimos llevar a cabo, fue que Arturo se encargase del desarrollo y yo, Javier, de la documentación y de tratar de facilitar los contenidos necesarios, los módulos en cuestión y las distintas pruebas en las que localizamos los problemas más graves y sus motivos. Esta forma de organizarnos ha dado sus frutos, ya que al encontrarnos un poco con el agua al cuello en lo que al tiempo respecta, hemos conseguido no tener que solaparnos excesivamente, y no depender el uno del otro en gran medida para no derivar en interbloqueos, de forma que hemos podido estar trabajando prácticamente sin parar, en este sentido.
En las secciones de la WiKi a continuación, procuraremos comentar los detalles más relevantes de nuestra tercera práctica, aunque sea algo más "genérica", y las decisiones de diseño más importantes tomadas, los distintos tests realizados y los resultados obtenidos a partir de los mismos, aunque en esta práctica las decisiones de diseño han sido prácticamente nulas, los tests sencillos y simples (hemos probado un funcionamiento normal y esperado) y los problemas, bastantes.

## Funcionamiento
Arrancar esta práctica es sencillo. Inicialmente deberemos ejecutar todos los comandos avisados en el enunciado, a fin de instalar open-cv y demás (se da por hecho, por la práctica anterior, que disponemos de Python 3 y pip3). Estos se resumen en los siguientes:
foo@bar:~$ sudo apt install python3-pil.imagetk python3-tk python3-numpy python-imaging-tk
foo@bar:~$ pip3 install appjar
foo@bar:~$ sudo apt install python-opencv
foo@bar:~$ pip3 install opencv-python
Con todo esto, no debería de hacernos falta ningún módulo más y debería de funcionar de primeras, como hemos comprobado en una instalación a partir de cero. Solo faltaría hacer ifconfig en una terminal, copiar nuestra IP y pegarla en la zona superior del fichero servidor_descubrimiento.py, donde pone IP, remplazando la anterior por la nuestra. De esta forma, para arrancar el cliente, bastará con escribir las líneas anteriores en la terminal y la siguiente:
foo@bar:~$ python3 practica3_client.py
Esto nos abrirá la ventana de la aplicación, que hemos tratado de mantener sencilla, pues no es lo que se viene a evaluar, y de otorgarle la funcionalidad necesaria. En ella, deberemos introducir un nick cualquiera, una contraseña por si dicho nick ya existe demostrar que es nuestro, el puerto a utilizar (deberá de estar disponible) y el protocolo, inicialmente, y por el momento, v0.
Para llamar a alguien, lo que deberemos hacer será entonces clicar en el botón de conectar, donde introduciremos el usuario del destinatario de la llamada. Será entonces cuando a dicho usuario, le salte una notificación permitiendo unirse a la llamada. Al unirse, se abrirá una nueva ventana, donde verá la imagen recibida de su contacto, y verá en su programa la suya propia. Podrá entonces colgar su llamada y salir del sistema o realizar otra llamada sucesiva.
Podemos encontrar a continuación un ejemplo de uso.


## Decisiones de diseño
Como ya hemos comentado, en esta práctica no ha habido decisiones de diseño que tomar, sino más bien problemas que resolver y afrontar, principalmente con los puertos, protocolos y problemas de ejecución en distintos dispositivos (por ejemplo, en mi portatil funcionaba a la perfección pero exactamente el mismo código, modificando la IP, daba error en mi ordenador fijo, crasheando constantemente y en distintos puntos). De esta forma, hemos tratado de identificar la mayor cantidad de problemas posibles y resolver los más graves que hemos encontrado, implementando la funcionalidad mínima y excluyendo cosas que pudiesen agregar más problemas como el sonido y demás. Por otro lado, tampoco conseguimos que algunas de las webcams funcionasen, con lo que tuve que instalarlo de forma que fuese el móvil el que actuase como webcam a través de un simulador de webcam y un servicio web.
Hemos decidido prescindir del botón de colgar, ya que después de una o dos ejecuciones, el programa se atascaba sin solución posible, dando lugar a problemas en su ejecución que no hemos sabido resolver, con lo que para hacer dos llamadas sucesivas, habría que arrancar de nuevo el programa.

## Código
Nada más descargar el contenido de GitHub nos encontramos con una distribución similar a la siguiente:

Carpeta src, que contiene el código fuente de bajo nivel.
Carpeta appJar con todo lo necesario por si no funciona correctamente appJar en algún punto.
Carpeta imgs con algunos ficheros auxiliares con los que probar el programa.
Ficheros sueltos, que corresponden a:

Ficheros de texto para soporte de algunas funcionalidades (calling_user.txt, session_user.txt).
Script de simular internet.
Fichero Python principal que hace las veces de main.
NOTA: El código ha quedado desorganizado porque reubicarlo nos dió problemas.




## Troubleshooting
Los problemas que nos podemos encontrar a lo largo de la ejecución de esta práctica son bastantes. Inicialmente, todos deberían de poder ser resueltos a partir del feedback que se nos da en la terminal, mientras el programa se ejecuta. Estos pueden ser, los más probables:

No introducir nuestra IP en el fichero servidor_descubrimiento.py
Introducir un puerto ya ocupado por otro proceso
No tener webcam disponible de ningún tipo, con lo que es posible que el programa se cierre
Que haya algun tipo de problema con el servidor de vega
Si hay algún otro localizado, por favor, comentarlo a los desarrolladores de forma que se pueda incluir aquí. De esta forma, los problemas son sencillos de resolver, localizado el error que estamos cometiendo.


## Conclusiones
Esta práctica nos ha resultado mucho más dura y complicada. No hemos sabido organizarnos de manera adecuada en menos tiempo y la carga de trabajo era mucho mayor y dispar, habiendo muchas ramas de trabajo y de desarrollo disponibles. Además, hemos tenido muchas ideas iniciales que no sabíamos si podríamos implementar. Sin embargo, resulta práctico enfrentarse a un problema real de este calibre, para poder ver de cerca los problemas que representa.
Personalmente, encuentro que lo que nos ha fallado ha sido la organización, al preferir responsabilizarnos completamente uno u otro de lo que era la programación en sí y no generarnos problemas mútuos el uno al otro. Además, el desconocimiento de lo que eran algunos de los módulos y su funcionamiento ha derivado en una mayor cantidad de problemas, como así lo ha producido también el hecho de no tener webcam en algunos casos, con lo que había que cambiar el programa para probarlo con gif y video. En resumidas cuentas, hemos tenido excesivos problemas que en ocasiones no hemos sido capaces de resolver o cuya resolución ha derivado en una mayor cantidad de problemas. Relativamente, ha resultado una práctica mucho más compleja que la anterior y que ha sido más difícil de plantear.
