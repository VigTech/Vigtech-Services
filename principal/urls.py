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
                       url(r'^gestionanalisis/coautoria1$', 'principal.views.analisisView', name="coautoria1"),
                       url(r'^gestionanalisis/coautoria2$', 'principal.views.coautoria_old', name="coautoria2"),
                       url(r'^paises/$', 'principal.views.analisis_paises', name="analisis_paises"),
                       url(r'^autores/$', 'principal.views.analisis_autores', name="analisis_autores"),
                       url(r'^afiliaciones/$', 'principal.views.analisis_afiliaciones', name="analisis_afiliaciones"),
                       url(r'^revistas/$', 'principal.views.analisis_revistas', name="analisis_revistas"),
                       url(r'^docsfechas/$', 'principal.views.analisis_docsfechas', name="analisis_docsfechas"),
                       url(r'^tipodocs/$', 'principal.views.analisis_tipodocs', name="analisis_tipodocs"),
                       url(r'^paisespie/$', 'principal.views.analisis_paisespie', name="analisis_paisespie"),
                       url(r'^autorespie/$', 'principal.views.analisis_autorespie', name="analisis_autorespie"),
                       url(r'^afiliacionespie/$', 'principal.views.analisis_afiliacionespie', name="analisis_afiliacionespie"),
                       url(r'^revistaspie/$', 'principal.views.analisis_revistaspie', name="analisis_revistaspie"),
                       url(r'^docsfechaspie/$', 'principal.views.analisis_docsfechaspie', name="analisis_docsfechaspie"),
                       url(r'^tipodocspie/$', 'principal.views.analisis_tipodocspie', name="analisis_tipodocspie"),
                       url(r'^clustering/$', 'principal.views.analisis_clustering', name="clustering"),
                       url(r'^indicadores/$', 'principal.views.analisis_indicadores', name="indicadores"),
                       url(r'^clasificacion_eisc/$', 'principal.views.clasificacion_eisc', name="eisc"),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
                           {'document_root': settings.MEDIA_ROOT}),

                       # url(r'^home/$' ,'buscador.views.indexarArchivos', name='indexar'),


)
