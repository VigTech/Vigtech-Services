# -*- encoding: utf-8 -*-
# from django.shortcuts import render, render_to_response, redirect, get_object_or_404, get_list_or_404, Http404
from django.core.cache import cache
from django.shortcuts import *
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.template import RequestContext
from django import template
from models import proyecto
from .forms import *
#from Logica.ConexionBD import adminBD
import funciones
import sys
#~ from administradorConsultas import AdministradorConsultas # Esta la comente JAPeTo
#~ from manejadorArchivos import obtener_autores # Esta la comente JAPeTo
#~ from red import Red # Esta la comente JAPeTo
from Logica import ConsumirServicios, procesamientoScopusXml, procesamientoArxiv
# import igraph
import traceback
import json
import django.utils
from Logica.ConexionBD.adminBD import AdminBD
from principal.parameters import *
from principal.permisos import *


# sys.setdefaultencoding is cancelled by site.py
reload(sys)  # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')
# Create your views here.
# @login_required

#ruta = "/home/administrador/ManejoVigtech/ArchivosProyectos/"

sesion_proyecto=None
proyectos_list =None
model_proyecto =None
id_proyecto = None
##nombre_proyecto = None


class home(TemplateView):
    template_name = "home.html"
    def get_context_data(self, **kwargs):
        global proyectos_list
        global model_proyecto 
        try:
            existe_proyecto = False
            proyectos_list = get_list_or_404(proyecto,  idUsuario=self.request.user)
            for project in proyectos_list:
                if  project == model_proyecto:
                    existe_proyecto = True
            if not (existe_proyecto):
                model_proyecto = None
        except:
           # print traceback.format_exc()
            proyectos_list = None
            model_proyecto = None
        return {'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos}
           

class RegistrarUsuario(FormView):
    template_name = "registrarUsuario.html"
    form_class = FormularioRegistrarUsuario
    success_url = reverse_lazy('RegistrarUsuarios')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Se ha creado exitosamente el usuario")
        return redirect('login')


def cambia_mensaje(crfsession,proyecto,usuario,borrar, mensaje,valor):
    # print ">>>> AQUI ESTOY"+str(borrar)+" & "+str(mensaje)
    try:
        cache_key = "%s_%s_%s" % (crfsession,proyecto.replace(" ",""),usuario)
        data = cache.get(cache_key)
        if data:
            data['estado'] = valor
            data['mensaje'] += mensaje
            if borrar :
                data['mensaje'] = mensaje
            cache.set(cache_key, data)
        else:
            cache.set(cache_key, {
                'estado': 0,
                'mensaje' : mensaje
            })
    except:
        pass

@login_required
def nuevo_proyecto(request):
    global id_proyecto
    global model_proyecto
    global proyectos_list
    
    if request.method == 'POST':
        form = FormularioCrearProyecto(request.POST)
        fraseB = request.POST.get('fraseB')
        fraseA = request.POST.get('fraseA')
        autor = request.POST.get('autor')
        words = request.POST.get('words')
        before = request.POST.get('before')
        after = request.POST.get('after')
        limArxiv = request.POST.get('limArxiv')
        limSco = request.POST.get('limSco')
        cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"",0)

        busqueda = fraseB + "," + words + "," + fraseA + "," + autor + "," + before + "," + after
        # print "busca "+busqueda+", by japeto"
        if form.is_valid():
            nombreDirectorio = form.cleaned_data['nombre']
            articulos = {}
            modelo_proyecto = form.save(commit=False)
            modelo_proyecto.idUsuario = request.user
            # print "formulario valido, by japeto"
            # print "2"
            # proyectos_list = get_list_or_404(proyecto,  idUsuario=request.user)
            # proyectos_list = get_list_or_404(proyecto, idUsuario=request.user)
            #modelo_proyecto.calificacion=5
            modelo_proyecto.fraseBusqueda = busqueda
            modelo_proyecto.save()

            proyectos_list = get_list_or_404(proyecto,  idUsuario=request.user)
            model_proyecto = get_object_or_404(proyecto, id_proyecto=modelo_proyecto.id_proyecto)
            id_proyecto = model_proyecto.id_proyecto

            #Creacion del directorio donde se guardaran los documentos respectivos del proyecto creado.
            mensajes_pantalla="<p class='text-primary'><span class='fa  fa-send fa-fw'></span>Se ha creado el Directorio para el proyecto</p>"
            funciones.CrearDirectorioProyecto(modelo_proyecto.id_proyecto, request.user)
            cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,mensajes_pantalla,6)
            # print "se crea directorio, by japeto"
            
            if fraseB != "":
                try:
                    """
                        Descarga de documentos de Google Arxiv
                    """
                    # print "descarga de documentos, by japeto"
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-primary'><span class='fa  fa-send fa-fw'></span>Descarga de documentos de Arxiv</p>",12)
                    articulos_arxiv= ConsumirServicios.consumir_arxiv(fraseB, request.user.username, str(modelo_proyecto.id_proyecto), limArxiv)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-success'><span class='fa  fa-check fa-fw'></span>Descarga de documentos terminada</p>",18)
                except:
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-danger'><span class='fa  fa-times fa-fw'></span><b>PROBLEMA: </b>Descarga de documentos de Arxiv</p>",12)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"STOP",0)
                    print traceback.format_exc()
                    
                try:
                    """
                        Descarga de documentos de Google Scopus
                    """
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-primary'><span class='fa  fa-send fa-fw'></span>Descarga de documentos de Scopus</p>",24)
                    articulos_scopus = ConsumirServicios.consumir_scopus(fraseB, request.user.username, str(modelo_proyecto.id_proyecto), limSco)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-success'><span class='fa  fa-check fa-fw'></span>Descarga de documentos terminada</p>",30)
                except:
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-danger'><span class='fa  fa-times fa-fw'></span><b>PROBLEMA: </b>Descarga de documentos de Scopus</p>",24)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"STOP",0)
                    print traceback.format_exc()
                    
                try:
                    """
                        Inserción de metadatos Arxiv
                    """
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-primary'><span class='fa  fa-send fa-fw'></span>Inica la inserción de metadatos Arxiv</p>",36)
                    xml = open(REPOSITORY_DIR+ str(request.user.username)+ "." + str(modelo_proyecto.id_proyecto) + "/salida.xml")
                    procesamientoArxiv.insertar_metadatos_bd(xml, str(modelo_proyecto.id_proyecto))
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-success'><span class='fa  fa-check fa-fw'></span>La inserción de metadatos Arxiv ha terminado</p>",42)
                except:
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",36)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-danger'><span class='fa  fa-times fa-fw'></span><b>PROBLEMA:</b>La inserción de metadatos Arxiv no se puede completar</p>",36)
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",36)
                    # print traceback.format_exc()
                
                try:
                    """
                       Conexión con base datos para insertar metadatos de paper de Scopus
                    """
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-primary'><span class='fa  fa-send fa-fw'></span>Inica la inserción de metadatos Scopus</p>",48)
                    busqueda = open(REPOSITORY_DIR+ str(request.user.username)+ "." + str(modelo_proyecto.id_proyecto) + "/busqueda0.xml")
                    procesamientoScopusXml.xml_to_bd(busqueda, modelo_proyecto.id_proyecto, articulos_scopus['titulos'])
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-success'><span class='fa  fa-check fa-fw'></span>La inserción de metadatos Scopus ha terminado</p>",54)
                except:
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",48)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-danger'><span class='fa  fa-times fa-fw'></span><b>PROBLEMA:</b>La inserción de metadatos Scopus no se puede completar</p>",48)
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",48)
                    # print traceback.format_exc()

               

                
                # try:
                #     """
                #         NAIVE BAYES
                #     """
                #     #ConsumirServicios.consumir_recuperacion_unidades_academicas(str(request.user.username),str(modelo_proyecto.id_proyecto))
                #     cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-primary'><span class='fa  fa-send fa-fw'></span>Inicia el procesado Scopus XML</ṕ>",60)
                #     procesamientoScopusXml.xml_to_bd(busqueda, modelo_proyecto.id_proyecto, articulos_scopus['titulos'])
                #     cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-success'><span class='fa  fa-check fa-fw'></span>El procesmiento Scopus XML ha terminado</p>",62)
                # except:
                #     # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",60)
                #     cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-danger'><span class='fa  fa-times fa-fw'></span><b>PROBLEMA:</b> El procesando Scopus XML no se puede completar</p>",60)
                #     # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",60)
                #     # print traceback.format_exc() 

                try:
                    
                    """
                         generar el XML OUTPUT
                   """
                    admin =AdminBD()
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-primary'><span class='fa  fa-send fa-fw'></span>Inicia convertidor archivo de XML</ṕ>",60)
                    #papers = admin.getPapers(modelo_proyecto.id_proyecto)
                    adminBD = AdminBD()
                    papers =adminBD.getPapers(modelo_proyecto.id_proyecto)
                    target = open(REPOSITORY_DIR+ str(request.user.username)+ "." + str(modelo_proyecto.id_proyecto) + "/busqueda1.xml", 'w')
                    target.write(funciones.papersToXML(papers))
                    target.close()
                    # print str(funciones.papersToXML(papers))
                    # funciones.papersToXML(papers).write(REPOSITORY_DIR+ str(request.user.username)+ "." + str(modelo_proyecto.id_proyecto) + "/busqueda1.xml")

                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-primary'><span class='fa  fa-send fa-fw'></span>termina el convertidor archivo de XML</ṕ>",60)
                except:
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",64)
                    print traceback.format_exc()
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-danger'><span class='fa  fa-times fa-fw'></span><b>PROBLEMA:</b>Error al convertir archivo de XML</p>",64)

                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",64)
                    # print traceback.format_exc()                          

                

                try:
                    """
                        indexación
                    """
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-primary'><span class='fa  fa-send fa-fw'></span>Inicia la indexación</label></p>",64)
                    ir = ConsumirServicios.IR()
                    ir.indexar(str(request.user.username),str(modelo_proyecto.id_proyecto))
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-success'><span class='fa  fa-check fa-fw'></span>Indexacion terminada</p>",68)
                except:
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",64)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-danger'><span class='fa  fa-times fa-fw'></span><b>PROBLEMA:</b>La indexación no se puede completar</p>",64)
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",64)
                    # print traceback.format_exc()


           


                try:
                    """"
                        Analisis
                    """
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-primary'><span class='fa  fa-send fa-fw'></span>Inicia el Analisis</p>",66)
                    data = ConsumirServicios.consumir_analisis(str(request.user.username),str(modelo_proyecto.id_proyecto))
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-success'><span class='fa  fa-check fa-fw'></span>Analisis terminado</p>",68)
                except:
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",66)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-danger'><span class='fa  fa-times fa-fw'></span><b>PROBLEMA:</b> El Analisis no se puede completar</p>",66)
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",66)
                    # print traceback.format_exc()

                try:
                    """
                    Analisis de Redes Sociales
                    """
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-primary'><span class='fa  fa-send fa-fw'></span>Inicia el Analisis de Redes Sociales</p>",70)
                    network = ConsumirServicios.consumir_red(str(request.user.username),str(modelo_proyecto.id_proyecto))
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-success'><span class='fa  fa-check fa-fw'></span>Analisis de Redes Sociales terminado</p>",72)
                except:
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",70)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-danger'><span class='fa  fa-times fa-fw'></span><b>PROBLEMA:</b>El Analisis de Redes Sociales no se puede completar</p>",70)
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",70)
                    #print traceback.format_exc()

                try:
                    """
                    Recuperacion de unidades
                    """                    
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-primary'><span class='fa  fa-send fa-fw'></span>Inicia la recuperacion de unidades academicas</p>",10)
                    # ConsumirServicios.consumir_recuperacion_unidades_academicas(str(request.user.username),str(modelo_proyecto.id_proyecto))
                    # cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-success'><span class='fa  fa-check fa-fw'></span>Finaliza la recuperacion de unidades academicas</p>",10)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,True,"",80)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-success'><span class='fa  fa-check fa-fw'></span>Se ha creado el proyecto</p>",90)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-success'><span class='fa  fa-check fa-fw'></span>Su navegador se reiniciara</p>",97)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"EOF",100)
                except:
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"<p class='text-danger'><span class='fa  fa-times fa-fw'></span><b>PROBLEMA:</b> la recuperacion de unidades academicas no se puede completar: {}</p>".format(traceback.format_exc()),80)
                    cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"EOF",100)
                    # print traceback.format_exc() 

                # messages.success(request, "Se ha creado exitosamente el proyecto")
                #articulos = funciones.buscadorSimple(fraseB)
                #ac = AdministradorConsultas()
                #ac.descargar_papers(fraseB)
                #lista_scopus = ac.titulos_descargas
            #if fraseA != "" or autor != "" or words != "":
            #    articulos = funciones.buscadorAvanzado(fraseA, words, autor, after, before)
            #print articulos
            #funciones.moveFiles(modelo_proyecto.id_proyecto, request.user, articulos, lista_scopus)
            #funciones.escribir_archivo_documentos(modelo_proyecto.id_proyecto, request.user, articulos, lista_scopus)
            # messages.success(request, "Se ha creado exitosamente el proyecto")
            #~ return redirect('crear_proyecto')
        else:
            messages.error(request, "Imposible crear el proyecto")
    else:
        form = FormularioCrearProyecto()
        

    return render(request, 'GestionProyecto/NuevoProyecto.html', {'form': form,
                'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos}, context_instance=RequestContext(request))


#Visualización de proyectos propios de un usuario.
@login_required
def ver_mis_proyectos(request):
    global model_proyecto
    global proyectos_list
    try:
        proyectos_list = get_list_or_404(proyecto, idUsuario=request.user)
    except: 
        proyectos_list =None
        messages.success(request, "Usted no tiene proyectos")

    return render(request, 'GestionProyecto/verMisProyectos.html', {'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos}, context_instance=RequestContext(request))


#Visualización de proyectos con disponibilidad pública que no pertenecen al usuario actual.
@login_required
def ver_otros_proyectos(request):
    global model_proyecto
    global proyecto_list

    if (model_proyecto != None and model_proyecto.idUsuario != request.user):
        model_proyecto = None
    try:
        proyectos_list_all = get_list_or_404(proyecto)
        idUser = request.user
        otros_proyectos = []
        for project in proyectos_list_all:
            if project.idUsuario != idUser:
                otros_proyectos.append(project)
    except:
        proyectos_list_all =None
        otros_proyectos = None


    return render(request, 'GestionProyecto/OtrosProyectos.html', {
        'proyectos': otros_proyectos, 'proyectos_user':proyectos_list, 'mproyecto': model_proyecto}, context_instance=RequestContext(request))


@login_required
def busqueda_navegacion(request):
    global proyectos_list
    global model_proyecto
    return render(request, 'GestionBusqueda/Busqueda_Navegacion.html', {'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})


@login_required
def editar_proyecto(request, id_proyecto):
    global proyectos_list
    global model_proyecto
    model_proyecto = get_object_or_404(proyecto, id_proyecto=id_proyecto)
    request.session['proyecto']= str(model_proyecto.id_proyecto)
    request.proyecto = model_proyecto
    # print  "This is my project:",request.session['proyecto']
    lista = funciones.crearListaDocumentos(id_proyecto, request.user)
    if request.method == 'POST':
        proyecto_form = FormularioCrearProyecto(request.POST, instance=model_proyecto)
        #proyecto_form.fields['disponibilidad'].widget.attrs['disabled']=True
        if proyecto_form.is_valid:
            #print proyecto_form.cleaned_data
            #nuevoNombre=proyecto_form.cleaned_data['nombre']
            model_project = proyecto_form.save()
            #    funciones.cambiarNombreDirectorio(nombreDirectorioAnterior,nuevoNombre,request.user)
            messages.success(request, "Se ha modificado exitosamente el proyecto")
        else:
            messages.error(request, "Imposible editar el proyecto")
    else:
        proyecto_form = FormularioCrearProyecto(instance=model_proyecto)
    return render(request, 'GestionProyecto/editar_proyecto.html',
                  {'form': proyecto_form, 'lista': lista, 'user': request.user, 'mproyecto':model_proyecto, 'proyectos_user': proyectos_list, 'proyecto': id_proyecto, 'lista_permisos': permisos},
                  context_instance=RequestContext(request))




@login_required
def ver_proyecto(request, id_proyecto):
    global model_proyecto
    global proyectos_list

    proyecto_actual = None
    proyecto_actual = get_object_or_404(proyecto, id_proyecto=id_proyecto)
    proyecto_form = FormularioCrearProyecto(instance=proyecto_actual)

    if (model_proyecto != None and model_proyecto.idUsuario != request.user):
        model_proyecto = None

    #model_proyecto = get_object_or_404(proyecto, id_proyecto=id_proyecto)
    #proyecto_form = FormularioCrearProyecto(instance=model_proyecto)
    #proyecto_form.fields['disponibilidad'].widget.attrs['disabled']=True
    #proyecto_form.fields['nombre'].label="Titulo del proyecto"
    proyecto_form.fields['nombre'].widget.attrs['disabled'] = True
    proyecto_form.fields['resumen'].widget.attrs['disabled'] = True

    return render(request, 'GestionProyecto/ver_proyecto.html', {'form': proyecto_form, 'mproyecto':model_proyecto, 'proyectos_user':proyectos_list, 'lista_permisos': permisos},
                  context_instance=RequestContext(request))


@login_required
def buscador(request):
    global proyectos_list
    global model_proyecto
    if request.method == 'GET':
        ir = ConsumirServicios.IR()

        fraseBusqueda = request.GET.get("busquedaIR")
        data = ir.consultar(fraseBusqueda,str(request.user.username), str(model_proyecto.id_proyecto))
        # print model_proyecto
        # IR.consultar(fraseBusqueda,"","")
      #  data = ir.consultar(fraseBusqueda,str(request.user.username),request.session['proyecto'])

        #data = funciones.busqueda(fraseBusqueda)
        #for d in data:
        #    d['path'] = d['path'].replace("/home/vigtech/shared/repository/", "/media/").encode("utf8")
        # print data
        # print fraseBusqueda
        return render(request, "GestionBusqueda/Busqueda_Navegacion.html", {'resultados': data, 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    else:
        return render(request, "GestionBusqueda/Busqueda_Navegacion.html", {'resultados': data, 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto,'lista_permisos': permisos})


@login_required
def analisisView(request):
    global proyectos_list
    global model_proyecto

    #data = ConsumirServicios.consumir_red(request.user.username, request.session['proyecto'])
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
        with open(REPOSITORY_DIR + proyecto + "/coautoria.json") as json_file:
            data = json.load(json_file)
        #nodos, aristas = r.generar_json()
        nodos1 = json.dumps(data['nodes'])
        aristas1 = json.dumps(data['links'])

   # return render(request, "GestionAnalisis/coautoria.html", {"nodos": nodos1, "aristas": aristas1})
        return render(request, "GestionAnalisis/coautoria.html", {"nodos": nodos1, "aristas": aristas1, 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto,'lista_permisos': permisos})
    #return render(request, "GestionAnalisis/coautoria2.html", {"proyecto":proyecto})
@login_required
def coautoria_old(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
        with open(REPOSITORY_DIR + proyecto + "/coautoria.json") as json_file:
            data = json.load(json_file)



        #nodos, aristas = r.generar_json()
        nodos1 = json.dumps(data['nodes'])
        aristas1 = json.dumps(data['links'])

       # return render(request, "GestionAnalisis/coautoria.html", {"nodos": nodos1, "aristas": aristas1})
        return render(request, "GestionAnalisis/Analisis.html", {"nodos": nodos1, "aristas": aristas1, 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
        
@login_required
def eliminar_proyecto(request, id_proyecto):
    global model_proyecto
    global proyectos_list
    try:
        # print "#1"
        proyectos_list = get_list_or_404(proyecto,  idUsuario=self.request.user)
        # print "#2"
        model_proyecto = get_object_or_404(proyecto, id_proyecto=str(self.request.session['proyecto']))
        # print "#3"   
    except:
        proyectos_list = None
        model_proyecto = None


    user = request.user
    project = get_object_or_404(proyecto, id_proyecto=id_proyecto)
    funciones.eliminar_proyecto(id_proyecto, user)
    project.delete()
    messages.success(request, "El proyecto \""+project.nombre+"\" se elimino.")
    return HttpResponseRedirect(reverse('ver_mis_proyectos'))

@login_required
def analisis_paises(request):
    global proyectos_list
    global model_proyecto
    # print model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
        with open(REPOSITORY_DIR+ proyecto + "/data.json") as json_file:
            data = json.load(json_file)
            # print data
        labels=json.dumps(data['paises']['labels'])
        values=json.dumps(data['paises']['valores'])
        # print proyecto
        #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
        return render(request, "GestionAnalisis/paisesbar.html",{"proyecto":proyecto, 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})

@login_required
def analisis_autores(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
        return render(request, "GestionAnalisis/autoresbar.html",{"proyecto":proyecto,'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
@login_required
def analisis_afiliaciones(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
        return render(request, "GestionAnalisis/afiliacionesbar.html",{"proyecto":proyecto,'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
@login_required
def analisis_revistas(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
        return render(request, "GestionAnalisis/revistasbar.html",{"proyecto":proyecto,'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
@login_required
def analisis_docsfechas(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
        return render(request, "GestionAnalisis/fechasbar.html",{"proyecto":proyecto,'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})

@login_required
def analisis_tipodocs(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
        return render(request, "GestionAnalisis/tiposbar.html",{"proyecto":proyecto,'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})

@login_required
def analisis_paisespie(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
        return render(request, "GestionAnalisis/paisespie.html",{"proyecto":proyecto,'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})

@login_required
def analisis_autorespie(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
        return render(request, "GestionAnalisis/autorespie.html",{"proyecto":proyecto, 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})

@login_required
def analisis_afiliacionespie(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
        return render(request, "GestionAnalisis/afiliacionespie.html",{"proyecto":proyecto,'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})

    except:
        return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})

@login_required
def analisis_revistaspie(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
        return render(request, "GestionAnalisis/revistaspie.html",{"proyecto":proyecto, 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})

@login_required
def analisis_docsfechaspie(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
        return render(request, "GestionAnalisis/fechaspie.html",{"proyecto":proyecto,'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})

@login_required
def analisis_tipodocspie(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
        return render(request, "GestionAnalisis/tipospie.html",{"proyecto":proyecto, 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
        return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})

@login_required
def analisis_clustering(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
        return render(request, "GestionAnalisis/grupos.html",{"proyecto":proyecto, 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
        return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
    

@login_required
def analisis_indicadores(request):
    global proyectos_list
    global model_proyecto
    try:
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        with open(REPOSITORY_DIR + proyecto + "/data.json") as json_file:
            data = json.load(json_file)
        return render(request, "GestionAnalisis/indicadores.html",{"data":data, 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
        print traceback.format_exc()
        return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
        

        # print data
    #labels=json.dumps(data['paises']['labels'])
    #values=json.dumps(data['paises']['valores'])
    #print proyecto
    #return render(request, "GestionAnalisis/paisesbar.html",{"labels": labels, "values": values})
    #return render(request, "GestionAnalisis/indicadores.html",{"data":data, 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto})

@login_required
def clasificacion_eisc(request):
    global proyectos_list
    global model_proyecto
    try:
        proyecto = str(request.user.username) + "." + str(model_proyecto.id_proyecto)
        #proyecto = str(request.user.username) + "." + str(request.session['proyecto'])
        with open(REPOSITORY_DIR + proyecto + "/eisc.json") as json_file:
            data = json.load(json_file)
        eids = data['clasificacion']
        if eids :
            adminBD = AdminBD()
            papers =adminBD.get_papers_eid(eids)
            return render (request, "GestionEISC/clasificacion_eisc.html", {"papers": papers, 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
        else:
            return render (request, "GestionEISC/clasificacion_eisc.html", {"papers": [], 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})
    except:
         return render(request, "GestionAnalisis/Blank_default.html", { 'proyectos_user': proyectos_list, 'mproyecto': model_proyecto, 'lista_permisos': permisos})



def logmensajes(request):
    """ 
    Permite consultar el estado del proceso de creacion de 
    un nuevo proyecto 
    """
    try:
        cache_key = "%s_%s_%s" % (request.GET.get('csrfmiddlewaretoken'),request.GET.get('fraseB').replace(" ",""),request.user.username)        
        data = json.dumps(cache.get(cache_key))
        print cache.get(cache_key)['estado']
        cache.set(cache_key, {'estado': cache.get(cache_key)['estado'],'mensaje' : ""})
    except:
        print "hay problema"
        cambia_mensaje(request.POST.get('csrfmiddlewaretoken'),request.POST.get('fraseB'),request.user.username,False,"",0)
    return HttpResponse(data,content_type="application/json")


# Configuración de los permisos --links a mostrar alozada
@login_required
def configurar_permisos(request):
    global model_proyecto
    global proyectos_list
    # print permisos["estadisticas"]
    try:
        proyectos_list = get_list_or_404(proyecto, idUsuario=request.user)
    except: 
        proyectos_list =None
        messages.success(request, "Usted no tiene proyectos")
    if request.method == 'POST':
        if 'cbIndicadores' in request.POST:
            permisos["indicadores"] = 1
        else:
            permisos["indicadores"] = 0

        if 'graficos_barra' in request.POST:
            permisos["graficos_barra"] = 1
        else:
            permisos["graficos_barra"] = 0

        if 'graficos_pie' in request.POST:
            permisos["graficos_pie"] = 1
        else:
            permisos["graficos_pie"] = 0

        if not ('cbIndicadores' in request.POST and 'graficos_barra' in request.POST and 'graficos_pie' and request.POST):
            print "entra if"
            permisos["estadisticas"] = 0
        else:
            print "entra else"
            permisos["estadisticas"] = 1    

        if 'coautoria' in request.POST:
            permisos["coautoria"] = 1
        else:
            permisos["coautoria"] = 0

        if 'coautoria_medidas' in request.POST:
            permisos["coautoria_medidas"] = 1
        else:
            permisos["coautoria_medidas"] = 0

        if 'clustering' in request.POST:
            permisos["clustering"] = 1
        else:
            permisos["clustering"] = 0

        if 'clasificacion_eisc' in request.POST:
            permisos["clasificacion_eisc"] = 1
        else:
            permisos["clasificacion_eisc"] = 0



    return render(request, 'configurar_permisos.html', {'proyectos_user': proyectos_list, 'lista_permisos': permisos, 'mproyecto': model_proyecto}, context_instance=RequestContext(request))



# def registrarusuario(request):
#     if request.method == 'GET':
#         return render(request, "registrarUsuario.html")
#     elif request.method == 'POST':
#         data = request.POST.get('nombre')
#         print data        
#         # messages.success(request, "Se ha creado exitosamente el usuario")
#         # return redirect('login')
#         return render (request, "registrarUsuario.html", {"response": data})        
#     else:
#         return render(request, "registrarUsuario.html")
