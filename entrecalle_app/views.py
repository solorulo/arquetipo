from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
##########
from entrecalle_app.forms import *
from entrecalle_app.models import *
from entrecalle_app.building import *
##########
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.views.defaults import page_not_found
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail,BadHeaderError
import random


def handler404(request):
	return render(request,'error404.html')
def handler500(request):
	return render(request,'error404.html')


# Utilizamos esta clase para almacenar la informacion de sesion
class getUser_info(dict):
	pass

class Agregado:
	pass

class Categoria:
	pass

class Monumento:
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

		session_key = request.session.session_key  # Sacamos el id de las variables de session

		session = Session.objects.get(session_key=session_key)
		uid = session.get_decoded().get('_auth_user_id')
		usu = User.objects.get(pk=uid) # Nos traemos el id yy el apodo del usuario
		informacion_usuario = Informacion_personale.objects.get(user=usu.id) # Nos traemos toda la informacion personal del usuario
						
		# Almacenamos toda la informacion del usuario en variables de sesion para despues utilizarlas
		request.session['apodo'] = usu.username
		request.session['permisos'] = informacion_usuario.permisos
		request.session['puntos'] = informacion_usuario.ranknig
		request.session['comentarios'] = informacion_usuario.N_Comentarios
		request.session['fotografias'] = informacion_usuario.N_Fotografias
		request.session['resena'] = informacion_usuario.N_Resenas
		request.session['biografias'] = informacion_usuario.N_Biografias
		request.session['foto'] = url(informacion_usuario.foto_perfil)
		request.session['id'] = usu.id

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

#############################################################################
#																			#
#				index: Muestra la pagina principal de entrecalle 		 	#
#																			#
#																			#
#############################################################################

def index(request):

	__init__(request)

	try:
		# Sacamos el ultimo edificio agregado
		_edif = Edificio.objects.all()
		_edificio = Edificio.objects.all().latest('edificio_id')
		#_monumento = Edificio.objects.filter(categoria = 15)

		ultimoAgregado = Agregado

		ultimoAgregado.nombre = _edificio.nombre
		ultimoAgregado.texto = _edificio.descripcion[0:50]
		ultimoAgregado.imagen = url( _edificio.foto_url )
		ultimoAgregado.id = _edificio.edificio_id

		# Sacamos un edificio en las categorias

		_edificio_mostrar = random.randint(0,len(_edif)-1)

		categoriaMostrar = Categoria
		categoriaMostrar.nombre = _edif[_edificio_mostrar].nombre
		categoriaMostrar.categoria = _edif[_edificio_mostrar].categoria
		categoriaMostrar.texto = _edif[_edificio_mostrar].descripcion[0:50]
		categoriaMostrar.imagen = url(_edif[_edificio_mostrar].foto_url)
		categoriaMostrar.id = _edif[_edificio_mostrar].edificio_id

		# Sacamos los monumentos

		_monumentos_mostrar = random.randint(0,len(_edif)-1)

		monumentoMostrar = Monumento
		monumentoMostrar.nombre = _edif[_monumentos_mostrar].nombre
		monumentoMostrar.texto = _edif[_monumentos_mostrar].descripcion[0:50]
		monumentoMostrar.imagen = url(_edif[_monumentos_mostrar].foto_url)
		monumentoMostrar.id = _edif[_monumentos_mostrar].edificio_id

		

		return render(request,'index.html',{
			'Informacion': getUser_info,
			'ultimoAgregado':ultimoAgregado,
			'categoriaMostrar':categoriaMostrar,
			'Monumento': monumentoMostrar
				})

	except:
		
		return render(request,'index.html',{
						'Informacion':getUser_info,
					})




#############################################################################
#																			#
#				register: Crea un nuevo usuario 							#
#																			#
#																			#
#############################################################################

def register(request):

	if request.user.is_authenticated(): # Si ya esta logeado lo manda a la pagina principal
	
		return HttpResponseRedirect('/')
	
	else: # Si no esta logeado lo registra

		if request.method == 'POST': # Si el usuario ya envio alguna informacion

			uform = UserForm( data = request.POST)
			pform = UserProfileForm( data = request.POST )

			if uform.is_valid() and pform.is_valid(): # Verificamos que todos los campos sean correctos

				try: # Verificamos que el correo no este registrado

					email = uform.cleaned_data['email'] 
					User.objects.get( email = email )

					uform = UserForm( request.POST ) 
					pform = UserProfileForm( request.POST )

					mensaje = "El correo ya esta registrado "
					return render(request,"Usuario/register.html",{
						'uform': uform,
						'pform': pform,
						'mensaje': mensaje
					}) 

				except User.DoesNotExist:

					user = User.objects.create_user( uform.cleaned_data['username'], uform.cleaned_data['email'], uform.cleaned_data['password'] ) # Guardamos el usuario
					user.save()
					profile = pform.save(commit = False) # Guardamos la informacion del usuario
					profile.user = user # Le asignamos un usuario a la informacion
					profile.save() # Guardamos la info

					# Alacenamos los datos del form en una variable respectiva
					usuario = uform.cleaned_data['username']
					password = uform.cleaned_data['password']
					user = authenticate( username=usuario, password=password )
	
					auth_login(request, user) # Iniciamos sesion

					usu = User.objects.get(username=usuario) # Nos traemos el id yy el apodo del usuario
					informacion_usuario = Informacion_personale.objects.get(user=usu.id) # Nos traemos toda la informacion personal del usuario
					
					# Almacenamos toda la informacion del usuario en variables de sesion para despues utilizarlas
					request.session['apodo'] = usu.username
					request.session['permisos'] = informacion_usuario.permisos
					request.session['puntos'] = informacion_usuario.ranknig
					request.session['comentarios'] = informacion_usuario.N_Comentarios
					request.session['fotografias'] = informacion_usuario.N_Fotografias
					request.session['resena'] = informacion_usuario.N_Resenas
					request.session['biografias'] = informacion_usuario.N_Biografias
					request.session['foto'] = informacion_usuario.foto_perfil
					request.session['id'] = usu.id

					return HttpResponseRedirect('/')

			else:

				uform = UserForm() 
				pform = UserProfileForm()

				mensaje = "Todos los campos son obligatorios o el usuario ya existe"
				return render(request,"Usuario/register.html",{
					'uform': uform,
					'pform': pform,
					'mensaje': mensaje
				})
		else:

			uform = UserForm() 
			pform = UserProfileForm()

		return render(request,"Usuario/register.html",{
			'uform': uform,
			'pform': pform
		})





#############################################################################
#																			#
#					Login: Loguea a un usuario 	 							#
#																			#
#																			#
#############################################################################

def login(request):

	if request.user.is_authenticated(): # Si el usuario ya esta logeado lo manda al index
	
		return HttpResponseRedirect('/')
	
	else: # Si el usuario no esta logeado seguimos con el procedimiento
	
		if request.method == 'POST': # Si el usuario ya envio todos sus datos
	
			form = Login(request.POST) # Recolectamos el POST y lo guardamos en la variable form
	
			if form.is_valid(): # Si el formulario es valido iniciamos con el proceso de login
				
				# Alacenamos los datos del form en una variable respectiva
				usuario = form.cleaned_data['usuario']
				password = form.cleaned_data['password']
				user = authenticate( username=usuario, password=password )
	
				if user is not None: # Si existe el usuario
	
					if user.is_active: # Si el usuario no esta banneado
	
						auth_login(request, user) # Iniciamos sesion

						usu = User.objects.get(username=usuario) # Nos traemos el id yy el apodo del usuario
						informacion_usuario = Informacion_personale.objects.get(user=usu.id) # Nos traemos toda la informacion personal del usuario
						
						# Almacenamos toda la informacion del usuario en variables de sesion para despues utilizarlas
						request.session['apodo'] = usu.username
						request.session['permisos'] = informacion_usuario.permisos
						request.session['puntos'] = informacion_usuario.ranknig
						request.session['comentarios'] = informacion_usuario.N_Comentarios
						request.session['fotografias'] = informacion_usuario.N_Fotografias
						request.session['resena'] = informacion_usuario.N_Resenas
						request.session['biografias'] = informacion_usuario.N_Biografias
						request.session['foto'] = url(informacion_usuario.foto_perfil)
						request.session['id'] = usu.id

						return HttpResponseRedirect('/')
	
					else: # Si el usuario esta baneado
	
						return HttpResponseRedirect('/')
	
				else: # Si el usuario o el password no coinciden
	
					mensaje = 'Lo sentimos pero su apodo o password son incorrectos'
					form = Login()
					
					return render(request,'Usuario/login.html',{
						'form':form,
						'mensaje':mensaje,
						'login': True
						})
	
			else: # Si la informacion del formulario no es valida

				mensaje = 'Lo sentimos pero su apodo o password son incorrectos'
				form = Login()
				
				return render(request,'Usuario/login.html',{
					'form':form,
					'mensaje':mensaje,
					'login': True
					})
	
		else: # Si todavia no se ha enviado nada del formulario
	
			form = Login()
			
			return render(request,'Usuario/login.html',{
				'form':form,
				'login': True
				})


#############################################################################
#																			#
#					Logout: Cierra la sesion de un usuario 	 				#
#																			#
#																			#
#############################################################################

def logout(request):
	auth_logout(request)
	return HttpResponseRedirect('/')

#############################################################################
#																			#
#			terminos: Contiene los terminos y condiciones de uso 			#
#																			#
#																			#
#############################################################################

def terminos(request):

	return render(request,'Paginas/terminosdeuso.html')

#############################################################################
#																			#
#			privacidad: Contiene las politicas de privacidad 	 			#
#																			#
#																			#
#############################################################################

def privacidad(request):

	return render(request,'Paginas/privacy.html')

#############################################################################
#																			#
#			infoUser: Vista para modificar la informacion del usuario 	 	#
#																			#
#																			#
#############################################################################
@login_required(login_url='/login',redirect_field_name='')
def infoUser(request):
	
	__init__(request)

	userInfo = User.objects.get(username=getUser_info.usuario)

	getUser_info.nombre = userInfo.first_name
	getUser_info.apellidos = userInfo.last_name
	getUser_info.email = userInfo.email

	return render(request,'Usuario/usuario.html',{
		'Informacion':getUser_info,
		})

@login_required(login_url='/login',redirect_field_name='')
@csrf_exempt
def infoUser_ajax(request):

	if request.method == 'POST':
		if request.FILES == None:
			return HttpResponse('1')

		#try:
		__init__(request)

		Informacion = User.objects.filter(username=getUser_info.usuario).update(first_name=request.POST['nombre'],last_name=request.POST['apellidos'],email=request.POST['email'])
		Informacion = User.objects.get(username=getUser_info.usuario)

		Foto = Informacion_personale.objects.get(user = Informacion.pk)
		Foto.foto_perfil = request.FILES['foto_perfil']
		Foto.save()


		userInfo = User.objects.get(username=getUser_info.usuario)
		Foto = Informacion_personale.objects.get(user = Informacion.pk)

		getUser_info.nombre = userInfo.first_name
		getUser_info.apellidos = userInfo.last_name
		getUser_info.email = userInfo.email
		request.session['foto'] = url(Foto.foto_perfil)
		getUser_info.foto = request.session['foto']
		

		return render(request,'Usuario/usuario.html',{'success':True,'Informacion':getUser_info,})
		
		# except:
		# 	return render(request,'Usuario/usuario.html',{
		# 		'success':False,
		# 		'Informacion':getUser_info,
		# 		})
	else:
		return render(request,'error404.html')



def passord_reset(request):

	return render(request,'reset_password/forgot_password.html')