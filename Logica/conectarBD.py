# -*- coding: utf-8 -*-
import json
import psycopg2
from principal.parameters import *



def run_query(query=''):
    #conn_string = "host='localhost' dbname='postgres' user='postgres' password='chucho'"
    #conn_string = "host='127.0.0.1' dbname='docker' user='docker' password='docker' port='49153' client_encoding=UTF8"
    conn_string = "host="+HOST+" dbname="+DATABASE+ " user="+USER+" password="+PASSWORD+" port="+PORT+" client_encoding=UTF8"
    conn = psycopg2.connect(conn_string) # Conectar a la base de datos
    #$conn.set_character_encoding('utf8')
    cursor = conn.cursor()         # Crear un cursor
    cursor.execute(query)          # Ejecutar una consulta

    #Le inclui insert
    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()   # Traer los resultados de un select
    elif query.upper().startswith('INSERT') and 'RETURNING' in query.upper():
        conn.commit()              # Hacer efectiva la escritura de datos
        data = cursor.fetchall()   # Traer los resultados de un select
    else:
        conn.commit()              # Hacer efectiva la escritura de datos
        data = None

    cursor.close()                 # Cerrar el cursor
    conn.close()                   # Cerrar la conexion

    return data

def select(tabla):
    query = 'SELECT article, publication_year, id FROM "'+tabla+'" ORDER BY publication_year DESC'
    result = run_query(query)
    return result

def insertar_paper(paper, autores, revista, afiliaciones, keywords, id_proyecto):#, revista, keywords, autores):
    '''Inserta en la BD la informacion de un paper que viene en forma de listas para cada tabla de la BD
    '''
    #funcion_sql_ultimo_id = "SELECT currval('paper_id_seq');"
    #paper_query = "INSERT INTO paper (doi,titulo_paper, abstract, issn, fecha, revista_issn, total_citaciones) VALUES ('%s','%s','%s',%s,%s,%s,%s);"%(paper['doi'],paper['title'],paper['abstract'])
    #paper_query = "INSERT INTO paper (doi,titulo_paper, abstract) VALUES ('%s','%s','%s') RETURNING id;"%(paper['doi'],paper['title'],paper['description'])

    if revista['issn']!='00000':
        id_revista = insert_returning_id(revista, 'revista', 'issn', 'issn', 'id', ['issn', 'titulo_revista', 'isbn'],
                                        ['issn', 'publicationName', 'isbn'])
    elif revista['isbn']!='00000':
        id_revista = insert_returning_id(revista, 'revista', 'isbn', 'isbn', 'id', ['issn', 'titulo_revista', 'isbn'],
                                        ['issn', 'publicationName', 'isbn'])
    else:
        id_revista = insert_returning_id(revista, 'revista', 'publicationName', 'titulo_revista', 'id',
                                         ['issn', 'titulo_revista', 'isbn'], ['issn', 'publicationName', 'isbn'])

    # print 'hola'
    id_paper = insert_returning_id(paper, 'paper', 'eid', 'eid', 'id', ['eid', 'titulo_paper', 'abstract','total_citaciones',
                                                                        'fecha','doi', 'link_source'],
                                   ['eid', 'title', 'description','citedby-count','coverDate','doi','linkScopus'])


    for afiliacion in afiliaciones:
        id_afiliacion = insert_returning_id(afiliacion, 'afiliacion', 'afid', 'scopus_id', 'id',
                                        ['scopus_id', 'nombre', 'pais','ciudad','variante_nombre'],
                                        ['afid', 'affilname', 'affiliation-country','affiliation-city','name-variant'])
        insert_relation('paper_afiliacion', 'paper_id', 'afiliacion_id', id_paper, id_afiliacion)

    for autor in autores:
        '''
        lista_id_autor = select_id('autor', 'id_scopus', autor['authid'])
        if lista_id_autor:
            print 'denegado for autores'
            id_autor = lista_id_autor[0][0]
        else:
            paper_query = "INSERT INTO autor (id_scopus,nombre_autor) VALUES ('%s','%s') RETURNING id;"%(autor['authid'],autor['authname'])
            id_autor = run_query(paper_query)[0][0]
        '''
        id_autor = insert_returning_id(autor, 'autor', 'authid', 'id_scopus', 'id', ['id_scopus', 'nombre_autor'],
                                       ['authid', 'authname'])

        insert_relation('paper_autor', 'paper_id', 'autor_id', id_paper, id_autor)

        lista_id_aff = select_id('id', 'afiliacion', 'scopus_id', autor['afid'])
        if lista_id_aff:
            id_aff = lista_id_aff[0][0]
            insert_relation('autor_afiliacion','autor_id','afiliacion_id',id_autor,id_aff)

    for key in keywords:
        id_key = insert_returning_id(key, 'keyword', 'authkeywords', 'keyword', 'id', ['keyword'],
                                     ['authkeywords'])

        insert_relation('paper_keyword', 'paper_id', 'keyword_id', id_paper, id_key)

    insert_relation('paper_proyecto', 'id_paper', 'id_proyecto', id_paper, id_proyecto)

    #print type(paper_query)
    # print id_paper

def insert_returning_id(dicci_tabla, nombre_tabla, identificador_xml, identificador_bd, id_retorno, campos_bd, campos_xml):
    lista_id_paper = select_id(id_retorno, nombre_tabla, identificador_bd, dicci_tabla[identificador_xml])
    if lista_id_paper: 
        # Si el auto ya existe en la BD  se le asigna un nuevo id
        # print 'Asignando un nuevo ID  autor'
        id = lista_id_paper[0][0]
    else:
        string_campos = '%s,'*len(campos_bd)%tuple((campo for campo in campos_bd))
        #eliminar ultimo caracter por la coma
        string_campos = string_campos[:-1]
        string_valores = "'%s',"*len(campos_bd)%tuple((dicci_tabla[campo] for campo in campos_xml))
        #eliminar ultimo caracter por la coma
        string_valores = string_valores[:-1]
        paper_query = "INSERT INTO %s (%s) VALUES (%s) RETURNING %s;"%(nombre_tabla,string_campos, string_valores, id_retorno)
        # print paper_query
        id = run_query(paper_query)[0][0]
        # print id
    return id

def insert_relation(tabla, atrib_id1, atrib_id2, valor1, valor2):
    if not select_id2(tabla, atrib_id1, atrib_id2, valor1, valor2):
        autor_paper_query = "INSERT INTO %s (%s, %s) VALUES (%s,%s)"%(tabla,atrib_id1,atrib_id2,valor1,valor2)
        run_query(autor_paper_query)

def select_id(id, tabla, atrib_id, valor):
    query = "SELECT %s FROM %s WHERE %s = '%s'"%(id,tabla, atrib_id, valor)
    # print  query
    result = run_query(query)
    return result

def select_id2(tabla, atrib_id1, atrib_id2, valor1, valor2):
    query = "SELECT * FROM %s WHERE %s = %s AND %s = %s"%(tabla, atrib_id1, valor1, atrib_id2, valor2)
    result = run_query(query)
    return result

def actualizar(titulos):
    for titulo in titulos:
        query = "UPDATE paper SET descargo=TRUE WHERE titulo_paper='%s';"%(titulo.strip())
        run_query(query)
        #print 'Modificando descarg'

def buscar(datos, tabla_conjunto, campo):
    '''Busca los datos en la tabla de paper'''
    condiciones = ''
    for dato in datos:
        base = campo+" LIKE '%%%s%%' AND "
        ANDS = base*len(dato)%tuple((datin for datin in dato))#[:-]
        ANDS = ANDS[:-4]
        condiciones = condiciones + '('+ANDS +') OR '
    condiciones = condiciones[:-3]

    query = "SELECT titulo_paper FROM paper_%s,%s,paper WHERE (%s.id = %s_id AND paper.id = paper_id) AND ("%(tabla_conjunto,
                                                                        tabla_conjunto,tabla_conjunto,tabla_conjunto)+condiciones+')'
    #query = 'SELECT titulo FROM paper WHERE ( campo LIKE %%s% OR campo LIKE %%s% OR campo LIKE %%s%) AND' \
    #        '( campo LIKE %%s% OR campo LIKE %%s% OR campo LIKE %%s%) AND (campo LIKE %%s%' \
    #        ''
    # print query

def obtener_papers(id_proyecto):
    query = "SELECT eid, nombre_autor FROM paper AS p, paper_autor, autor AS a, paper_proyecto AS pp WHERE a.id = autor_id AND paper_id = p.id AND pp.id_paper = paper_id AND pp.id_proyecto = '{}'".format(id_proyecto)
    return run_query(query)

def obtener_autores(id_proyecto):
    '''Obtiene un diccionario que tiene como llave los autores y almacena la lista de los eid en los que ha participado
    :param id_proyecto:
    :return:
    '''
    autores = {}
    papers_proyecto = obtener_papers(id_proyecto);
    for paper in papers_proyecto:
        autor = paper[1]
        id = paper[0]
        if(autores.get(autor) == None):
            autores[autor] = []
        if(not (id in autores[autor]) ):
            autores[autor].append(id)
    #print json.dumps(autores)
    return json.dumps(autores)
#print select()[1]
#existe('paper','id', '1' )

def main():
    run_query(u'SELECT * FROM paper WHERE nombre="ò"')
    #buscar([['ing','sist','comp'],['eng', 'sys', 'comp']], 'afiliacion', 'nombre')#,[],[],[]])
    #obtener_papers(68)
    len(obtener_autores(68))
#main()

