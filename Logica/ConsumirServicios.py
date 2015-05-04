__author__ = 'andres'
import json
from urllib2 import urlopen, quote, Request
def  consumir_scholar(consulta):
    consulta = quote(consulta.encode("utf8"))
    server = "http://192.168.28.103:50000/consultaScholar/v1.0/"+consulta

    #req = Request(server)
    response = urlopen(server)
    data = json.load(response)
    print response.read()

#consumirScholar("Software")

def consumir_scopus(consulta):

    consulta = quote(consulta.encode("utf8"))
    server = "http://192.168.28.103:50001/consultaScopus/v1.0/"+consulta

    response = urlopen(server)
    data = json.load(response)
    print response.read()