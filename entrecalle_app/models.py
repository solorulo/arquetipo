from django.db import models
from datetime import date
from django.contrib.auth.models import User
import cloudinary
from cloudinary.models import *

# Create your models here.

class Intere(models.Model):

    interes = models.CharField(max_length=200)

    def __unicode__(self):
        return self.interes
    
class Informacion_personale(models.Model):
    
    user = models.OneToOneField(User)
    pais = models.CharField(max_length = 30,null=True,blank=True)
    sexo = models.CharField(max_length=1, choices=(('H', 'Hombre'), ('M', 'Mujer')))
    areas_interes = models.ManyToManyField(Intere,null=True,blank=True)
    permisos = models.IntegerField(default = 4)
    ranknig = models.BigIntegerField(default = 0)
    foto_perfil = CloudinaryField('foto_url',null=True,blank=True)
    noticias = models.BooleanField(default=True)
    N_Comentarios = models.BigIntegerField(default = 0)
    N_Fotografias = models.BigIntegerField(default = 0)
    N_Resenas = models.BigIntegerField(default = 0)
    N_Biografias = models.BigIntegerField(default = 0)
    
    
class Categoria(models.Model):
    
    categoria_id = models.AutoField(primary_key=True)
    categoria_tipo = models.CharField(max_length=50)
    imagen = CloudinaryField('imagen')
    
    def __unicode__(self):
        return self.categoria_tipo
    
class Edificio(models.Model):
    
    edificio_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=200)
    categoria = models.ForeignKey(Categoria,null=True,blank=True,default=1)
    descripcion = models.TextField(null=True,blank=True)
    direccion = models.CharField(max_length = 300,null=True,blank=True)
    foto_url = CloudinaryField('foto_url')
    longitud = models.CharField(max_length=30,null=True,blank=True)
    latitud = models.CharField(max_length=30,null=True,blank=True)

    def __unicode__(self):
        return self.nombre
    
class Imagene(models.Model):
    
    imagen_id = models.AutoField(primary_key=True)
    url = CloudinaryField('foto_url')
    edificio = models.ForeignKey(Edificio)
    tipo = models.CharField(max_length=2,default=0)
    usuario = models.CharField(max_length=15)

class Cronica(models.Model):

    edificio = models.ForeignKey(Edificio)
    cronica = models.CharField(max_length=121)
    usuario = models.CharField(max_length=50)
    fecha = models.CharField(max_length=11)