#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from conectarBD import insertar_paper

def obtener_metadatos(xml, etiquetas_paper, etiquetas_revista, etiquetas_autor):
    '''Guarda los datos de un xml en una base de datos
    Parámetros: Los nombres de los campos que son guardados en cada tabla'''
    respuesta = []
    tree = ET.parse(xml)
    root = tree.getroot()
    for child in root:
        #Allí se guardan los datos de cada tabla que se insertan por paper
        paper = {}
        revista = {}
        autores = []
        for campito in child:#.findall(campo):
            registrar(campito, paper, etiquetas_paper)
            registrar(campito, revista, etiquetas_revista)
            registrar_autores(campito,autores,etiquetas_autor)
            #print campito.text
            #print campito.tag
            respuesta.append(campito.text)
        #print revista
        print autores
        if(paper != {}):
            insertar_paper(paper, autores)
    return respuesta

def registrar_autores(campito, autores, etiquetas_autor):
    tag_autor = '{http://www.w3.org/2005/Atom}author'
    if campito.tag == tag_autor:
        autor = {}
        for meta_autor in campito:
            registrar(meta_autor, autor, etiquetas_autor)
            autores.append(autor)
            #print meta_autor.tag

def registrar(campito, paper, etiquetas_metadatos):
    '''Guarda en paper, un diccionario que contiene los datos de campito etiquetados con etiquetas_metadatos
    Parámetros:
    Campito: Un objeto del lector de xml que contiene los datos de una de las ramificaciones.
    paper: variable en la que se va almacenando el diccionario con los datos
    etiquetas_metadatos: Lista con los tags de los metadatos que vamos a guardar'''
    for metadato in etiquetas_metadatos:
        nombre_meta = metadato.partition('}')[2]
        if(paper.get(nombre_meta) == None):
            paper[nombre_meta] = 'null'
        if metadato == campito.tag:
            #print 'fue'
            #print campito.text
            if campito.text is not None:
				paper[nombre_meta] = campito.text.replace("'", " ").encode('utf-8')

def xml_to_bd(xml):
    etiquetas_paper = ['{http://purl.org/dc/elements/1.1/}title', '{http://purl.org/dc/elements/1.1/}description',
                 '{http://prismstandard.org/namespaces/basic/2.0/}doi', '{http://prismstandard.org/namespaces/basic/2.0/}issn',
                 '{http://www.w3.org/2005/Atom}citedby-count', '{http://www.w3.org/2005/Atom}eid',
                 '{http://prismstandard.org/namespaces/basic/2.0/}coverDate']
    etiquetas_revista = ['{http://prismstandard.org/namespaces/basic/2.0/}publicationName',
                         '{http://prismstandard.org/namespaces/basic/2.0/}issn']
    etiquetas_autor= ['{http://www.w3.org/2005/Atom}authid', '{http://www.w3.org/2005/Atom}authname',
                      '{http://www.w3.org/2005/Atom}afid']

    obtener_metadatos(xml, etiquetas_paper, etiquetas_revista, etiquetas_autor)
    return 0

#xml_to_bd(open('xml0.xml'))
#main(open('xml0.xml'))
