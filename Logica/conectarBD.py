import psycopg2
# -*- coding: utf-8 -*-


def run_query(query=''):
    #conn_string = "host='localhost' dbname='postgres' user='postgres' password='chucho'"
    conn_string = "host='127.0.0.1' dbname='docker' user='docker' password='docker' port='49153'"
    conn = psycopg2.connect(conn_string) # Conectar a la base de datos
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
    id_revista = insert_returning_id(revista, 'revista', 'issn', 'issn', 'issn', ['issn', 'titulo_revista'],
                                     ['issn', 'publicationName'])
    print 'hola'
    id_paper = insert_returning_id(paper, 'paper', 'eid', 'eid', 'id', ['eid', 'titulo_paper', 'abstract','total_citaciones',
                                                                        'fecha','doi', 'link_source'],
                                   ['eid', 'title', 'description','citedby-count','coverDate','doi','linkScopus'])


    for afiliacion in afiliaciones:
        id_afiliacion = insert_returning_id(afiliacion, 'afiliacion', 'afid', 'scopus_id', 'id',
                                            ['scopus_id', 'nombre', 'pais','ciudad','variante_nombre'],
                                            ['afid', 'affilname', 'affiliation-country','affiliation-city','name-variant'])
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
    print id_paper

def insert_returning_id(dicci_tabla, nombre_tabla, identificador_xml, identificador_bd, id_retorno, campos_bd, campos_xml):
    lista_id_paper = select_id(id_retorno, nombre_tabla, identificador_bd, dicci_tabla[identificador_xml])
    if lista_id_paper:
        print 'denegado insert returning'
        id = lista_id_paper[0][0]
    else:
        string_campos = '%s,'*len(campos_bd)%tuple((campo for campo in campos_bd))
        #eliminar ultimo caracter por la coma
        string_campos = string_campos[:-1]
        string_valores = "'%s',"*len(campos_bd)%tuple((dicci_tabla[campo] for campo in campos_xml))
        #eliminar ultimo caracter por la coma
        string_valores = string_valores[:-1]
        paper_query = "INSERT INTO %s (%s) VALUES (%s) RETURNING %s;"%(nombre_tabla,string_campos, string_valores, id_retorno)
        print paper_query
        id = run_query(paper_query)[0][0]
        print id
    return id

def insert_relation(tabla, atrib_id1, atrib_id2, valor1, valor2):
    if not select_id2(tabla, atrib_id1, atrib_id2, valor1, valor2):
        autor_paper_query = "INSERT INTO %s (%s, %s) VALUES (%s,%s)"%(tabla,atrib_id1,atrib_id2,valor1,valor2)
        run_query(autor_paper_query)

def select_id(id, tabla, atrib_id, valor):
    query = "SELECT %s FROM %s WHERE %s = '%s'"%(id,tabla, atrib_id, valor)
    result = run_query(query)
    return result

def select_id2(tabla, atrib_id1, atrib_id2, valor1, valor2):
    query = "SELECT * FROM %s WHERE %s = %s AND %s = %s"%(tabla, atrib_id1, valor1, atrib_id2, valor2)
    result = run_query(query)
    return result


#print select()[1]
#existe('paper','id', '1' )
def main():
    run_query('SELECT * FROM paper')

#main()
