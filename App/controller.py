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
from DISClib.ADT import graph
from DISClib.Algorithms.Graphs import scc
import config as cf
from App import model
from DISClib.ADT import orderedmap as om
import csv
import os
"""
El controlador se encarga de mediar entre la vista y el modelo.
Existen algunas operaciones en las que se necesita invocar
el modelo varias veces o integrar varias de las respuestas
del modelo en una sola respuesta.  Esta responsabilidad
recae sobre el controlador.
"""

# ___________________________________________________
#  Inicializacion del catalogo
def InitCatalog():
    Analyzer = model.analyzer()
    return Analyzer
# ___________________________________________________

def NoelleImpacto(analyzer, origen):
    A = model.GrafosPorCiclo(analyzer, origen)
    if A == False:
        return "No se pueden encontrar ciclos con esta estación"
    else:
        return A

# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
def loadTrips(analyzer):
    archivos = []
    for filename in os.listdir(cf.data_dir):
        if filename.endswith('.csv'):
            archivos.append(filename)
            loadFile(analyzer, filename)
    V = model.TotalDeVertices(analyzer)
    A = model.TotalDeArcos(analyzer)
    K = model.TotaldeClusteres(analyzer)
    archivos.append({"Total de Vertices":V})
    archivos.append({"Total de Arcos":A})
    archivos.append({"Total de Clusteres":K})
    return archivos


    
def loadFile(analyzer, file):
    """
    """
    file = cf.data_dir + file
    input_file = csv.DictReader(open(file, encoding="utf-8"),
                                delimiter=",")
    for route in input_file:
        model.AñadirRuta(analyzer, route)
    analyzer['components'] = scc.KosarajuSCC(analyzer['graph'])
        
    return analyzer


# ___________________________________________________

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def totaldeclusters(analyzer):
    return model.TotaldeClusteres(analyzer)
def clusterentre2id(analyzer,id1,id2):
    return model.ClusterPresence(analyzer,id1,id2)

def CiclosIdealesTurismomod(analyzer, origen, limites):
    A = model.CiclosDelOrigen(analyzer, origen)
    B = model.LectorDeCiclos(analyzer, origen, A)
    C = model.GrafosPorCiclo(analyzer, origen, B)
    D = model.TiempoNecesario(analyzer, C)
    
def CiclosIdealesTurismo(analyzer, origen, limites):
    A = model.CiclosDelOrigen(analyzer, origen)
    B = model.LectorDeCiclos(analyzer, origen, A)
    C = model.GrafosPorCiclo(analyzer, origen, B)
    if limites == True:
        D = model.TiempoNecesario(analyzer, C)
        return D
    else:
        return C

def estacionesCriticas(analyzer):
    A = model.top3llegada(analyzer)
    B = model.top3salida(analyzer)
    C = model.top3lessUsed(analyzer)
    N = {"llegadas":A,
         "salidas":B,
         "usadas":C}
    return N

def recomendarRutas(analyzer, agerange):
    return model.recomendarRutas(analyzer, agerange)
