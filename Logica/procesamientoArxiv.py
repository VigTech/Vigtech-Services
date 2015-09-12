import xml.etree.ElementTree as ET
#from conectarBD import insertar_paper
from ConexionBD import adminBD
from adminBD import AdminBD
#paper, autores, revista,afiliaciones, keywords, id_proyecto
REPOSITORY_DIR= "/home/vigtech/shared/repository/"

def get_metadatos(xml):
	tree = ET.parse(xml)
	root = tree.getroot()
	papers = []
		#print root.tag
	
	papers=[]
	for node in tree.findall('{http://www.w3.org/2005/Atom}entry'):
		node.tag
		autores=[]
		link=node.find('{http://www.w3.org/2005/Atom}link')
		if link.get("title") == 'doi':
			doi= extraer_doi(link.get('href'))
				#print doi
		else:
			doi = '00000'
		if link.get('title') == 'pdf':
			linktext=link.get('href')
		else:
			linktext=""
				#print doi
		partsid=node.find("{http://www.w3.org/2005/Atom}id").text.split("/")
		id = partsid[len(partsid)-1]
			#print id
		titulo=node.find("{http://www.w3.org/2005/Atom}title").text
		titulo = titulo.replace("'","''")
		fecha =node.find("{http://www.w3.org/2005/Atom}published").text[0:10]
			#print fecha
			#doi=node.find("{http://www.w3.org/2005/Atom}arxiv:doi").text
		abstract=node.find("{http://www.w3.org/2005/Atom}summary").text
		abstract = abstract.replace("'","''")
		for autor in node.findall('{http://www.w3.org/2005/Atom}author'):
			for name in autor.iter('{http://www.w3.org/2005/Atom}name'):
				autores.append(name.text)
		paper={"doi":str(doi),"fecha":str(fecha),"id":str(id),"titulo":str(titulo), "abstract":str(abstract), 'autores': autores, "link":linktext}
			#print autores
		papers.append(paper)
		#print papers
	return papers
		
def insertar_metadatos_bd(xml,proyecto):
	#xml = open("salida1.xml", "r")
	papers=get_metadatos(xml)
	admin = AdminBD()	
	admin.insertar_papers(proyecto, papers)
	
def extraer_doi(link):
	#prueba = "http://dx.doi.org/10.5121/ijsea.2010.1303"
	values = link.split(".org")
	#print values
	doi = values[1][1:]
	return doi 
#arxiv = Arxiv("camicasi", "1")

#xml = open("/home/vigtech/shared/repository/admin.33/salida.xml", "r")
#get_metadatos(xml)
#insertar_metadatos_bd(xml,33)
	
	
