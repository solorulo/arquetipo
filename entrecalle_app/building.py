# Librerias de Django
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate
from django.views.defaults import page_not_found, server_error
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.views.decorators.csrf import csrf_exempt
from sorl.thumbnail import get_thumbnail
from django.utils import simplejson
from django.core.files.uploadedfile import UploadedFile

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

class getUser_info(dict):
	pass

def __init__(request):

	try:
		
		if request.user.is_authenticated():

			if request.session['permisos'] == 4:
						
				getUser_info.permiso = 'Observador'
						
			elif request.session['permisos'] == 3:
						
				getUser_info.permiso = 'Visitante'
						
			elif request.session['permisos'] == 2:
						
				getUser_info.permiso = 'Habitante'
						
			elif request.session['permisos'] == 1:
						
				getUser_info.permiso = 'Moderador'

			# Agregamos mas campos al diccionario de informacion
			getUser_info.usuario = request.session['apodo']
			getUser_info.puntos = request.session['puntos']
			getUser_info.comentarios = request.session['comentarios']
			getUser_info.fotografias = request.session['fotografias']
			getUser_info.foto = request.session['foto']

			getUser_info.menu = True # Agregamos la propiedad menu=True para mostrar el menu del usuario

		else:

			getUser_info.menu = False
	
	except:

		# Agregamos mas campos al diccionario de informacion
		getUser_info.permiso = 'Administrador'
		getUser_info.usuario = 'Infinito'
		getUser_info.puntos = 'Infinito'
		getUser_info.comentarios = 'Infinito'
		getUser_info.fotografias = 'Infinito'
		getUser_info.foto = ''

		getUser_info.menu = True # Agregamos la propiedad menu=True para mostrar el menu del usuario


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

		CronicasFiltradas = Cronica.objects.filter( edificio = id )

		Fotos = []
		usuarios_fotos = []

		CronicasFiltradas.test=[]

		for croniquilla in CronicasFiltradas:
			usuario_info = Informacion_personale.objects.get(user_id =croniquilla.usuario)

			#usuarios_fotos.append(url(usuario_info.foto_perfil, width=100, height=100))
			usuarios_fotos.append(url(usuario_info.foto_perfil))

		Cronicas = zip(CronicasFiltradas,usuarios_fotos)

		info_edificio.CronicasFiltradas = CronicasFiltradas



		info_edificio.view = True # Agregamos la propiedad view=True para que se pueda agregar el js y el css de la plantilla vista

		__init__(request)

		# Renderizamos la pagina
		return render(request,'Edificio/build_view.html',{
			'Informacion': getUser_info,
			'info_edificio': info_edificio,
			'Cronicas':Cronicas,
			'building_view': True
			})


	except Edificio.DoesNotExist: # Si no existe el edificio enviamos un 404
		
		return page_not_found(request, "404.html")

#########################################################################################################################################################
#																																						#
#								Agregar_Cronica: Agrega una cronica a la base de datos											 		          		#
#																																						#
#												siempre que el usuario este autenticado
#												(para pruebas no es necesario estar autenticado)																										#
#########################################################################################################################################################
import time
from datetime import date
def Agregar_Cronica(request):
	if request.user.is_authenticated():
		if request.is_ajax():
			if request.method == 'GET':
				today = date.today()
				FechaHoy = str(today.day) + '/' + str(today.month) + '/' + str(today.year)
				Cronica( edificio_id = request.GET['edifID'], cronica = request.GET['LaCronica'], usuario = request.session['id'], fecha = FechaHoy).save()
				request.session['comentarios'] = request.session['comentarios']+1
				Informacion_personale.objects.filter(user_id=request.session['id']).update(N_Comentarios=F('N_Comentarios')+1 )
				message = request.GET['LaCronica']
				return HttpResponse(message)
			else:
				message = "no se subio la cronica metodo no es GET"
		else:
			message = "no se subio la cronica a"
			return HttpResponse(message)
	else:
		if request.is_ajax():
			if request.method == 'GET':
				today = date.today()
				FechaHoy = str(today.day) + '/' + str(today.month) + '/' + str(today.year)  
				Cronica( edificio_id = request.GET['edifID'], cronica = request.GET['LaCronica'], usuario = 3, fecha = FechaHoy).save()
				message = request.GET['LaCronica']
				return HttpResponse(message)
			else:
				message = "no se subio la cronica metodo no fue GET"
		else:
			message = "no se subio la cronica b"
			return HttpResponse(message)




#########################################################################################################################################################
#																																						#
#								building_add: Agrega un edificio a la base de datos 											 		          		#
#																																						#
#					form => Almacena el formulario para enviar los datos de un edificio 																#
#																																						#
#########################################################################################################################################################

@login_required(login_url='/login',redirect_field_name='') # Verificamos que el usuario este logeado
def build_add(request):

 	if request.method == 'POST': # Verificamos que el formulario haya sido enviado

		form = Building(request.POST, request.FILES) # Guardamos las peticiones en la variable form

		if form.is_valid(): # Verificamos que la informacion enviada sea valida

			try: # Verificamos que el edificio no exista

				Edificio.objects.get(longitud=form.cleaned_data['longitud'],latitud=form.cleaned_data['latitud'],nombre=form.cleaned_data['nombre'])
				mensaje = "Error 0004: Lo sentimos pero este edificio no esta en nuestra base de datos"

				return render(request,'building_add.html',{
					'form':form,'mensaje_m':mensaje
					})

			except Edificio.DoesNotExist: # Si no existe el edificio tratamos de darlo de alta

				try: # Intentamos guardar la informacion

					form.save() # Guardamos toda la informacion del edificio

					try: # Intentamos traernos la imagen principal del edificio y guardarla en la tabla Imagene

						edif = Edificio.objects.get(longitud=form.cleaned_data['longitud'],latitud=form.cleaned_data['latitud'],nombre=form.cleaned_data['nombre'])
						Imagene(url=edif.foto_url,edificio_id=edif.edificio_id).save()

						try: # Intentamos aumentar los puntos

							# Agregamos los puntos respectivos por dar de alta un edificio y una imagen
							request.session['puntos'] = request.session['puntos']+1
							request.session['fotografias'] = request.session['fotografias']+1

							# Los puntos los almacenamos en la base de datos
							Informacion_personale.objects.filter(user_id=request.session['id']).update(ranknig=F('ranknig')+1,N_Fotografias=F('N_Fotografias')+1 )

							# Redirigimos a la pagina del edificio creado
							return HttpResponseRedirect('/building/view/'+str(edif.edificio_id))

						except: # Si no se le asigna un numero de likes a una imagen se borra todo lo anterior

							Imagene.objects.get(url=edif.foto_url,edificio=edif.edificio_id).delete()
							Edificio.objects.get(edificio_id=edif.edificio_id).delete()
							mensaje = "Error 0003 al dar de alta edificio"

							return render(request,'Edificio/building_add.html',{
								'form':form,
								'mensaje_m':mensaje
								})

					except: # Si no podemos traer la imagen principal del edificio eliminamos el edificio

						Edificio.objects.get(edificio_id=edif.edificio_id).delete()
						mensaje = "Error 0002 al dar de alta edificio"

						return render(request,'Edificio/building_add.html',{
							'form': form,
							'mensaje_m': mensaje
							})

				except: # Si no podemos guardar la informacion del edificio mandamos un mensaje de error

					mensaje = "Error 0001 al dar de alta edificio"

					return render(request,'Edificio/building_add.html',{
						'form':form,
						'mensaje_m':mensaje
						})

		# Si el formulario no es valido renderizamos el form denuevo con los errores
		return render(request,'Edificio/building_add.html',{
			'form':form
			})

	else: # Si no se ha enviado nada por POST mostramos el formulario vacio

		form = Building() #Le asignamos a form el formulario del edificio

	return render(request,'Edificio/building_add.html',{
		'form':form
		})

#########################################################################################################################################################
#																																						#
#						building_photo_render: Muestra El Menu Para Subir imagenes 																		#
#																																						#
#																																						#
#########################################################################################################################################################

@login_required(login_url='/login',redirect_field_name='') # Verificamos que el usuario este logeado
def building_photo_render(request,id):

	_edificio = get_object_or_404(Edificio,edificio_id=id)

	return render(request,'Edificio/add_photo.html',{
		'nombre':_edificio.nombre,
		'edificio_id':id
		})

#########################################################################################################################################################
#																																						#
#						building_photo_ajax: Muestra El Menu Para Subir imagenes 																		#
#																																						#
#																																						#
#########################################################################################################################################################

@csrf_exempt
def building_photo_ajax(request):
	"""
    Main Multiuploader module.
    Parses data from jQuery plugin and makes database changes.
    """
	if request.method == 'POST':
		if request.FILES == None:
			return HttpResponseBadRequest('Debes adjuntar fotos')


		file = request.FILES[u'files[]']

		# Guardamos dentro de la base de datos
		try:
			image = Imagene()
			image.url=file
			image.edificio_id = request.POST['id'] # Contiene el id del edificio
			image.usuario = request.session['id'] # Contiene el id del usuario
			image.save()

			# Agregamos los puntos
			Informacion_personale.objects.filter(user_id=request.session['id']).update( N_Fotografias=F('N_Fotografias')+1 )
			request.session['fotografias'] = request.session['fotografias']+1

		except:
			return HttpResponseBadRequest('Error jpg,gif,png')

		# Creamos un arreglo que contenga la url y el thumbnail que es lo mismo
		#imagen = Imagene.objects.filter(imagen_id=request.POST['id']).latest('imagen_id')
		result = []

		result.append({
			"url":'/media/images/check.png', 
			"thumbnail_url":'/media/images/check.png',
			})
		response_data = simplejson.dumps(result)
        
		#checking for json data type
		#big thanks to Guy Shapiro
		if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
			mimetype = 'application/json'
		else:
			mimetype = 'text/plain'
		return HttpResponse(response_data, mimetype=mimetype)
	else: #GET
		return HttpResponse('Only POST accepted')