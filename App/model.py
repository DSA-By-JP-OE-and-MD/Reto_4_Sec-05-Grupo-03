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
from DISClib.Utils import Haversine as ha
import config
from DISClib.ADT import queue
from DISClib.ADT import stack
from DISClib.DataStructures import mapentry as me
from DISClib.ADT.graph import gr
from DISClib.DataStructures import edge as ed
from DISClib.ADT import map as m
from DISClib.ADT import list as lt
from DISClib.Algorithms.Sorting import mergesort as merge
from DISClib.DataStructures import listiterator as it
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.DataStructures import adjlist as adj
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
                "graph":None,
                "components":None}
    analyzer["index"] = m.newMap(numelements=1000, 
                                  prime=109345121, 
                                  maptype="CHAINING",
                                  loadfactor=1.0, 
                                  comparefunction=comparerMap)      

    analyzer["graph"] = gr.newGraph(datastructure='ADJ_LIST',
                                  directed=True,
                                  size=1000,
                                  comparefunction=comparer)
    return analyzer

# -----------------------------------------------------

# Funciones para agregar informacion al grafo
def AñadiralIndex(analyzer, route):
    ID = route["start station id"]
    if not m.contains(analyzer["index"], ID):
        m.put(analyzer["index"], ID, route)
    
def AñadirRuta(analyzer, route):
    """
    Si
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
        edge = gr.getEdge(analyzer["graph"], origin, destination)
        edge["Repeticiones"] = 1
    else:
        edge["weight"] = (edge["weight"]+int(duration))
        edge["Repeticiones"] += 1
    
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
"""def CicloMasCorto(analizer, origen):
    Grafos = GrafosPorCiclo(analyzer, origen)
    for A in Grafos:"""
    

# ==============================
# Funciones Helper
# ==============================

def CiclosDelOrigen(analyzer, origen):
    """
    Busca todos los vectores pertenecientes a el/los ciclo(s) fuertemente conectado(s)
    relacionados al origen para tomar los valores de cada ciclo.
    
    """
    #CRAO = Ciclos Relacionados Al Origen
    CRAO = lt.newList(datastructure="ARRAY_LIST")
    Revisar = analyzer["components"]["idscc"]
    a = it.newIterator(m.keySet(Revisar))
    while it.hasNext(a):
        Lector = it.next(a)
        if me.getKey(m.get(Revisar, Lector)) == origen:
            lt.addLast(CRAO, me.getValue(m.get(Revisar, Lector)))
    if lt.size(CRAO) == 0:
        return False
    else:
        return CRAO
    
def LectorDeCiclos(analyzer, origen, CRAO):
    """
    Se crea un diccionario con el valor de cada ciclo al que pertenece el origen,
    cada valor tiene una lista encadenada con los vertices de cada ciclo (excluyendo el origen)

    """
    #VDC = Vertices Del Ciclo
    VDC = {}
    valores = CRAO
    if valores == False:
        return False
    else:
        a = it.newIterator(valores)
        while it.hasNext(a):
            b = it.next(a)
            VDC[b] = lt.newList(datastructure="ARRAY_LIST", cmpfunction=comparador)
            A = it.newIterator(m.keySet(analyzer["components"]["idscc"]))
            while it.hasNext(A):
                B = it.next(A)
                C = me.getValue(m.get(analyzer["components"]["idscc"], B))
                if C == b and C != origen:
                    lt.addLast(VDC[b], B)
        return VDC

def GrafosPorCiclo(analyzer, origen, VDC):
    """
    Genera un grafo por cada ciclo diferente relacionado al origen y los añade a
    GPCC (diccionario)
    """
    #GPCC = Grafos Por Cada Ciclo
    GPCC = {}
    if VDC == False:
        return False
    else:
        for Valor in VDC:
            Cierre = False
            GPCC[Valor] = gr.newGraph(datastructure="ADJ_LIST",
                                        directed=True,
                                        size=6,
                                        comparefunction=comparer)
            gr.insertVertex(GPCC[Valor], origen)
            actual = origen
            mismo = origen
            Adjacentes = adj.adjacents(analyzer["graph"], actual)
            Adjacentes["cmpfunction"] = comparador
            while Cierre == False:
                a = it.newIterator(VDC[Valor])
                while it.hasNext(a):
                    b = it.next(a)
                    if actual != mismo:
                        Adjacentes = adj.adjacents(analyzer["graph"], actual)
                        Adjacentes["cmpfunction"] = comparador
                        mismo = actual
                    if not gr.containsVertex(GPCC[Valor], b):
                        if lt.isPresent(Adjacentes, origen) != 0 and actual != origen and b != origen:
                            gr.insertVertex(GPCC[Valor], b)
                            Tartalia = gr.getEdge(analyzer["graph"], actual, origen)
                            Peso = int(ed.weight(Tartalia)/Tartalia["Repeticiones"])
                            adj.addEdge(GPCC[Valor], actual, origen, Peso)
                            actual = b
                            Cierre = True
                        elif lt.isPresent(Adjacentes, b) != 0 and b != origen:
                            gr.insertVertex(GPCC[Valor], b)
                            Tartalia = gr.getEdge(analyzer["graph"], actual, b)
                            Peso = int(ed.weight(Tartalia)/Tartalia["Repeticiones"])
                            adj.addEdge(GPCC[Valor], actual, b, Peso)
                            actual = b  
                    elif actual == origen and lt.size(VDC[Valor]) == 1:
                            Cierre = True       
        return GPCC

def TiempoNecesario(analyzer, GPCC, limites):
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
        LimiteInferior = 180*60
        LimiteSuperior = 210*60
        for B in Pesos:
            if Pesos[B] >= LimiteInferior and Pesos[B] <= LimiteSuperior:
                Ideal[B] = GPCC[B]
        if len(Ideal) == 0:
            return "Vacio"
        else:
            return Ideal

def EstaciónMasProxima(latO, lonO, analyzer):
    idynombre = []
    prox = lt.newList(datastructure="ARRAY_LIST", cmpfunction=comparador)
    Index = analyzer["index"]
    A = m.keySet(Index)
    a = it.newIterator(A)
    while it.hasNext(a):
        B = it.next(a)
        C = m.get(Index, B)
        B = me.getValue(C)
        latitud = B["start station latitude"]
        longitud = B["start station longitude"]
        distancia = ha.haversine(float(lonO), float(latO), float(longitud), float(latitud))
        B["Distancia al punto"] = distancia
        lt.addLast(prox, B)
    merge.mergesort(prox, MasProximo)
    resultado = lt.firstElement(prox)
    idynombre.append(resultado["start station name"])
    idynombre.append(resultado["start station id"])
    return idynombre

def CaminoMasCorto(latO, lonO, latD, lonD, analyzer):
    EstacionInicio = EstaciónMasProxima(latO, lonO, analyzer)
    EstacionMeta = EstaciónMasProxima(latD, lonD, analyzer)
    M = djk.Dijkstra(analyzer["graph"], EstacionInicio[1])
    if djk.hasPathTo(M, EstacionMeta[1]):
        F = djk.pathTo(M, EstacionMeta[1])
        return F
    else:
        return False
def NombreEspecifico(listapy):
    A = listapy[0]
    return A

def ListaConID(lista):
    A = []
    while stack.size(lista) != 0:
        B = (stack.pop(lista))
        N = B["vertexB"]
        A.append(N)
    return A

def NombresDeUnaLista(lista, analyzer):
    L = []
    I = analyzer["index"]
    for a in lista:
        A = m.get(I, a)
        C = me.getValue(A)
        C = C["start station name"]
        L.append(C)
    return L
def PesoDeLaLista(lista):
    A = 0
    while stack.size(lista) != 0:
        b = (stack.pop(lista))
        n = b["weight"]
        A += float(n)
    return A

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
def comparenames(searchname, element):
    return (searchname == element['key'])

def comparador(key1, key2):
    if key1==key2:
        return 0
    else:
        return -1

def comparerMap(keyname, value):
    entry = me.getKey(value)
    if (keyname == entry):
        return 0
    elif (keyname > entry):
        return 1
    else:
        return -1
def MasProximo(ele1, ele2):
    if float(ele1["Distancia al punto"]) > float(ele2["Distancia al punto"]):
        return True
    return False