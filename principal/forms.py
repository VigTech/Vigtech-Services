# encoding:UTF-8
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from principal.models import *
from django.utils.translation import ugettext_lazy as _
#from django.contrib.auth.models import User


#class FormularioRegistrarUsuario(UserCreationForm):
#	fields=['first_name', 'last_name', 'username', 'email', 'password']
class UniqueUserEmailField(forms.EmailField):
    """
    An EmailField which only is valid esr-gobernanza@renata.edu.coif no User has that email.
    """

    def validate(self, value):
        super(forms.EmailField, self).validate(value)
        try:
            User.objects.get(email=value)
            raise forms.ValidationError("El Email ya existe")
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("El Email ya existe")
        except User.DoesNotExist:
            pass


class FormularioRegistrarUsuario(UserCreationForm):
    nombres = forms.CharField(label="Nombres")
    apellidos = forms.CharField(label="Apellidos")
    email = UniqueUserEmailField(label="Email",help_text='Estos son tus datos personales.', required=True)
    username=forms.CharField(label="Vigtech usuario",help_text='Con este nombre podras acceder a tu cuenta en Vigtech.',required=True)
    email =forms.CharField(label="Correo",help_text='Escribe el correo donde pueda recibir actulizaciones sobre el VigTech.',required=True)
    password1=forms.CharField(widget=forms.PasswordInput(),help_text='Tu contraseña debe tener mas de 8 caracteres.',label="Contraseña",required=True)
    password2=forms.CharField(widget=forms.PasswordInput(),help_text='Escribe la misma contraseña para la verificacion',label="Confirmar Contraseña",required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2','nombres', 'apellidos', 'email']
        help_texts = {}

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name = self.cleaned_data["nombres"]
        user.last_name = self.cleaned_data["apellidos"]
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class FormularioCrearProyecto(ModelForm):
    class Meta:
        model = proyecto
        fields = ['nombre', 'resumen']

    def __init__(self, *args, **kwargs):
        super(FormularioCrearProyecto, self).__init__(*args, **kwargs)
        self.fields['nombre'].label = "Título del proyecto"
