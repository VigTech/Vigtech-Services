import psycopg2
# -*- coding: utf-8 -*-


def run_query(query=''):
    #conn_string = "host='localhost' dbname='metaVigTech' user='postgres' password='chucho'"
    conn_string = "host='127.0.0.1:32768' dbname='docker' user='docker' password='docker'"
    conn = psycopg2.connect(conn_string) # Conectar a la base de datos
    cursor = conn.cursor()         # Crear un cursor
    cursor.execute(query)          # Ejecutar una consulta

    #Le inclui insert
    if query.upper().startswith('SELECT'):
        data = cursor.fetchall()   # Traer los resultados de un select
    elif query.upper().startswith('INSERT') and 'RETURNING ID' in query.upper():
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

def insertar_paper(paper, autores):#, revista, keywords, autores):
    '''Inserta en la BD la información de un paper que viene en forma de listas para cada tabla de la BD
    '''
    #funcion_sql_ultimo_id = "SELECT currval('paper_id_seq');"
    #paper_query = "INSERT INTO paper (doi,titulo_paper, abstract, issn, fecha, revista_issn, total_citaciones) VALUES ('%s','%s','%s',%s,%s,%s,%s);"%(paper['doi'],paper['title'],paper['abstract'])
    #paper_query = "INSERT INTO paper (doi,titulo_paper, abstract) VALUES ('%s','%s','%s') RETURNING id;"%(paper['doi'],paper['title'],paper['description'])
    id_paper = insert_returning_id(paper, 'paper', 'eid', ['eid', 'titulo_paper', 'abstract'], ['eid', 'title', 'description'])

    for autor in autores:
        lista_id_autor = select_id('autor', 'id_scopus', autor['authid'])
        if lista_id_autor:
            print 'denegado'
            id_autor = lista_id_autor[0][0]
        else:
            paper_query = "INSERT INTO autor (id_scopus,nombre_autor) VALUES ('%s','%s') RETURNING id;"%(autor['authid'],autor['authname'])
            id_autor = run_query(paper_query)[0][0]
        if not select_id2('paper_autor', 'paper_id', 'autor_id', id_paper, id_autor):
            autor_paper_query = "INSERT INTO paper_autor (paper_id, autor_id) VALUES ('%s','%s')"%(id_paper, id_autor)
            run_query(autor_paper_query)

    #print type(paper_query)
    print id_paper

def insert_returning_id(dicci_tabla, nombre_tabla, identificador, campos_bd, campos_xml):
    lista_id_paper = select_id(nombre_tabla, identificador, dicci_tabla[identificador])
    if lista_id_paper:
        print 'denegado'
        id = lista_id_paper[0][0]
    else:
        string_campos = '%s,'*len(campos_bd)%tuple((campo for campo in campos_bd))
        #eliminar último caracter por la coma
        string_campos = string_campos[:-1]
        string_valores = "'%s',"*len(campos_bd)%tuple((dicci_tabla[campo] for campo in campos_xml))
        #eliminar último caracter por la coma
        string_valores = string_valores[:-1]
        paper_query = "INSERT INTO paper (%s) VALUES (%s) RETURNING id;"%(string_campos, string_valores)
        print paper_query
        id = run_query(paper_query)[0][0]
    return id

def select_id(tabla, atrib_id, valor):
    query = "SELECT id FROM %s WHERE %s = '%s'"%(tabla, atrib_id, valor)
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