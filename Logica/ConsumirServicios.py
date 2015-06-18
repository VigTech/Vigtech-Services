# coding=utf-8
__author__ = 'andres'
import json
from urllib2 import urlopen, quote, Request
import urllib
import procesamientoScopusXml


def consumir_scholar(consulta, user, proyecto):
    consulta = quote(consulta.encode("utf8"))
    user = quote(user.encode("utf8"))
    proyecto = quote(proyecto.encode("utf8"))

    server = "http://localhost:50000/consultaScholar/?consulta=" + consulta + "&user=" \
             + str(user) + "&proyecto=" + str(proyecto)



    # req = Request(server)
    response = urlopen(server)
    data = json.load(response)
    print response.read()

def consumir_arxiv(consulta, user, proyecto, limite):
    consulta = quote(consulta.encode("utf8"))
    user = quote(user.encode("utf8"))
    proyecto = quote(proyecto.encode("utf8"))
    
    server = "http://localhost:50000/consultaArxiv/?consulta=" + consulta + "&user=" \
             + str(user) + "&proyecto=" + str(proyecto) + "&limite=" +str(limite)



    # req = Request(server)
    response = urlopen(server)
    #data = json.load(response)
    print response.read()

# consumirScholar("Software")
# Realizar consulta a servicio web de Scopus para descargar documentos
def consumir_scopus(consulta, user, proyecto, limite):
    consulta = quote(consulta.encode("utf8"))
    user = quote(user.encode("utf8"))
    proyecto = quote(proyecto.encode("utf8"))
    server = "http://localhost:50001/consultaScopus/?consulta=" + consulta + "&user=" \
             + str(user) + "&proyecto=" + str(proyecto) + "&limite="+str(limite) 

    response = urlopen(server)
    data = json.load(response)
    print response.read()

   
    
class IR:
    # Acceso a Servicio Web de IR, realizar búsqueda sobre documentos indexados <GET>

    def consultar(self, consulta, user, proyecto):
        consulta =  quote(consulta.encode("utf8"))
        user = quote(user.encode("utf8"))
        proyecto = quote(proyecto.encode("utf8"))

        server = "http://localhost:8085/vigtech-ir/indexes/"+str(user) + "." + str(proyecto)\
                 + "/search?query=" \
                 + consulta

        response = urlopen(server)
        data = json.load(response)
        print response.read()
        return data
    # Indexación de documentos <POST>
    def indexar(self, user, proyecto):
        try:
            proyectopath= quote(str(user) + "." + str(proyecto))
            server = "http://localhost:8085/vigtech-ir/indexes/" + proyectopath
            #print server
            values=urllib.urlencode({})
            req = Request(server,values)
            response = urlopen(req)
            print "Indexar"
        except:
            print "Imposible realizar la indexacion" 

def consumir_red(user, proyecto):
    user = quote(user.encode("utf8"))
    proyecto = quote(proyecto.encode("utf8"))   
    server ="http://localhost:50002/red/?proyecto=" + str(proyecto)  + "&user=" + str(user)
    response = urlopen(server)
    data = json.load(response)
    return data
#ir = IR()
#ir.indexar("prueba", "1");
#Hagamos un prueba en este archivo

#consumir_arxiv("Software", "camicasi" ,"1" , 2)
