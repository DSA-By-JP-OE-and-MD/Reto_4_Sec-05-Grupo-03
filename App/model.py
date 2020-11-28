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
from DISClib.Algorithms.Sorting import mergesort as mrg
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
def analyzer():
    analyzer = {"routeList":None,
                "nameIndex":None,
                "graph":None}

    analyzer["routeList"] = lt.newList(datastructure="SINGLE_LINKED",
                                       cmpfunction=compareIds)

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
    lt.addLast(analyzer["routeList"], route)
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
def vertexNamesAge(grafo):
    N = dfo.DepthFirstOrder(grafo)
    return N["pre"]

# ==============================
# Funciones Helper
# ==============================


def grafoEdades(listaViajes):
    grafo = gr.newGraph(datastructure="ADJ_LIST",
                        directed=True,
                        size=1000,
                        comparefunction=comparer)
    iteEdades = it.newIterator(listaViajes)
    while it.hasNext(iteEdades):
        viaje = it.next(iteEdades)
        estacion1 = viaje["start station id"]
        estacion2 = viaje["end station id"]
        duracion = int(viaje["tripduration"])
        if not gr.containsVertex(grafo, estacion1):
            gr.insertVertex(grafo, estacion1)
        if not gr.containsVertex(grafo, estacion2):
            gr.insertVertex(grafo, estacion2)
        gr.addEdge(grafo, estacion1, estacion2, duracion)
    return grafo

def top3llegada(analyzer):
    intree = om.newMap(omaptype="RBT", comparefunction=compareIds)
    pqiterator = it.newIterator(vertexNames(analyzer))
    while it.hasNext(pqiterator):
        vert = int(it.next(pqiterator))
        llegadas = gr.indegree(analyzer["graph"], str(vert))
        if not om.contains(intree, llegadas):
            om.put(intree, llegadas, str(vert))
        else:
            A = om.get(intree, llegadas)
            B = me.getValue(A)
            om.put(intree, llegadas, str(B)+","+str(vert))
    estaciones = lt.newList(datastructure="ARRAY_LIST")
    while lt.size(estaciones) < 3:
        val = om.get(intree, om.maxKey(intree))
        val1 = me.getValue(val)
        mayorllegada = val1.split(",")
        for i in mayorllegada:
            if lt.size(estaciones) < 3:
                K = m.get(analyzer["nameIndex"], i)
                L = me.getValue(K)
                lt.addLast(estaciones, L)
        om.deleteMax(intree)
    return estaciones

def top3salida(analyzer):
    outree = om.newMap(omaptype="RBT", comparefunction=compareIds)
    pqiterator = it.newIterator(vertexNames(analyzer))
    while it.hasNext(pqiterator):
        vert = int(it.next(pqiterator))
        salidas = gr.outdegree(analyzer["graph"], str(vert))
        if not om.contains(outree, salidas):
            om.put(outree, salidas, str(vert))
        else:
            A = om.get(outree, salidas)
            B = me.getValue(A)
            om.put(outree, salidas, str(B)+","+str(vert))
    estaciones = lt.newList(datastructure="ARRAY_LIST")
    while lt.size(estaciones) < 3:
        val = om.get(outree, om.maxKey(outree))
        val1 = me.getValue(val)
        mayorsalida = val1.split(",")
        for i in mayorsalida:
            if lt.size(estaciones) < 3:
                K = m.get(analyzer["nameIndex"], i)
                L = me.getValue(K)
                lt.addLast(estaciones, L)
        om.deleteMax(outree)
    return estaciones

def top3lessUsed(analyzer):
    totaltree = om.newMap(omaptype="RBT", comparefunction=compareIds)
    pqiterator = it.newIterator(vertexNames(analyzer))
    while it.hasNext(pqiterator):
        vert = int(it.next(pqiterator))
        salidas = gr.outdegree(analyzer["graph"], str(vert))
        destinos = gr.indegree(analyzer["graph"], str(vert))
        usototal = salidas + destinos
        if not om.contains(totaltree, usototal):
            om.put(totaltree, usototal, str(vert))
        else:
            A = om.get(totaltree, usototal)
            B = me.getValue(A)
            om.put(totaltree, usototal, str(B)+","+str(vert))
    estaciones = lt.newList(datastructure="ARRAY_LIST")
    while lt.size(estaciones) < 3:
        val = om.get(totaltree, om.minKey(totaltree))
        val1 = me.getValue(val)
        menortotal = val1.split(",")
        for i in menortotal:
            if lt.size(estaciones) < 3:
                K = m.get(analyzer["nameIndex"], i)
                L = me.getValue(K)
                lt.addLast(estaciones, L)
        om.deleteMin(totaltree)
    return estaciones

def majorStart(grafo):
    outree = om.newMap(omaptype="RBT", comparefunction=compareIds)
    pqiterator = it.newIterator(vertexNamesAge(grafo))
    while it.hasNext(pqiterator):
        vert = it.next(pqiterator)
        salidas = gr.outdegree(grafo, vert)
        om.put(outree, salidas, vert)
    if om.isEmpty(outree):
        return None
    else:
        mayor = om.get(outree, om.maxKey(outree))
        mayornombre = me.getValue(mayor)
        return mayornombre

def majorDestiny(grafo):
    intree = om.newMap(omaptype="RBT", comparefunction=compareIds)
    pqiterator = it.newIterator(vertexNamesAge(grafo))
    while it.hasNext(pqiterator):
        vert = it.next(pqiterator)
        salidas = gr.indegree(grafo, vert)
        om.put(intree, salidas, vert)
    if om.isEmpty(intree):
        return None
    else:
        mayor = om.get(intree, om.maxKey(intree))
        mayornombre = me.getValue(mayor)
        return mayornombre

def crearGrafoEdad(analyzer, agerange):
    if agerange == "60+":
        rango = [60, 150]
    else:
        rango = agerange.split("-")
    listaPorEdad = lt.newList(datastructure="SINGLE_LINKED", cmpfunction=compareIds)
    routeiterator = it.newIterator(analyzer["routeList"])
    while it.hasNext(routeiterator):
        ruta = it.next(routeiterator)
        edad = 2020 - int(ruta["birth year"])
        if int(rango[0]) <= edad <= int(rango[1]):
            lt.addLast(listaPorEdad, ruta)
    ageGraph = grafoEdades(listaPorEdad)
    return {"grafo":ageGraph, "lista":listaPorEdad}

def recomendarRutas(analyzer, agerange):
    ageGraph = crearGrafoEdad(analyzer, agerange)
    mayorsalida = majorStart(ageGraph["grafo"])
    mayordestino = majorDestiny(ageGraph["grafo"])
    if mayorsalida == None or mayordestino == None:
        return "No existen rutas para este rango de edad"
    else:
        pesos = lt.newList(datastructure="ARRAY_LIST")
        pathiterator = it.newIterator(ageGraph["lista"])
        while it.hasNext(pathiterator):
            viaje = it.next(pathiterator)
            if viaje["start station id"] == mayorsalida and viaje["end station id"] == mayordestino:
                lt.addLast(pesos, viaje["tripduration"])
        if lt.isEmpty(pesos):
            econ = None
        else:
            mrg.mergesort(pesos, lessfunction)
            econ = lt.firstElement(pesos)
        sal = m.get(analyzer["nameIndex"], mayorsalida)
        salnombre = me.getValue(sal)
        dest = m.get(analyzer["nameIndex"], mayordestino)
        destnombre = me.getValue(dest)
        W = {"salida":salnombre,
             "destino":destnombre,
             "tiempo":econ}
        return W


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

def lessfunction(ele1, ele2):
    if ele1 < ele2:
        return True
    return False