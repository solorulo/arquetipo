from django import forms
from entrecalle_app.models import *
from django.contrib.auth.models import User
import cloudinary
from cloudinary.forms import *

    #areas_interes = forms.ModelMultipleChoiceField( queryset=Intere.objects.all() , required=False)

# Formularios para los usuarios
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email","first_name","last_name","password"]
        widgets = {
            'username': forms.TextInput ( attrs = { 'class' : 'validate[required] text-input' } ),
            'password': forms.PasswordInput( attrs ={ 'class' : 'validate[required] text-input' } )
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Informacion_personale
        fields = ["sexo", "areas_interes", "noticias", "pais" ]

class Login(forms.Form):
    usuario = forms.CharField( widget = forms.TextInput ( attrs = { 'class' : 'validate[required] text-input' } ) )
    password = forms.CharField( widget = forms.PasswordInput ( attrs ={ 'class' : 'validate[required] text-input' } ) )
    
class Building(forms.ModelForm):
    class Meta:
        model = Edificio
        exclude=('edificio_id')
        widgets = {
            'nombre':forms.TextInput( attrs = {'class':'validate[required] text-input'}),
            'categoria':forms.Select( attrs = {'type':'estilo'} ),
            'direccion':forms.TextInput( attrs = {'class':'validate[required] text-input','maxlength':'200'} ),
            'descripcion':forms.Textarea( attrs = {'type':'edif','rows':''} ),
            'longitud':forms.HiddenInput(),
            'latitud':forms.HiddenInput(),
        }
class Forgot_password(forms.Form):
    password = forms.CharField( widget = forms.TextInput ( attrs = {'class':'validate[required] text-input','maxlength':'50'} ) )

class Cronicas(forms.ModelForm):
    class Meta:
        model = Cronica
        widgets = {
            'cronica':forms.Textarea( attrs = {'type':'edif','rows':''} ),
        }