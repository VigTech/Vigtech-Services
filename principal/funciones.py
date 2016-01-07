import scholar
import os
import json
import urllib
import xml.etree.cElementTree as ET
from principal.parameters import *




# REPOSITORY_DIR = '/home/japeto/shared/repository/'
REPOSITORY_DIR = REPOSITORY_DIR
def buscadorSimple(frase):
    # nombre_directorio=str(id_user)+ "."+ str(id_proyecto)
    querier = scholar.ScholarQuerier()

    settings = scholar.ScholarSettings()

    query = scholar.SearchScholarQuery()

    query.set_phrase(frase)
    query.set_num_page_results(40)

    querier.send_query(query)
    scholar.getArticles(querier)

    articles = querier.articles
    articulos = getArticlesDict(articles)
    # MOVER ARTICULOS A CARPETA TMP
    #if articulos is not None:
    #	moveFiles()
    #	indexarArchivos()
    return articulos


def buscadorAvanzado(frase, words, autor, after, before):
    # nombre_directorio= str(id_user)+ "."+ str(id_proyecto)
    querier = scholar.ScholarQuerier()
    settings = scholar.ScholarSettings()
    query = scholar.SearchScholarQuery()
    if frase != "":
        query.set_phrase(frase)
    if words != "":
        query.set_words(words)
    if autor != "":
        query.set_author(autor)
    if after != "" or before != "":
        query.set_timeframe(after, before)

    query.set_num_page_results(40)
    querier.send_query(query)
    scholar.getArticles(querier)
    articles = querier.articles

    articulos = getArticlesDict(articles)

    # if articulos is not None:
    #	moveFiles()
    #	indexarArchivos()
    return articulos


def getArticlesDict(articles):
    articulos = []
    for art in articles:

        titulo = art.attrs["title"][0]
        # print(titulo)
        url = art.attrs["url"][0]
        url_pdf = art.attrs["url_pdf"][0]
        # state =art.attrs['state'][0]
        #testFile=urllib.URLopener()
        if url_pdf is not None:
            newArt = {'titulo': titulo, 'url': url, 'url_pdf': url_pdf}
            articulos.append(newArt)
            # print (newArt['titulo'] + '\n')

    return articulos

#Recibe la lista del contedor especifico.
def moveFiles(nombreProyecto, user, articulosScholar, articulosScopus):
    rutaProyecto = str(user) + "." + str(nombreProyecto)
    items = os.listdir(os.getcwd())

    lista = []
    for art in articulosScholar:
        if art['titulo'] != "NO ACCESIBLE":
            lista.append(art['titulo'] + ".pdf")

    for art in articulosScopus:
        if art is not None:
            lista.append(art + ".pdf")
    lista = set(lista)

    # os.listdir(os.getcwd())
    for art in lista:
        nombre = art.replace(" ", "\\ ")
        os.system("mv -f " + nombre + " " + rutaProyecto + "/")

    '''
	for files in items:
		if files.endswith(".pdf"):
			preName=str(files).replace(" ","\\ ")
			os.system("mv -f " + preName + " " + rutaProyecto+"/" )
			'''
    os.system("mv " + rutaProyecto + "/" + " /home/administrador/ManejoVigtech/media/")


# os.system("mv " + rutaProyecto+ "/" + " static/"+rutaProyecto+"/")

def indexarArchivos():
    ejecutar = "java -jar /home/administrador/OlayaVigtech/Indexador/Indexador.jar /home/administrador/OlayaVigtech/indices/ /home/administrador/archivos"
    # print "Indexando..."
    os.system(ejecutar)
    # print "Indexacion terminada..."


def CrearDirectorioProyecto(nombreProyecto, user):
    nombreDirectorio = str(user) + "." + str(nombreProyecto)
    # Creacion de directorios de proyectos.
    #Ruta en el host
    os.mkdir(REPOSITORY_DIR+nombreDirectorio, 0777)
    os.chmod(REPOSITORY_DIR+nombreDirectorio, 0777)


# os.system("mkdir /home/administrador/ManejoVigtech/ArchivosProyectos/ " + nombreDirectorio)

def cambiarNombreDirectorio(nombreAnterior, nuevoNombre, user):
    nombreDirectorioAnterior = str(user) + "." + str(nombreAnterior.replace(" ", ""))
    nombreDirectorioNuevo = str(user) + "." + str(nuevoNombre.replace(" ", ""))

    os.system("mv" + nombreDirectorioAnterior + "/ " + nombreDirectorioNuevo + "/")


def busqueda(consulta):
    ruta_indeces = "Busquedas/asdIndices"
    ruta_json = "Busquedas/"
    ruta_jar = "Busquedas/dist/JSONConverter.jar"
    try:
        os.system("java -jar " + ruta_jar + " " + consulta + " " + ruta_indeces + " " + ruta_json)
        json_data = open(ruta_json + "prueba.txt")
        data = json.load(json_data)

        return data
    except Exception, e:
        raise e


def crearListaDocumentos(id_proyecto, user):

    archivo = open(REPOSITORY_DIR + str(user) + "." + str(id_proyecto) + "/" + "docs.txt",
                   "r")
    lista = []
    for linea in archivo:
        lista.append(linea.rstrip())
    return lista

def eliminar_proyecto(id_proyecto, user):
    os.system("rm -rf " + REPOSITORY_DIR + str(user) + "." + str(id_proyecto))
    os.system("rm -rf " + REPOSITORY_INDEXES  + str(user) + "." + str(id_proyecto))

def escribir_archivo_documentos(id_proyecto, user, articulosScholar, articulosScopus):
    lista = []
    for art in articulosScholar:
        if art['titulo'] != "NO ACCESIBLE":
            lista.append(art['titulo'] + ".pdf")

    for art in articulosScopus:
        if art is not None:
            lista.append(art + ".pdf")
    lista = set(lista)
    #pdfs = open("static/"+str(user)+"."+str(id_proyecto)+"/"+"docs.txt", "w")
    pdfs = open("/home/administrador/ManejoVigtech/media/" + str(user) + "." + str(id_proyecto) + "/" + "docs.txt", "w")
    for pdf in lista:
        if pdf is not None:
            pdfs.write(pdf + '\n')

#funciones para los script

def dict_to_xml(tag, d):
    '''
    Turn a simple dict of key/value pairs into XML
    '''
    tag = tag.replace('__', '-').replace('_', ':')
    elem = ET.Element(tag)
    for key, val in d.items():
        key = key.replace('__', '-').replace('_', ':')
        child = ET.Element(key)
        child.text = unicode(str(val), "utf-8") if val else ''
        elem.append(child)
    return elem

def paperToXML(paper):
    entry = ET.Element("entry")
    for key in paper:
        xml_key = key.replace('__', '-')
        xml_key = xml_key.replace('_', ':')
        if key == 'affiliation':
            elem = dict_to_xml(xml_key, paper[key])
            entry.append(elem)
            continue
        if key == 'authors':
            for author in paper[key]:
                elem = dict_to_xml('author', author)
                entry.append(elem)
            continue
        ET.SubElement(entry, xml_key).text = unicode(str(paper[key]), "utf-8") if paper[key] else ''
    return entry

def papersToXML(papers):
    root = ET.Element("search-results")
    root.set('xmlns', 'http://www.w3.org/2005/Atom')
    root.set('xmlns:cto', 'http://www.elsevier.com/xml/cto/dtd')
    root.set('xmlns:atom', 'http://www.w3.org/2005/Atom')
    root.set('xmlns:prism', 'http://prismstandard.org/namespaces/basic/2.0/')
    root.set('xmlns:opensearch', 'http://a9.com/-/spec/opensearch/1.1/')
    root.set('xmlns:dc', 'http://purl.org/dc/elements/1.1/')
    for paper in papers:
        root.append(paperToXML(paper))

    return ET.tostring(root)
    # ET.dump(root)
