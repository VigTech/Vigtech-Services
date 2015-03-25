from urllib2 import urlopen, quote
import xml.etree.ElementTree as ET
import traceback
#Esta clase sirve para conectarse con scopus y obtener datos de alli
class Descarga:
	#COnstructor con valores por defecto para una busqueda
	def __init__(self):
		self.url = "http://api.elsevier.com/content/search/scopus"
		self.consulta = self.codificar_a_url("heart")
		self.parametros = "&view=COMPLETE&httpAccept=application/xml&apiKey=b50e60b193e884e6d78948e916d816a0&count=100"
	def __init__(self, query, start = 0):
		self.url = "http://api.elsevier.com/content/search/index:scopus"
		self.consulta = self.codificar_a_url(query)
		self.raw_consulta = query
		self.parametros = "&view=COMPLETE&httpAccept=application/xml&apiKey=b50e60b193e884e6d78948e916d816a0&count=20&start="+str(start)
		self.construir_peticion()
	#Construye, a partir de los atributos de la clase, la url para hacer la peticion a scopus
	def buscar_por_doi(self):
		self.url = 'http://api.elsevier.com/content/article/'
		#self.peticion = self.url+'DOI:'+self.codificar_a_url('['+self.consulta+']')+ '?httpAccept=application/pdf'
		self.peticion = self.url+'DOI:['+self.consulta+']?httpAccept=application/pdf'
		self.peticionXML = self.url+'DOI:['+self.consulta+']?httpAccept=text/xml'

		
		
	def construir_peticion(self):
		self.peticion = self.url+"?query="+self.consulta+self.parametros
		return self.peticion
	#Codifica la consulta en bruto(string) a la forma que puede entender la url
	def codificar_a_url(self, consulta):
		consulta_formateada = quote(consulta.encode("utf8"))
		return consulta_formateada
	# Hace la peticion al url y devuelve la respuesta
	def obtener_respuesta(self, peticion):
		url = (peticion)
		print url
		# Archivo web
		
		respuesta = urlopen(url)
		
		
		return respuesta
		
	def descargar_xml(self, xml, filename):
		f = open(filename+'.xml', "w")
		respuesta = xml.read()
		f.write(respuesta)
		f.close
		
	# Escribe la respuesta del url en un archivo	
	def descargar(self):
		try:
			#r = self.obtener_respuesta(self.peticionXML)
			#titulo = self.obtener_metadatos(r, '{http://purl.org/dc/elements/1.1/}title')[0]
			r = self.obtener_respuesta(self.peticion)
			# Nombre del archivo a partir del URL
			#filename = self.raw_consulta.replace('/','s').replace('.','p')+".pdf"
			
			respuesta = r.read()
			
			# Verificar si es un xml		
			if (not '<full-text-retrieval' in respuesta):
				xml = self.obtener_respuesta(self.peticionXML)
				titulo = self.obtener_metadatos(xml, '{http://purl.org/dc/elements/1.1/}title')[0]
				# Archivo local
				filename = titulo+'.pdf'
				#f = open(filename, "w")
				#f=open("/home/administrador/ManejoVigtech/ArchivosProyectos/" + filename, "w")
				f=open(filename, "w") 
				# Escribir en un nuevo fichero local los datos obtenidos via HTTP.
				f.write(respuesta)
				# Cerrar ambos
				f.close()
				print "%s descargado correctamente." % filename
				print titulo
				return titulo
			
			r.close()
			
		except Exception:
			print 'no hay nada', traceback.format_exc()
		
	def obtener_metadatos(self, xml, campo):
		respuesta = []
		tree = ET.parse(xml)
		root = tree.getroot()
		for child in root:
			for campito in child.findall(campo):
				print campito.text
				respuesta.append(campito.text)
		return respuesta

'''	
def main():
	d = Descarga("Hola( a")
	print d.construir_peticion()

main()'''
#d = Descarga('AUTHOR-NAME ( aranda,  AND  j )')
#d.descargar_xml(d.obtener_respuesta(d.peticion))
