
import urllib
testFile=urllib.URLopener()
url= "http://trec.nist.gov/pubs/trec11/papers/lcc.moldovan.pdf"
urllib.urlretrieve(url, "/home/administrador/ManejoVigtech/ArchivosProyectos/admin.42/prueba.pdf")
#testFile.retrieve(url,"/home/administador/ManejoVigtech/ArchivosProyectos/prueba.pdf")

'''
import os
#os.system("mv -f test /home/administrador/ManejoVigtech/ArchivosProyectos/ ")
import tempfile
import shutil

path=tempfile.mkdtemp()
print shutil.rmtree(path)
'''
