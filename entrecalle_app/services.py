from django.http import HttpResponse
from django.utils import simplejson

from entrecalle_app.models import *

# Librerias para la conecion con el servidor de imagenes
import cloudinary
from cloudinary import uploader, utils, CloudinaryImage


def url(self, **options):
    options.update(format = self.format, version = self.version)
    return utils.cloudinary_url(self.public_id, **options)[0]

def building_json(request):

	Edificios = Edificio.objects.all()
	
	_json = []

	for edif in Edificios:

		Imagene = Categoria.objects.get(categoria_tipo = str(edif.categoria))

		_json.append({
			'pk':edif.edificio_id,
			'nombre':edif.nombre,
			'direccion':edif.direccion,
			'longitud':edif.longitud,
			'latitud':edif.latitud,
			'categoria':str(edif.categoria),
			'foto_url':url(edif.foto_url),
			'categoria_img': url(Imagene.imagen)

			})

	data = simplejson.dumps(_json,indent=4)
	return HttpResponse(data)