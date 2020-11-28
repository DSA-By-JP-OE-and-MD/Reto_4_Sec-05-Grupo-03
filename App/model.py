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
from DISClib.ADT import list as lt
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
def analyzer():
    analyzer = {"index":None,
                "graph":None}
    analyzer["index"] = m.newMap(numelements=1000, 
                                  prime=109345121, 
                                  maptype="CHAINING",
                                  loadfactor=1.0, 
                                  comparefunction=None)      

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
    duration = int(route['tripduration'])
    AñadirEstacion(analyzer, origin)
    AñadirEstacion(analyzer, destination)
    AñadirConeccion(analyzer, origin, destination, duration)

def  AñadirEstacion(analyzer, estacion):
    if not gr.containsVertex(analyzer["graph"], estacion):
        gr.insertVertex(analyzer["graph"], estacion)
    return analyzer

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

# ==============================
# Funciones Helper
# ==============================
def TiempoNecesariomod(analyzer, GPCC, limites):
    if GPCC == False:
        return False
    else:
        Ideal = {}
        Pesos = {}
        for A in GPCC:
            Pesos[A] = 0
            n = it.newIterator(gr.edges(GPCC[A]))
            if it.hasNext(n):
                d = it.next(n)
                Pesos[A] += ed.weight(d)
        LimiteInferior = 0*60
        LimiteSuperior = limites*60
        for B in Pesos:
            if Pesos[B] >= LimiteInferior and Pesos[B] <= LimiteSuperior:
                Ideal[B] = GPCC[B]
        if len(Ideal) == 0:
            return "Vacio"
        else:
            return Ideal
# ==============================
# Funciones de Comparacion
# ==============================
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