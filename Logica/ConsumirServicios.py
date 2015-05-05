__author__ = 'andres'
import json
from urllib2 import urlopen, quote, Request


def consumir_scholar(consulta, user, proyecto):
    consulta = quote(consulta.encode("utf8"))
    user = quote(user.encode("utf8"))
    proyecto = quote(proyecto.encode("utf8"))

    server = "http://192.168.28.103:50000/consultaScholar/?consulta=" + consulta + "&user=" \
             + str(user) + "&proyecto=" + str(proyecto)



    # req = Request(server)
    response = urlopen(server)
    data = json.load(response)
    print response.read()


# consumirScholar("Software")

def consumir_scopus(consulta, user, proyecto):
    consulta = quote(consulta.encode("utf8"))
    user = quote(user.encode("utf8"))
    proyecto = quote(proyecto.encode("utf8"))
    server = "http://192.168.28.103:50001/consultaScopus/?consulta=" + consulta + "&user=" \
             + str(user) + "&proyecto=" + str(proyecto)

    response = urlopen(server)
    data = json.load(response)
    print response.read()