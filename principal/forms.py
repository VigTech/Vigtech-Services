#encoding:UTF-8
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
            User.objects.get(email = value)
            raise forms.ValidationError("El Email ya existe")
        except User.MultipleObjectsReturned:
            raise forms.ValidationError("El Email ya existe")
        except User.DoesNotExist:
            pass


class FormularioRegistrarUsuario(UserCreationForm):

	nombres=forms.CharField(label="Nombres")
	apellidos=forms.CharField(label="Apellidos")
	email=UniqueUserEmailField(label="Email", required=True)
	#username=form.CharField(widget=forms.widget.TextInput, label="Nombre de usuario")
	#pass1=forms.CharField(widget=forms.widget.PasswordInput,label="Contraseña")
	#pass2=forms.CharField(widget=forms.widget.PasswordInput,label="Vuelva a escribir la contraseña")

	class Meta:
		model=User
		fields=['nombres', 'apellidos', 'username', 'email', 'password1', 'password2']
		#exclude=['username.help_text']
		help_texts = {
			'username': _('Help text'),
		}

	def save(self,commit=True):
		user = super(UserCreationForm,self).save(commit=False)
		user.first_name=self.cleaned_data["nombres"]
		user.last_name=self.cleaned_data["apellidos"]
		user.set_password(self.cleaned_data["password1"])
		if commit:
			user.save()
		return user

class FormularioCrearProyecto(ModelForm):
	class Meta:
		model=proyecto
		fields=['nombre',  'resumen']
	def __init__(self, *args, **kwargs):
		super(FormularioCrearProyecto, self).__init__(*args, **kwargs)
		self.fields['nombre'].label= "Título del proyecto"	
