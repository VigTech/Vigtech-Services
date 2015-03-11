# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='proyecto',
            fields=[
                ('id_proyecto', models.AutoField(serialize=False, primary_key=True)),
                ('nombre', models.CharField(max_length=200, db_column=b'nombre_proyecto')),
                ('calificacion', models.IntegerField()),
                ('fraseBusqueda', models.CharField(max_length=200, db_column=b'busqueda')),
                ('disponibilidad', models.CharField(max_length=200, db_column=b'disponibilidad', choices=[(b'PUBLICO', b'Publico'), (b'PRIVADO', b'Privado')])),
                ('idUsuario', models.ForeignKey(to=settings.AUTH_USER_MODEL, db_column=b'fk_usuario')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
