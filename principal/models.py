# -*- encoding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
import sys    # sys.setdefaultencoding is cancelled by site.py
reload(sys)    # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')
#rom django.contrib.auth.models import AbstractBaseUser
# Create your models here.

disponibilidad_choices= (
	("PUBLICO", "Público"),
	("PRIVADO", "Privado")
)

class proyecto(models.Model):
	#proyectoKey= models.AutoField(primary_key=True)

	id_proyecto=models.AutoField(primary_key=True)
	nombre=models.CharField(max_length=200, db_column="nombre_proyecto")
	idUsuario=models.ForeignKey(User, db_column="fk_usuario")
	calificacion=models.IntegerField()
	fraseBusqueda= models.CharField(max_length=200, db_column="busqueda")
	#disponibilidad= models.CharField(max_length=200, db_column="disponibilidad", choices=disponibilidad_choices)
	resumen=models.TextField(max_length=599, db_column='resumen')
	
	def __unicode__(self):
		return self.nombre

#class calificaciones(models.Model):
#	id_calificacion=models.AutoField(primary_key=True)
#	id_proyecto=models.ForeignKey(proyecto,db_column="fk_proyecto")