import psycopg2
from psycopg2 import extras
# Create your views here.
import sys

reload(sys)  # to re-enable sys.setdefaultencoding()

sys.setdefaultencoding('utf-8')

class AdminBD:
    #conn_string = ""

    def __init__(self):

		#host='127.0.0.1' dbname='docker' user='docker' password='docker' port='49153'"
        try:


            self.conn = psycopg2.connect(database="docker", user="docker", password="docker", host="localhost", port="49153")
            # get a connection, if a connect cannot be made an exception will be raised here
            # conn.cursor will return a cursor object, you can use this cursor to perform queries
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            #self.conn.set_character_encoding('utf8')
            self.conn.set_client_encoding('UTF-8')
            #self.cursor.execute("SET CLIENT_ENCODING TO 'LATIN-1';")
            #cursor_factory=psycopg2.extras.DictCursor
            print "Connected!\n"
        except:
            print "Not Connected!\n"

    def get_eid_papers_proyecto(self, proyecto):
        consulta = "SELECT eid from paper_proyecto JOIN paper ON id_paper=id WHERE id_proyecto = %s;" %(str(proyecto))
        try:
            print consulta
            self.cursor.execute(consulta)
            filas = self.cursor.fetchall()
            eids=[]
            for row in filas:
				eids.append( row['eid'])
            #print filas
            return eids
        except psycopg2.DatabaseError, e:
            print 'Error %s' %e
            print "Imposible realizar la cosulta"
    def get_autores(self, proyecto):
		consulta= "Select au.nombre_autor from paper_proyecto pp JOIN paper_autor pa ON pa.paper_id = pp.id_paper JOIN autor au ON au.id = autor_id WHERE pp.id_proyecto = %s;" %(str(proyecto))
		try:
			print consulta
			self.cursor.execute(consulta)
			filas = self.cursor.fetchall()
			print filas
			return filas
		except psycopg2.DatabaseError, e:
			print 'Error %s' %e
			print "Imposible realizar la cosulta"
    #Select au.nombre_autor from paper_proyecto pp JOIN paper_autor pa ON pa.paper_id = pp.id_paper JOIN autor au ON au.id = autor_id WHERE pp.id_proyecto = 1; 
    def get_dois_proyecto(self, proyecto):
		consulta= "SELECT doi from paper_proyecto pp JOIN paper p ON pp.id_paper=p.id WHERE pp.id_proyecto =%s AND p.descargo=false AND NOT doi='00000';" %str(proyecto)
		try:
			print consulta
			self.cursor.execute(consulta)
			filas = self.cursor.fetchall()
			doi=[]
			for row in filas:
				doi.append( row['doi'])
			#print filas
			#print doi
			return doi
		except psycopg2.DatabaseError, e:
			print 'Error %s' %e
			print "Imposible realizar la cosulta"
        
    def insertar_papers(self, proyecto,papers):
        print "hola mundo"
        for paper in papers:
            consulta = "INSERT INTO paper (doi,fecha,titulo_paper, total_citaciones,eid,abstract,descargo) VALUES (\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\') RETURNING id"%(paper['doi'], paper['fecha'], paper['titulo'],str(0), '00000', paper['abstract'], 'FALSE')
            try:
                print consulta
                self.cursor.execute(consulta)
                self.conn.commit()
                data = self.cursor.fetchall()
                id_paper=data[0][0]
                self.insertar_autores(paper['autores'], id_paper)
                self.insertar_paper_proyecto(proyecto,id_paper)
            except psycopg2.DatabaseError, e:
                if self.conn:
                    self.conn.rollback()
                print 'Error %s' %e
                print "Imposible realizar la cosulta"
                sys.exit(1)

    def insertar_autor(self,autor):
        autor = autor.replace("'","''")
        consulta = "INSERT INTO autor (nombre_autor) VALUES('%s') RETURNING id;"%(autor)
        try:
            print consulta
            
            self.cursor.execute(consulta)
            self.conn.commit()
            data = self.cursor.fetchall()
            return data[0][0]
        except psycopg2.DatabaseError, e:
            if self.conn:
                self.conn.rollback()
            print 'Error %s' %e
            print "Imposible realizar la cosulta"
            sys.exit(1)
    def insertar_paper_autor(self,id_autor,id_paper):
        consulta = "INSERT INTO paper_autor (paper_id,autor_id) VALUES(\'%s\',\'%s\');"%(str(id_paper), str(id_autor))
        try:
            print consulta
            self.cursor.execute(consulta)
            self.conn.commit()
        except psycopg2.DatabaseError, e:
            if self.conn:
                self.conn.rollback()
            print 'Error %s' %e
            print "Imposible realizar la cosulta"
            sys.exit(1)
    def insertar_autores(self,autores,id_paper):
        for autor in autores:
            id_autor=self.insertar_autor(autor)
            self.insertar_paper_autor(id_autor,id_paper)
    def insertar_paper_proyecto(self,id_proyecto,id_paper):
        consulta = "INSERT INTO paper_proyecto (id_proyecto,id_paper) VALUES(\'%s\',\'%s\');"%(str(id_proyecto), str(id_paper))
        try:
            print consulta
            self.cursor.execute(consulta)
            self.conn.commit()
        except psycopg2.DatabaseError, e:
            if self.conn:
                self.conn.rollback()
            print 'Error %s' %e
            print "Imposible realizar la cosulta"
            sys.exit(1)

    def get_papers_eid(self, eids):
        consulta = 'SELECT titulo_paper FROM paper WHERE '
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
            print consulta
            self.cursor.execute(consulta)
            filas = self.cursor.fetchall()
            #filas=[]
            papers=[]
            for row in filas:
                   #papers.append({"titulo": row['titulo_paper'], "link": row['link'])
                papers.append({"titulo": row['titulo_paper']})
                    #eids.append( row['eid'])
            #print filas
            return papers
        except psycopg2.DatabaseError, e:
            print traceback.format_exc()
            print 'Error %s' %e
            print "Imposible realizar la cosulta"
            sys.exit(1)

    def get_papers_proyecto(self, proyecto):
        consulta="SELECT id_paper, titulo_paper, fecha, total_citaciones, revista_issn, eid, abstract from paper_proyecto pp JOIN paper p ON p.id=pp.id_paper  WHERE pp.id_proyecto=%s" %(str(proyecto))
        try:
            print consulta
            self.cursor.execute(consulta)
            filas = self.cursor.fetchall()
            papers=[]
            for row in filas:
                   #papers.append({"titulo": row['titulo_paper'], "link": row['link'])
                papers.append({"titulo": row['titulo_paper']})
                    #eids.append( row['eid'])
            #print filas
            return eids
        except psycopg2.DatabaseError, e:
            if self.conn:
                self.conn.rollback()
            print 'Error %s' %e
            print "Imposible realizar la cosulta"
            sys.exit(1)
#admin = AdminBD()
#print admin.get_eid_papers_proyecto(11)
#print admin.get_dois_proyecto(22)
#admin.get_autores(1)
"""
data = {"Hola": "hola", "mundo": [1,2,3] }
import json
with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)
"""
