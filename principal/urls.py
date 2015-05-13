from django.conf.urls import patterns, include, url
from .views import *
from django.conf import settings

urlpatterns = patterns('',
                       url(r'^$', login_required(home.as_view()), name='index'),
                       url(r'^home/$', login_required(home.as_view()), name='home'),
                       url(r'^gestionusuarios/registrar/$', RegistrarUsuario.as_view(), name='registrar_usuario'),
                       url(r'^gestionproyectos/nuevoProyecto/$', 'principal.views.nuevo_proyecto',
                           name='crear_proyecto'),

                       url(r'^gestionproyectos/MisProyectos/$', 'principal.views.ver_mis_proyectos',
                           name='ver_mis_proyectos'),
                       url(r'^gestionproyectos/editar_proyecto/(\d+)$', 'principal.views.editar_proyecto',
                           name='editar_proyecto'),
                       url(r'^gestionproyectos/ver_proyecto/(\d+)$', 'principal.views.ver_proyecto',
                           name='ver_proyecto'),
                       url(r'^gestionproyectos/eliminar_proyecto/(\d+)$', 'principal.views.eliminar_proyecto',
                           name='eliminar_proyecto'),
                       url(r'^gestionproyectos/OtrosProyectos/$', 'principal.views.ver_otros_proyectos',
                           name='ver_otros_proyectos'),
                       url(r'^gestionbusqueda/$', 'principal.views.busqueda_navegacion', name='busqueda_navegacion'),
                       url(r'^gestionbusqueda/Resultados/$', 'principal.views.buscador', name="buscador"),
                       url(r'^gestionanalisis/$', 'principal.views.analisisView', name="analisis"),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}),

                       # url(r'^home/$' ,'buscador.views.indexarArchivos', name='indexar'),


)
