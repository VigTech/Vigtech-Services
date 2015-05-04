# -*- encoding: utf-8 -*-

from django.shortcuts import render, render_to_response, redirect, get_object_or_404, get_list_or_404, Http404
from django.views.generic import TemplateView, FormView
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.contrib import messages
from django.template import RequestContext
from .forms import *
import funciones
import sys
from administradorConsultas import AdministradorConsultas
from manejadorArchivos import obtener_autores
from red import Red
# import igraph
import json
import django.utils

# sys.setdefaultencoding is cancelled by site.py
reload(sys)  # to re-enable sys.setdefaultencoding()
sys.setdefaultencoding('utf-8')
# Create your views here.
# @login_required

ruta = "/home/administrador/ManejoVigtech/ArchivosProyectos/"


class home(TemplateView):
    template_name = "home.html"


class RegistrarUsuario(FormView):
    template_name = "registrarUsuario.html"
    form_class = FormularioRegistrarUsuario
    success_url = reverse_lazy('RegistrarUsuarios')

    def form_valid(self, form):
        user = form.save()
        messages.success(self.request, "Se ha creado exitosamente el usuario")
        return redirect('login')


@login_required
def nuevo_proyecto(request):
    if request.method == 'POST':
        form = FormularioCrearProyecto(request.POST)
        fraseB = request.POST.get('fraseB')
        fraseA = request.POST.get('fraseA')
        autor = request.POST.get('autor')
        words = request.POST.get('words')
        before = request.POST.get('before')
        after = request.POST.get('after')
        #print fraseB
        #Formato de frase de busqueda
        #FraseBásica,Words,FraseA,autor,before,after
        busqueda = fraseB + "," + words + "," + fraseA + "," + autor + "," + before + "," + after
        if form.is_valid():
            nombreDirectorio = form.cleaned_data['nombre']
            articulos = {}
            modelo_proyecto = form.save(commit=False)
            modelo_proyecto.idUsuario = request.user
            #modelo_proyecto.calificacion=5
            modelo_proyecto.fraseBusqueda = busqueda
            modelo_proyecto.save()

            #Creacion del directorio donde se guardaran los documentos respectivos del proyecto creado.

            funciones.CrearDirectorioProyecto(modelo_proyecto.id_proyecto, request.user)
            if fraseB != "":
                articulos = funciones.buscadorSimple(fraseB)
                ac = AdministradorConsultas()
                ac.descargar_papers(fraseB)
                lista_scopus = ac.titulos_descargas

            #if fraseA != "" or autor != "" or words != "":
            #    articulos = funciones.buscadorAvanzado(fraseA, words, autor, after, before)


            #print articulos


            #print str(modelo_proyecto.id_proyecto)

            funciones.moveFiles(modelo_proyecto.id_proyecto, request.user, articulos, lista_scopus)
            funciones.escribir_archivo_documentos(modelo_proyecto.id_proyecto, request.user, articulos, lista_scopus)
            messages.success(request, "Se ha creado exitosamente el proyecto")
            return redirect('crear_proyecto')
        else:
            messages.error(request, "Imposible crear el proyecto")
    else:
        form = FormularioCrearProyecto()
    return render(request, 'GestionProyecto/NuevoProyecto.html', {'form': form})


#Visualización de proyectos propios de un usuario.
@login_required
def ver_mis_proyectos(request):
    try:
        proyectos_list = get_list_or_404(proyecto, idUsuario=request.user)
    except proyecto.DoesNotExist:
        raise Http404
    return render(request, 'GestionProyecto/verMisProyectos.html', {
        'proyectos': proyectos_list}, context_instance=RequestContext(request))


#Visualización de proyectos con disponibilidad pública que no pertenecen al usuario actual.
@login_required
def ver_otros_proyectos(request):
    try:
        proyectos_list = get_list_or_404(proyecto)
        idUser = request.user
        otros_proyectos = []
        for project in proyectos_list:
            if project.idUsuario != idUser:
                otros_proyectos.append(project)

    except proyecto.DoesNotExist:
        raise Http404
    return render(request, 'GestionProyecto/OtrosProyectos.html', {
        'proyectos': otros_proyectos}, context_instance=RequestContext(request))


@login_required
def busqueda_navegacion(request):
    return render(request, 'GestionBusqueda/Busqueda_Navegacion.html')


@login_required
def editar_proyecto(request, id_proyecto):
    model_proyecto = get_object_or_404(proyecto, id_proyecto=id_proyecto)
    #nombreDirectorioAnterior=model_proyecto.nombre
    lista = funciones.crearListaDocumentos(id_proyecto, request.user, )
    if request.method == 'POST':
        proyecto_form = FormularioCrearProyecto(request.POST, instance=model_proyecto)
        #proyecto_form.fields['disponibilidad'].widget.attrs['disabled']=True
        if proyecto_form.is_valid:
            #print "Hola mundo"
            #print proyecto_form.cleaned_data
            #nuevoNombre=proyecto_form.cleaned_data['nombre']
            model_project = proyecto_form.save()
            #	funciones.cambiarNombreDirectorio(nombreDirectorioAnterior,nuevoNombre,request.user)
            messages.success(request, "Se ha modificado exitosamente el proyecto")
        else:
            messages.error(request, "Imposible editar el proyecto")
    else:
        proyecto_form = FormularioCrearProyecto(instance=model_proyecto)

    return render(request, 'GestionProyecto/editar_proyecto.html',
                  {'form': proyecto_form, 'lista': lista, 'user': request.user, 'proyecto': id_proyecto},
                  context_instance=RequestContext(request))


@login_required
def ver_proyecto(request, id_proyecto):
    model_proyecto = get_object_or_404(proyecto, id_proyecto=id_proyecto)
    proyecto_form = FormularioCrearProyecto(instance=model_proyecto)
    #proyecto_form.fields['disponibilidad'].widget.attrs['disabled']=True
    #proyecto_form.fields['nombre'].label="Titulo del proyecto"
    proyecto_form.fields['nombre'].widget.attrs['disabled'] = True
    proyecto_form.fields['resumen'].widget.attrs['disabled'] = True

    return render(request, 'GestionProyecto/ver_proyecto.html', {'form': proyecto_form},
                  context_instance=RequestContext(request))


@login_required
def buscador(request):
    if request.method == 'GET':
        fraseBusqueda = request.GET.get("busquedaIR")
        data = funciones.busqueda(fraseBusqueda)
        print data
        print fraseBusqueda
    else:
        print "Hi"
    return render(request, "GestionBusqueda/Busqueda_Navegacion.html", {'resultados': data})


@login_required
def analisisView(request):
    print 'hola'
    diccionario_autores = obtener_autores([open('busqueda.xml')])
    lista_autores = []
    lista_nombres = []
    for autor in diccionario_autores:
        lista_autores.append(diccionario_autores[autor])
        lista_nombres.append(autor)
    r = Red(lista_autores, 'autores3', lista_nombres)
    nodos, aristas = r.generar_json()
    nodos1 = json.dumps(nodos)
    aristas1 = json.dumps(aristas)
    #return render(request, "GestionAnalisis/Analisis.html", {"nodos":nodos, "aristas":aristas})
    return render(request, "GestionAnalisis/Analisis.html", {"nodos": nodos1, "aristas": aristas1})
