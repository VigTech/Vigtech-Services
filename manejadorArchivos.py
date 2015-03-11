# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
'''Este módulo sirve para leer archivos y convertirlos en listas.'''


def escribir_archivo(lista):
    pdfs = open('listaPdfs', 'w')
    for pdf in lista:
        pdfs.write(pdf+'\n')

def leer_archivo(archivo, eliminar_primero=False):
    '''Convierte un archivo a una lista, línea a línea

    Parámetros:
    Si eliminar_primero es True, entonces no se tiene en cuenta la primera línea del archivo

    '''
    lista = []
    if eliminar_primero:
        archivo.readline()
    for linea in archivo:
        lista.append(linea.rstrip())
    return lista

def obtener_autores(xmls):

    autores = {}
    documento = 0
    for xml in xmls:
        tree = ET.parse(xml)
        root = tree.getroot()
        documento = documento - 9
        for child in root:
            documento += 1
            for eid in child.findall('{http://www.w3.org/2005/Atom}eid'):
                id = eid.text
                print eid.text
            for authors in child.findall('{http://www.w3.org/2005/Atom}author'):
                for child2 in authors.findall('{http://www.w3.org/2005/Atom}authname'):
                    print child2.tag, child2.text, documento
                    autor = child2.text.encode('utf-8')
                    if(autores.get(autor) == None):
                        autores[autor] = []
                    autores[autor].append(id)
    print autores
    print len(autores)
    return autores

def dicci_to_list(dicci):
    list = []
    for autor in dicci:
        list.append(dicci[autor])
    return list
#obtener_autores([open('XMLs/xml0.xml'),open('XMLs/xml1.xml'),open('XMLs/xml2.xml'),open('XMLs/xml3.xml')])