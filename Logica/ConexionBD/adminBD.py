import psycopg2
from psycopg2 import extras
from principal.parameters import *

# Create your views here.
import sys

reload(sys)  # to re-enable sys.setdefaultencoding()

sys.setdefaultencoding('utf-8')

class AdminBD:
    #conn_string = ""

    def __init__(self):

		#host='127.0.0.1' dbname='docker' user='docker' password='docker' port='49153'"
        try:


            #self.conn = psycopg2.connect(database="docker", user="docker", password="docker", host="localhost", port="49153")
            self.conn = psycopg2.connect(database=DATABASE, user=USER, password=PASSWORD, host=HOST, port=PORT)
            # get a connection, if a connect cannot be made an exception will be raised here
            # conn.cursor will return a cursor object, you can use this cursor to perform queries
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            #self.conn.set_character_encoding('utf8')
            self.conn.set_client_encoding('UTF-8')
            #self.cursor.execute("SET CLIENT_ENCODING TO 'LATIN-1';")
            #cursor_factory=psycopg2.extras.DictCursor
        except:
            raise Exception('No se pudo conectar a la DB!')

    def get_eid_papers_proyecto(self, proyecto):
        consulta = "SELECT eid from paper_proyecto JOIN paper ON id_paper=id WHERE id_proyecto = %s;" %(str(proyecto))
        try:
            self.cursor.execute(consulta)
            filas = self.cursor.fetchall()
            eids=[]
            for row in filas:
				eids.append( row['eid'])
            return eids
        except psycopg2.DatabaseError, e:
            raise Exception('No se pudo get_eid_papers_proyecto()')

    def get_autores(self, proyecto):
		consulta= "Select au.nombre_autor from paper_proyecto pp JOIN paper_autor pa ON pa.paper_id = pp.id_paper JOIN autor au ON au.id = autor_id WHERE pp.id_proyecto = %s;" %(str(proyecto))
		try:
			self.cursor.execute(consulta)
			filas = self.cursor.fetchall()
			return filas
		except psycopg2.DatabaseError, e:
			raise Exception('No se pudo get_autores()')
    #Select au.nombre_autor from paper_proyecto pp JOIN paper_autor pa ON pa.paper_id = pp.id_paper JOIN autor au ON au.id = autor_id WHERE pp.id_proyecto = 1; 
    def get_dois_proyecto(self, proyecto):
		consulta= "SELECT doi from paper_proyecto pp JOIN paper p ON pp.id_paper=p.id WHERE pp.id_proyecto =%s AND p.descargo=false AND NOT doi='00000';" %str(proyecto)
		try:
			self.cursor.execute(consulta)
			filas = self.cursor.fetchall()
			doi=[]
			for row in filas:
				doi.append( row['doi'])
			return doi
		except psycopg2.DatabaseError, e:
			raise Exception('No se pudo get_dois_proyecto()')
        
    def insertar_papers(self, proyecto,papers):
        for paper in papers:
            consulta = "INSERT INTO paper (doi,fecha,titulo_paper, total_citaciones,eid,abstract,descargo,link_source) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\') RETURNING id"%(paper['doi'], paper['fecha'], paper['titulo'],str(0), '00000', paper['abstract'], 'FALSE', paper['link'])
            try:
                self.cursor.execute(consulta)
                self.conn.commit()
                data = self.cursor.fetchall()
                id_paper=data[0][0]
                self.insertar_autores(paper['autores'], id_paper)
                self.insertar_paper_proyecto(proyecto,id_paper)
            except psycopg2.DatabaseError, e:
                if self.conn:
                    self.conn.rollback()
                raise Exception('No se pudo insertar_papers()')
                sys.exit(1)

    def insertar_autor(self,autor):
        autor = autor.replace("'","''")
        consulta = "INSERT INTO autor (nombre_autor) VALUES('%s') RETURNING id;"%(autor)
        try:
            self.cursor.execute(consulta)
            self.conn.commit()
            data = self.cursor.fetchall()
            return data[0][0]
        except psycopg2.DatabaseError, e:
            if self.conn:
                self.conn.rollback()
            raise Exception('No se pudo insertar_autor()')
            sys.exit(1)
    def insertar_paper_autor(self,id_autor,id_paper):
        consulta = "INSERT INTO paper_autor (paper_id,autor_id) VALUES(\'%s\',\'%s\');"%(str(id_paper), str(id_autor))
        try:
            self.cursor.execute(consulta)
            self.conn.commit()
        except psycopg2.DatabaseError, e:
            if self.conn:
                self.conn.rollback()
            raise Exception('No se pudo insertar_paper_autor()')
            sys.exit(1)
    def insertar_autores(self,autores,id_paper):
        for autor in autores:
            id_autor=self.insertar_autor(autor)
            self.insertar_paper_autor(id_autor,id_paper)
    def insertar_paper_proyecto(self,id_proyecto,id_paper):
        consulta = "INSERT INTO paper_proyecto (id_proyecto,id_paper) VALUES(\'%s\',\'%s\');"%(str(id_proyecto), str(id_paper))
        try:
            self.cursor.execute(consulta)
            self.conn.commit()
        except psycopg2.DatabaseError, e:
            if self.conn:
                self.conn.rollback()
            raise Exception('No se pudo insertar_paper_proyecto()')
            sys.exit(1)

    def get_papers_eid(self, eids):
        consulta = 'SELECT titulo_paper, link_source  FROM paper WHERE '
        count = 0
        for eid in eids:
            if count == 0:
                concat = ' eid = \'%s\'' %(str(eid))
                consulta += concat
            else:
                concat = ' OR eid = \'%s\'' %(str(eid))
                consulta += concat
            count +=1
        try:
            self.cursor.execute(consulta)
            filas = self.cursor.fetchall()
            #filas=[]
            papers=[]
            for row in filas:
                   #papers.append({"titulo": row['titulo_paper'], "link": row['link'])
                papers.append({"titulo": row['titulo_paper'], "link_source": row['link_source']})
                    #eids.append( row['eid'])
            return papers
        except psycopg2.DatabaseError, e:
            raise Exception('No se pudo get_papers_eid()')
            sys.exit(1)

    def get_papers_proyecto(self, proyecto):
        consulta="SELECT id_paper, titulo_paper, fecha, total_citaciones, revista_issn, eid, abstract from paper_proyecto pp JOIN paper p ON p.id=pp.id_paper  WHERE pp.id_proyecto=%s" %(str(proyecto))
        try:
            self.cursor.execute(consulta)
            filas = self.cursor.fetchall()
            papers=[]
            for row in filas:
                   #papers.append({"titulo": row['titulo_paper'], "link": row['link'])
                papers.append({"titulo": row['titulo_paper'], "link_source": row['link_source']})
                    #eids.append( row['eid'])
            return eids
        except psycopg2.DatabaseError, e:
            if self.conn:
                self.conn.rollback()
            raise Exception('No se pudo get_papers_proyecto()')
            sys.exit(1)

    def getAuthors(self, paper_id):
        #cur = self.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """
        SELECT
            id_scopus AS authid,
            nombre_autor AS authname,
            id_afiliacion_scopus AS afid
        FROM
            paper_autor pau, autor au
        WHERE
            pau.paper_id = {} AND pau.autor_id = au.id;
        """
        query = query.format(paper_id)
        self.cursor.execute(query)
        #cur.execute(query)
        data = self.cursor.fetchall()
        authors = []
        for data_tuple in data:
            authors.append(dict(data_tuple))
        return authors

    def getAffiliation(self, paper_id):
        #cur = self.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """
        SELECT
            scopus_id AS afid,
            nombre AS affilname,
            pais AS affiliation__country,
            ciudad AS affiliation__city,
            variante_nombre AS name__variant
        FROM
            paper_afiliacion pa, afiliacion a
        WHERE
            pa.paper_id = {} AND pa.afiliacion_id = a.id
        """
        query = query.format(paper_id)
        #cur.execute(query)
        self.cursor.execute(query)
        data =  self.cursor.fetchone()
        return dict(data) if data else {}

    def getKeywords(self, paper_id):
        #cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """
        SELECT
            pk.paper_id,
            string_agg(k.keyword, '|') as authkeywords
        FROM
            paper_keyword pk, keyword k
        WHERE
            pk.paper_id = {} AND pk.keyword_id = k.id
        GROUP BY pk.paper_id
        """
        query = query.format(paper_id)
        self.cursor.execute(query)
        #cur.execute(query)
        data = self.cursor.fetchone()
        return data['authkeywords'] if data else ''

    

    def getPapers(self, project_id):
        #cur = self.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = """
        SELECT
            id,
            p.link_source AS prism_url,
            eid, titulo_paper AS dc_title,
            doi AS prism_doi,
            abstract AS dc_description,
            fecha AS prism_coverDate,
            total_citaciones AS citedby__count
        FROM
            paper p, paper_proyecto pp
        WHERE
            pp.id_proyecto = {} AND pp.id_paper = p.id;
        """
        query = query.format(project_id)
        self.cursor.execute(query)
        data = self.cursor.fetchall()
        papers = []
        for data_tuple in data:
            paper_id = data_tuple[0]
            paper = dict(data_tuple)
            paper['authors'] = self.getAuthors(paper_id)
            paper['affiliation'] = self.getAffiliation(paper_id)
            paper['authkeywords'] = self.getKeywords(paper_id)
            papers.append(paper)
        return papers

"""
data = {"Hola": "hola", "mundo": [1,2,3] }
import json
with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)
"""
