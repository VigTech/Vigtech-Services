import psycopg2
from psycopg2 import extras
# Create your views here.
import sys

reload(sys)  # to re-enable sys.setdefaultencoding()

sys.setdefaultencoding('utf-8')

class AdminBD:
    #conn_string = ""

    def __init__(self):


        try:


            self.conn = psycopg2.connect(database="docker", user="docker", password="docker", host="localhost", port="5432")
            # get a connection, if a connect cannot be made an exception will be raised here
            # conn.cursor will return a cursor object, you can use this cursor to perform queries
            self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            self.cursor.execute("SET CLIENT_ENCODING TO 'LATIN-1';")
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
            print filas
            return filas
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

#admin = AdminBD()
#admin.get_papers_proyecto(1)
#admin.get_autores(1)
data = {"Hola": "hola", "mundo": [1,2,3] }
import json
with open('data.txt', 'w') as outfile:
    json.dump(data, outfile)
