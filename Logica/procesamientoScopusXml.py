#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from conectarBD import insertar_paper

def obtener_metadatos(xml, etiquetas_paper, etiquetas_revista, etiquetas_autor, etiquetas_afiliaciones, etiquetas_keys, id_proy):
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
        afiliaciones = []
        keys = {}
        for campito in child:#.findall(campo):
            registrar(campito, paper, etiquetas_paper)
            registrar(campito, revista, etiquetas_revista)
            registrar(campito, keys, etiquetas_keys)
            registrar_autores(campito,autores,etiquetas_autor,'{http://www.w3.org/2005/Atom}author')
            registrar_autores(campito,afiliaciones,etiquetas_afiliaciones,'{http://www.w3.org/2005/Atom}affiliation')
            print campito.tag, campito.text
            #print paper
            respuesta.append(campito.text)
        #Dividir las keywords en su diccionario
        #print keys
        keywords = dividir_diccionario_key(keys, etiquetas_keys)
        #print revista
        #print autores
        #print paper
        #print respuesta
        if(paper != {}):
            insertar_paper(paper, autores, revista, afiliaciones, keywords, id_proy)
    return respuesta

def registrar_autores(campito, autores, etiquetas_autor,tag):
    #print 'Hola'
    tag_autor = tag
    #print campito.tag, campito.text
    if campito.tag == tag_autor:
        #print 'hola2'
        #print autores
        autor = {}
        for meta_autor in campito:
            registrar(meta_autor, autor, etiquetas_autor)
            #print autor
            #print meta_autor.tag, meta_autor.text
        autores.append(autor)
            #print autor
            #print autores


def registrar(campito, paper, etiquetas_metadatos):
    '''Guarda en paper, un diccionario que contiene los datos de campito etiquetados con etiquetas_metadatos
    Parámetros:
    Campito: Un objeto del lector de xml que contiene los datos de una de las ramificaciones.
    paper: variable en la que se va almacenando el diccionario con los datos
    etiquetas_metadatos: Lista con los tags de los metadatos que vamos a guardar'''
    for metadato in etiquetas_metadatos:
        nombre_meta = metadato.partition('}')[2]
        if(paper.get(nombre_meta) == None):
            paper[nombre_meta] = '00000'
        if metadato == campito.tag:
            #print 'fue'
            #print campito.text
            if campito.text is not None:
				paper[nombre_meta] = campito.text.replace("'", " ").encode('utf-8')

def dividir_diccionario_key(keywords, etiquetas):
    keys_respuesta = []
    print 'hola', keywords
    if keywords != {}:
        etiqueta_key = etiquetas[0].partition('}')[2]
        keys = keywords[etiqueta_key].split('|')
        keys_respuesta = []
        for key in keys:
            keys_respuesta.append({etiqueta_key:key.strip()})
    return keys_respuesta






def xml_to_bd(xml, id_proyecto):
    etiquetas_paper = ['{http://purl.org/dc/elements/1.1/}title', '{http://purl.org/dc/elements/1.1/}description',
                 '{http://prismstandard.org/namespaces/basic/2.0/}doi', '{http://prismstandard.org/namespaces/basic/2.0/}issn',
                 '{http://www.w3.org/2005/Atom}citedby-count', '{http://www.w3.org/2005/Atom}eid',
                 '{http://prismstandard.org/namespaces/basic/2.0/}coverDate', '{http://prismstandard.org/namespaces/basic/2.0/}volume']
    etiquetas_revista = ['{http://prismstandard.org/namespaces/basic/2.0/}publicationName',
                         '{http://prismstandard.org/namespaces/basic/2.0/}issn']
    etiquetas_autor= ['{http://www.w3.org/2005/Atom}authid', '{http://www.w3.org/2005/Atom}authname',
                      '{http://www.w3.org/2005/Atom}afid']
    etiquetas_afiliaciones=['{http://www.w3.org/2005/Atom}afid','{http://www.w3.org/2005/Atom}affilname',
                           '{http://www.w3.org/2005/Atom}name-variant','{http://www.w3.org/2005/Atom}name-variant',
                           '{http://www.w3.org/2005/Atom}affiliation-city','{http://www.w3.org/2005/Atom}affiliation-country']
    etiquetas_keywords=['{http://www.w3.org/2005/Atom}authkeywords']

    #dividir_diccionario_key({"authkeywords":'Meta-language | Mobile robot | Programming environment | STEM'},etiquetas_keywords)
    obtener_metadatos(xml, etiquetas_paper, etiquetas_revista, etiquetas_autor, etiquetas_afiliaciones, etiquetas_keywords, id_proyecto)
    return 0

#xml_to_bd(open('xml1.xml'), 13)
#main(open('xml0.xml'))
