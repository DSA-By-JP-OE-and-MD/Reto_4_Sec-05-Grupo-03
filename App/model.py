"""
 * Copyright 2020, Departamento de sistemas y Computación
 * Universidad de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along with this program.  If not, see <http://www.gnu.org/licenses/>.
 * Contribución de:
 *
 * Dario Correal
 *
 """
import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.ADT import orderedmap as om
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Algorithms.Graphs import dfo
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
def analyzer():
    analyzer = {"nameIndex":None,
                "graph":None}
    analyzer["nameIndex"] = m.newMap(numelements=1000, 
                                     maptype="PROBING",
                                     loadfactor=0.5, 
                                     comparefunction=comparer)      

    analyzer["graph"] = gr.newGraph(datastructure='ADJ_LIST',
                                    directed=True,
                                    size=1000,
                                    comparefunction=comparer)
    return analyzer

# -----------------------------------------------------

# Funciones para agregar informacion al grafo
def AñadirRuta(analyzer, route):
    """
    """
    origin = route['start station id']
    destination = route['end station id']
    originName = route["start station name"]
    destinationName = route["end station name"]
    duration = int(route['tripduration'])
    AñadirEstacion(analyzer, origin)
    AñadirEstacion(analyzer, destination)
    AñadirConeccion(analyzer, origin, destination, duration)
    addMapName(analyzer, origin, originName)
    addMapName(analyzer, destination, destinationName)

def AñadirEstacion(analyzer, estacion):
    if not gr.containsVertex(analyzer["graph"], estacion):
        gr.insertVertex(analyzer["graph"], estacion)
    return analyzer

def addMapName(analyzer, estacion, nombre):
    if not m.contains(analyzer["nameIndex"], estacion):
        m.put(analyzer["nameIndex"], estacion, nombre)

def AñadirConeccion(analyzer, origin, destination, duration):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer["graph"], origin, destination)
    if edge is None:
        gr.addEdge(analyzer["graph"], origin, destination, duration)
    else:
        edge["weight"] = (edge["weight"]+int(duration))/2
    
    return analyzer

# ==============================
# Funciones de consulta
# ==============================
def TotaldeClusteres(analyzer):
    A = scc.KosarajuSCC(analyzer["graph"])
    return scc.connectedComponents(A)
def ClusterPresence(analyzer,id1,id2):
    A = scc.KosarajuSCC(analyzer["graph"])
    return scc.stronglyConnected(A, id1, id2)
def TotalDeVertices(analyzer):
    return gr.numVertices(analyzer["graph"])
def TotalDeArcos(analyzer):
    return gr.numEdges(analyzer["graph"])
def vertexNames(analyzer):
    N = dfo.DepthFirstOrder(analyzer["graph"])
    return N["pre"]

# ==============================
# Funciones Helper
# ==============================

def top3llegada(analyzer):
    arrivetree = om.newMap(omaptype="RBT", comparefunction=compareIds)
    pqiterator = it.newIterator(vertexNames(analyzer))
    while it.hasNext(pqiterator):
        vert = int(it.next(pqiterator))
        om.put(arrivetree, gr.indegree(analyzer["graph"], str(vert)), vert)
    mayorllegada = []
    i = 0
    while i < 3:
        C = om.values(arrivetree, om.maxKey(arrivetree), om.maxKey(arrivetree))
        maxima = lt.firstElement(C)
        mayorllegada.append(maxima)
        om.deleteMax(arrivetree)
        i+=1
    del arrivetree
    estaciones = []
    for i in mayorllegada:
        H = m.get(analyzer["nameIndex"], str(i))
        G = me.getValue(H)
        estaciones.append(G)
    return estaciones

def top3salida(analyzer):
    startree = om.newMap(omaptype="RBT", comparefunction=compareIds)
    pqiterator = it.newIterator(vertexNames(analyzer))
    while it.hasNext(pqiterator):
        vert = int(it.next(pqiterator))
        om.put(startree, gr.outdegree(analyzer["graph"], str(vert)), vert)
    mayorsalida = []
    i = 0
    while i < 3:
        C = om.values(startree, om.maxKey(startree), om.maxKey(startree))
        maxima = lt.firstElement(C)
        mayorsalida.append(maxima)
        om.deleteMax(startree)
        i+=1
    del startree
    estaciones = []
    for i in mayorsalida:
        H = m.get(analyzer["nameIndex"], str(i))
        G = me.getValue(H)
        estaciones.append(G)
    return estaciones

def top3menosUsadas(analyzer):
    totaltree = om.newMap(omaptype="RBT", comparefunction=compareIds)
    pqiterator = it.newIterator(vertexNames(analyzer))
    while it.hasNext(pqiterator):
        vert = int(it.next(pqiterator))
        usototal = (gr.outdegree(analyzer["graph"], str(vert)) + gr.indegree(analyzer["graph"], str(vert)))
        om.put(totaltree, usototal, vert)
    menortotal = []
    i = 0
    while i < 3:
        C = om.values(totaltree, om.minKey(totaltree), om.minKey(totaltree))
        minima = lt.firstElement(C)
        menortotal.append(minima)
        om.deleteMin(totaltree)
        i+=1
    del totaltree
    estaciones = []
    for i in menortotal:
        H = m.get(analyzer["nameIndex"], str(i))
        G = me.getValue(H)
        estaciones.append(G)
    return estaciones

# ==============================
# Funciones de Comparacion
# ==============================
def compareIds(id1, id2):
    """
    Compara dos crimenes
    """
    if (id1 == id2):
        return 0
    elif id1 > id2:
        return 1
    else:
        return -1

def comparer(stop, keyvaluestop):
    """
    Compara dos estaciones
    """
    stopcode = keyvaluestop['key']
    if (stop == stopcode):
        return 0
    elif (stop > stopcode):
        return 1
    else:
        return -1