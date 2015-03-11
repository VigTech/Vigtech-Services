# -*- coding: utf-8 -*-
import igraph
from manejadorArchivos import leer_archivo, obtener_autores

class Red:
    '''La clase representa una red que se construye a partir de listas.
    '''
    def __init__(self, conjuntos, nombre, etiquetas_nodos = None):
        self.grafo = self.construir_red_autocorrelacion(conjuntos, nombre, self.contar_coincidencias, etiquetas_nodos)

    def construir_red_autocorrelacion(self, conjuntos, nombre, contar_coinc, etiquetas_nodos):
        '''Construye la red de autocorrelación de un conjunto de conjuntos

        Parámetros
        Conjuntos es una lista de listas'''
        print(len(conjuntos))
        cantidad_nodos = len(conjuntos)
        red = open(nombre+".net", 'w')
        red.write("*Vertices "+str(cantidad_nodos)+"\n")

        if etiquetas_nodos!=None:
            for i,etiqueta in enumerate(etiquetas_nodos):
                red.write(str(i+1)+' "'+etiqueta+'"\n')

        red.write("*Edges\n")
        for i in range(cantidad_nodos-1):
            for j in range(i+1, cantidad_nodos):
                #print(i,j)
                coinc = contar_coinc(conjuntos[i],conjuntos[j])
                if(coinc > 0):
                    print(i,j,"  ",coinc)
                    red.write(str(i+1)+" "+str(j+1)+" "+str(coinc)+"\n")
        red.close()
        return igraph.read(nombre+".net",format="pajek")
    def contar_coincidencias(self, conjunto_1, conjunto_2):
        coincidencias = 0
        for elemento_en_1 in conjunto_1:
            if elemento_en_1 in conjunto_2:
                    coincidencias+=1
        return coincidencias
    def average_degree(self):
	    return sum(self.grafo.degree())/float(len(self.grafo.degree()))

    def average_strength(self):
        return sum(self.grafo.strength(weights=self.grafo.es['weight']))/float(len(self.grafo.strength(weights=self.grafo.es['weight'])))

    def clustering_coefficient(self):
        return self.grafo.transitivity_undirected()

    def average_path_lenght(self):
        return self.grafo.average_path_length()

def main():
    # nodos = 15
    # conjuntos = []
    # for i in range(15):
    #     conjuntos.append(leer_archivo(open('redes/s/s'+str(i+1)+'.csv', 'r')))
    # print conjuntos
    # r = Red(conjuntos, 's')

    diccionario_autores = obtener_autores([open('XMLs/xml0.xml'),open('XMLs/xml1.xml'),open('XMLs/xml2.xml'),open('XMLs/xml3.xml')])
    lista_autores = []
    lista_nombres = []
    for autor in diccionario_autores:
        lista_autores.append(diccionario_autores[autor])
        lista_nombres.append(autor)
    r=Red(lista_autores, 'autores3', lista_nombres)
    #r.grafo.write_svg('autores4.svg')
    layout = r.grafo.layout("circle")
    igraph.plot(r.grafo,'autoresCircle.pdf', layout=layout, )

    visual_style = {}
    visual_style["vertex_size"] = 1
    #visual_style["vertex_color"] = [color_dict[gender] for gender in g.vs["gender"]]
    #visual_style["vertex_label"] = g.vs["name"]
    #visual_style["edge_width"] = [1 + 2 * int(is_formal) for is_formal in g.es["is_formal"]]
    visual_style["layout"] = layout
    visual_style["bbox"] = (300, 300)
    visual_style["margin"] = 20
    igraph.plot(r.grafo,'autoresNUEV.pdf', **visual_style)

#main()
