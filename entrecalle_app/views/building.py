# Librerias de Django
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib.auth import authenticate
from django.views.defaults import page_not_found, server_error

# Librerias para los modelos y los formularios
from entrecalle_app.models import *
from entrecalle_app.forms import *

# Librerias para la conecion con el servidor de imagenes
import cloudinary
from cloudinary import uploader, utils, CloudinaryImage

# Esencial para enviar las imagenes al servidor de cloudinary
def __init__(self):
	cloudinary.config(
  cloud_name = 'entrecalle2',  
  api_key = '292582476523925',  
  api_secret = 'HBttI7Q_3veYaYycFc7CZkKCmd4'  
)

# Nos devuelve la URL de la imagen en el servidor
def url(self, **options):
    options.update(format = self.format, version = self.version)
    return utils.cloudinary_url(self.public_id, **options)[0]

# Utilizamos esta clase para almacenar la informacion de sesion
class informacion_sesion(dict):
	pass



#########################################################################################################################################################
#																																						#
#						building_view: Muestra un edificio y toda su informacion, tambien agrega una cronica al Edificio 		                		#
#																																						#
#		informacion type=dict ==> Almacena toda la informacion del usuario																				#
#		info_edificio type=dict ==> Almacena toda la informacion del eficio, incluyendo las imagenes del mismo en info_edificio.imagenes como objeto	#
#																																						#
#########################################################################################################################################################
def build_view(request,id):
	
	try: # Intentamos buscar el edificio por su identificador

		info_edificio = Edificio.objects.get( edificio_id = id ) # Almacenamos toda la informacion del edificio

		# Almacenamos el objeto de todas las imagenes en el diccionario de la informacion del edificio para poder enviarla toda
		img = Imagene.objects.filter( edificio = id )
		imagenes = []
		for imagen in img:
			imagenes.append( url( imagen.url, width=750, height=550 ) ) # Nos traemos la URL de la imagen del servidor convertida a 750x550

		info_edificio.imagenes = imagenes

		info_edificio.view = True # Agregamos la propiedad view=True para que se pueda agregar el js y el css de la plantilla vista

		if request.user.is_authenticated(): # Verificamos que el usuario ya tiene una sesion iniciada

			informacion = informacion_sesion # Creamos un diccionario para almacenar toda la informacion del usuario

			# Verificamos el tipo de usuario
			if request.session['permisos'] == 4:

				informacion.permiso = 'Observador'
			
			elif request.session['permisos'] == 3:
			
				informacion.permiso = 'Visitante'
			
			elif request.session['permisos'] == 2:
			
				informacion.permiso = 'Habitante'
			
			elif request.session['permisos'] == 1:
			
				informacion.permiso = 'moderador'

			# Agregamos mas campos al diccionario de informacion
			informacion.usuario = request.session['apodo']
			informacion.puntos = request.session['puntos']
			informacion.comentarios = request.session['comentarios']
			informacion.fotografias = request.session['fotografias']
			informacion.foto = request.session['foto']
			informacion.resena = request.session['resena']
			informacion.biografia = request.session['biografias']

			informacion.menu = True # Agregamos la propiedad menu=True para mostrar el menu del usuario
			
			# Renderizamos la pagina
			return render(request,'building/building_view.html',{
				'informacion': informacion,
				'info_edificio': info_edificio,
				})

		else: # Si el usuario no esta logeado

			info_edificio.menu = False # Agregamos la propiedad menu=False para ocultar el menu del usuario

			# Renderizamos la pagina
			return render(request,'building/build_view.html',{
				'info_edificio': info_edificio,
				})


	except Edificio.DoesNotExist: # Si no existe el edificio enviamos un 404
		
		return page_not_found(request, "404.html")