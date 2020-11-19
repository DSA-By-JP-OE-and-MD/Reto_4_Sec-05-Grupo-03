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
    return analyzer


# ___________________________________________________

# ___________________________________________________
#  Funciones para consultas
# ___________________________________________________
def totaldeclusters(analyzer):
    return model.TotaldeClusteres(analyzer)
def clusterentre2id(analyzer,id1,id2):
    return model.ClusterPresence(analyzer,id1,id2)

def estacionesCriticas(analyzer):
    A = model.top3llegada(analyzer)
    B = model.top3salida(analyzer)
    C = model.top3menosUsadas(analyzer)
    N = {"llegadas":B,
         "salidas":A,
         "usadas":C}
    return N
 