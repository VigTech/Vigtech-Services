# coding=utf-8
__author__ = 'andres'
import json
from urllib2 import urlopen, quote, Request
import urllib
import procesamientoScopusXml
from ConexionBD import adminBD


REPOSITORY_DIR = "/home/vigtech/shared/repository/"
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

def consumir_analisis(user, proyecto):
    
    user = quote(user.encode("utf8"))
    proyecto = quote(proyecto.encode("utf8"))

    server = "http://127.0.0.1:50003/analysis/?name=" + str(user) + "." + str(proyecto)
              

    response = urlopen(server)
    data = json.load(response)

    #analisis = open(REPOSITORY_DIR + "datos.json","w" )
    #analisis.write(data)
    with open(REPOSITORY_DIR +  str(user)  + "." + str(proyecto) +"/datos.json","w" ) as outfile:
        json.dump(data, outfile)
    #print response.read()
    #return data
def consumir_recuperacion_unidades_academicas(proyecto):
    UNIVERSIDAD_sin_cerrar_parantesis = ' ( AFFIL ( universidad  AND  del  AND  valle )  OR  AF-ID ( 60066812 ) ) '
    UNIVERSIDAD = ' ( AFFIL ( universidad  AND  del  AND  valle )  OR  AF-ID (  60066812 ) ) )'
    aranda = '(AUTHOR-NAME(AUTHLASTNAME(aranda) AUTHFIRST(j)) AND '+UNIVERSIDAD
    diaz = '((AUTHOR-NAME(AUTHLASTNAME(diaz) AUTHFIRST(f)) AND NOT (AUTHLASTNAME(diaz) AUTHFIRST(fernando)) ) AND '+UNIVERSIDAD
    banon = '(AUTHOR-NAME(AUTHLASTNAME(banon) AUTHFIRST(j)) AND '+UNIVERSIDAD
    bedoya = '(AUTHOR-NAME(AUTHLASTNAME(bedoya) AUTHFIRST(o)) AND '+UNIVERSIDAD
    gaona = '(AUTHOR-NAME(AUTHLASTNAME(gaona) AUTHFIRST(m)) AND '+UNIVERSIDAD
    florian = '(AUTHOR-NAME(AUTHLASTNAME(florian) AUTHFIRST(b)) AND '+UNIVERSIDAD
    solarte = '(AUTHOR-NAME(AUTHLASTNAME(solarte) AUTHFIRST(o)) AND '+UNIVERSIDAD
    gutierrez = '((AUTHOR-NAME(AUTHLASTNAME(gutierrez) AUTHFIRST(r.e)) OR AUTHOR-NAME(AUTHLASTNAME(pinerez) AUTHFIRST(r))) AND '+UNIVERSIDAD
    millan = '(((AUTHOR-NAME(AUTHLASTNAME(millan) AUTHFIRST(m)) AND NOT (AUTHLASTNAME(millan) AUTHFIRST(mauricio)) ) OR AUTHOR-NAME(AUTHLASTNAME(millan) AUTHFIRST(s))) AND '+UNIVERSIDAD
    moreno = '(AUTHOR-NAME(AUTHLASTNAME(moreno) AUTHFIRST(p)) AND '+UNIVERSIDAD
    tischer = '(AUTHOR-NAME(AUTHLASTNAME(tischer) AUTHFIRST(i)) AND '+UNIVERSIDAD
    trujillo = '(AUTHOR-NAME(AUTHLASTNAME(trujillo) AUTHFIRST(m)) AND '+UNIVERSIDAD
    banos = '(AUTHOR-NAME(AUTHLASTNAME(banos) AUTHFIRST(a)) AND '+UNIVERSIDAD
    carrillo = '(AUTHOR-NAME(AUTHLASTNAME(carrillo) AUTHFIRST(p)) AND '+UNIVERSIDAD
    villegas = '(AUTHOR-NAME(AUTHLASTNAME(villegas) AUTHFIRST(m)) AND '+UNIVERSIDAD
    a = ' OR '
    profesores = '('+aranda+a+diaz+a+banon+a+bedoya+a+gaona+a+florian+a+solarte+a+gutierrez+a+millan+a+moreno+a+tischer+a+trujillo+a+banos+a+carrillo+a+villegas+')'
    #resto_busqueda = '( ISSN ( 0121-5299 )  OR  ISSN ( 0123-3033 )  OR  ISSN ( 1571-0661 )  OR  ISSN ( 0302-9743 )  OR  ISSN ( 2010-3700 )  OR  ISSN ( 1900-8260 )  OR  ISSN ( 0716-8756 )  OR  ISSN ( 0120678 )  OR  ISSN ( 1657-7663 )  OR  ISSN ( 0718-0764 )  OR  ISSN ( 1794-1237 )  OR  ISSN ( 0010-4825 )  OR  ISSN ( 1657-4583 )  OR  ISSN ( 0717-5000 )  OR  ISSN ( 1383-7133 )  OR  ISSN ( 1657-2831 )  OR  ISSN ( 1571-5736 )  OR  ISSN ( 0124-2253 )  OR  ISSN ( 12345 )  OR  ISSN ( 0122-8242 )  OR  ISSN ( 0121-0777 )  OR  ISSN ( 0120-5609 )  OR  ISSN ( 1939-1382 )  OR  ISSN ( 1138-7386 )  OR  ISSN ( 0122-820x )  OR  ISSN ( 0232-0274 )  OR  ISSN ( 0036-1399 )  OR  ISSN ( 1657-5636 )  OR  ISSN ( 0884-8173 )  OR  ISSN ( 0120-548x )  OR  ISSN ( 0121-0262 )  OR  ISSN ( 0031-0603 )  OR  ISSN ( 1676-5680 )  OR  ISSN ( 0234-6206 )  OR  ISSN ( 0218-0014 )  OR  ISSN ( 1909-0056 )  OR  ISSN ( 0012-7353 )  OR  ISSN ( 1553-7358 ) )  OR  ( AFFIL ( ing*  AND  sist*  AND  comp* )  OR  AFFIL ( eng*  AND  sys*  AND  comp* )  OR  AFFIL ( dep*  AND  comput* )  OR  AFFIL ( eisc ) )'
    revistas = '( ISSN ( 0121-5299 )  OR  ISSN ( 0123-3033 )  OR  ISSN ( 1571-0661 )  OR  ISSN ( 0302-9743 )  OR  ISSN ( 2010-3700 )  OR  ISSN ( 1900-8260 )  OR  ISSN ( 0716-8756 )  OR  ISSN ( 0120678 )  OR  ISSN ( 1657-7663 )  OR  ISSN ( 0718-0764 )  OR  ISSN ( 1794-1237 )  OR  ISSN ( 0010-4825 )  OR  ISSN ( 1657-4583 )  OR  ISSN ( 0717-5000 )  OR  ISSN ( 1383-7133 )  OR  ISSN ( 1657-2831 )  OR  ISSN ( 1571-5736 )  OR  ISSN ( 0124-2253 )  OR  ISSN ( 12345 )  OR  ISSN ( 0122-8242 )  OR  ISSN ( 0121-0777 )  OR  ISSN ( 0120-5609 )  OR  ISSN ( 1939-1382 )  OR  ISSN ( 1138-7386 )  OR  ISSN ( 0122-820x )  OR  ISSN ( 0232-0274 )  OR  ISSN ( 0036-1399 )  OR  ISSN ( 1657-5636 )  OR  ISSN ( 0884-8173 )  OR  ISSN ( 0120-548x )  OR  ISSN ( 0121-0262 )  OR  ISSN ( 0031-0603 )  OR  ISSN ( 1676-5680 )  OR  ISSN ( 0234-6206 )  OR  ISSN ( 0218-0014 )  OR  ISSN ( 1909-0056 )  OR  ISSN ( 0012-7353 )  OR  ISSN ( 1553-7358 ) ) AND'+UNIVERSIDAD_sin_cerrar_parantesis
    direccion = '( AFFIL ( ing*  AND  sist*  AND  comp* )  OR  AFFIL ( eng*  AND  sys*  AND  comp* )  OR  AFFIL ( dep*  AND  comput* )  OR  AFFIL ( eisc ) ) AND'+UNIVERSIDAD_sin_cerrar_parantesis
    conceptos = '(TITLE-ABS-KEY(Constraint theory) OR TITLE-ABS-KEY(Problem solving) OR TITLE-ABS-KEY(Constraint programming) OR TITLE-ABS-KEY(Computer programming languages) OR TITLE-ABS-KEY(Logic programming) OR TITLE-ABS-KEY(Random access storage) OR TITLE-ABS-KEY(Computational geometry) OR TITLE-ABS-KEY(Collision detection) OR TITLE-ABS-KEY(Automatic translation) OR TITLE-ABS-KEY(Classification) OR TITLE-ABS-KEY(Software design) OR TITLE-ABS-KEY(User interfaces) OR TITLE-ABS-KEY(E-learning) OR TITLE-ABS-KEY(Virtual learning environment) OR TITLE-ABS-KEY(Adaptive evaluation) OR TITLE-ABS-KEY(Engineering education) OR TITLE-ABS-KEY(Learning system) OR TITLE-ABS-KEY(Recommender system) OR TITLE-ABS-KEY(Information retrieval) OR TITLE-ABS-KEY(Controlled natural language) OR TITLE-ABS-KEY(statistical parsing) OR TITLE-ABS-KEY(Data mining) OR TITLE-ABS-KEY(Database system) OR TITLE-ABS-KEY(Graph data model) OR TITLE-ABS-KEY(Decision support systems) OR TITLE-ABS-KEY(Graph theory) OR TITLE-ABS-KEY(Knowledge discovery in databases) OR TITLE-ABS-KEY(Recommender systems) OR TITLE-ABS-KEY(Electronic commerce) OR TITLE-ABS-KEY(DNA sequence) OR TITLE-ABS-KEY(Gene cluster) OR TITLE-ABS-KEY(Gene function) OR TITLE-ABS-KEY(Nucleotide sequence) OR TITLE-ABS-KEY(Chromosome map) OR TITLE-ABS-KEY(Computational Biology) OR TITLE-ABS-KEY(Bioinformatics) OR TITLE-ABS-KEY(Cellular automata) OR TITLE-ABS-KEY(Protein folding) OR TITLE-ABS-KEY(Computer vision) OR TITLE-ABS-KEY(Quantitative evaluation) OR TITLE-ABS-KEY(Stereo correspondence) OR TITLE-ABS-KEY(Stereo vision) OR TITLE-ABS-KEY(3D reconstruction) OR TITLE-ABS-KEY(Image coding) OR TITLE-ABS-KEY(Image segmentation) OR TITLE-ABS-KEY(Motion estimation) OR TITLE-ABS-KEY(Stereo correspondence) OR TITLE-ABS-KEY(Histology images) OR TITLE-ABS-KEY(Image analysis))'
    social_semantic = '%s AND %s'%(profesores,conceptos)
    direccion_cod = codificar_a_url(revistas)
    json_eids_revistas = urlopen('http://127.0.0.1:5001/obtenerEid/?consulta=%s'%(direccion_cod))
    eids_revistas = json.load(json_eids_revistas)['eids']
    eids_revistas = map(str, eids_revistas)
    print profesores

    eids_direccion = obtener_conjunto(direccion)
    eids_profesores = obtener_conjunto(profesores)
    eids_social_semantic = obtener_conjunto(social_semantic)

    papers_clasificar = adminBD.get_eid_papers_proyecto(proyecto)

    diccionario_peticion = {"j":eids_revistas, "s":eids_profesores, "clasificar":eids_revistas, "a": eids_direccion, "o":eids_social_semantic}
    print str(diccionario_peticion)
    consultica = str(diccionario_peticion).replace('\'','"')
    consulta = 'http://127.0.0.1:5000/clasificacionUnidadAcademica/?datosJson=%s'%(consultica)
    print consulta
    json_clasificados = urlopen('http://127.0.0.1:5000/clasificacionUnidadAcademica/?datosJson=%s'%(codificar_a_url(consultica)))
    print json_clasificados.read()

def codificar_a_url(consulta):
    consulta_formateada = quote(consulta.encode("utf8"))
    return consulta_formateada

def obtener_conjunto(consulta):
    consulta_cod = codificar_a_url(consulta)
    json_eids_conjunto = urlopen('http://127.0.0.1:5001/obtenerEid/?consulta=%s'%(consulta_cod))
    eids = json.load(json_eids_conjunto)['eids']
    eids = map(str, eids)
    return eids

    
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
        for d in data:
            d['path'] = quote(d['path'].replace("/home/vigtech/shared/repository/", "/media/").encode("utf8"))
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
    with open(REPOSITORY_DIR +  str(user)  + "." + str(proyecto) +"/coautoria.json","w" ) as outfile:
        json.dump(data, outfile)
    print response.read()
    return data
#ir = IR()
#ir.indexar("prueba", "1");
#Hagamos un prueba en este archivo

#consumir_arxiv("Software", "camicasi" ,"1" , 2)
