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


import sys
import config
from App import controller
from DISClib.ADT import stack
from DISClib.DataStructures import listiterator as it
import timeit
from time import process_time
assert config
from DISClib.Algorithms.Graphs import scc
from DISClib.ADT import graph
from  DISClib.ADT import map as m

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Variables
# ___________________________________________________

def printReq3(resp):
    print("\n")
    print("TOP 3 ESTACIONES DE SALIDA")
    itresp = it.newIterator(resp["salidas"])
    while it.hasNext(itresp):
        M = it.next(itresp)
        print("- "+M)
    print("\n")
    print("TOP 3 ESTACIONES DE DESTINO")
    itresp2 = it.newIterator(resp["llegadas"])
    while it.hasNext(itresp2):
        F = it.next(itresp2)
        print("- "+F)
    print("\n")
    print("TOP 3 ESTACIONES MENOS USADAS")
    itresp3 = it.newIterator(resp["usadas"])
    while it.hasNext(itresp3):
        R = it.next(itresp3)
        print("- "+R)

def printReq5(resp):
    print("\n")
    print("ESTACIÓN DE SALIDA MÁS POPULAR")
    print("- "+resp["salida"])
    print("\n")
    print("ESTACIÓN DE DESTINO MÁS POPULAR")
    print("- "+resp["destino"])
    print("\n")
    if resp["tiempo"] == None:
        print("No existe un tiempo mínimo de una ruta directa")
    else:
        print("TIEMPO MÍNIMO ENTRE AMBAS ESTACIONES")
        print(resp["tiempo"]+" segundos")
# ___________________________________________________
#  Menu principal
def Menu():
    print("\n")
    print("🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞")
    print("Bienvenido")
    print("I) Iniciar el catalogo")
    print("0) Cargar archivos al catalogo")
    print("1) REQ. 1: Cantidad de clusters de Viajes ")
    print("2) REQ. 2: Ruta turística Circular ")
    print("3) REQ. 3: Estaciones críticas")
    print("4) REQ. 4: Ruta turística por resistencia ")
    print("5) REQ. 5: Recomendador de Rutas ")
    print("6) REQ. 6: Ruta de interés turístico ")
    print("7) Cerrar App")
    print("🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞🍞")

# ___________________________________________________

"""
Menu principal
"""
def Req1(analyzer):
    id1 = input("ID de la primera estación: ")
    id2 = input("ID de la segunda estacion: ")
    t = controller.totaldeclusters(analyzer)
    p = controller.clusterentre2id(analyzer,id1,id2)
    print("Total de clústeres: ",t)
    print("¿Hay componentes fuertemente conectados entre los 2 ids?: ",p)

def OpcionesMenu():
    analyzer = None
    A = True
    while A is True:
        Menu()
        Kaneki = str(input("Seleccione una opción:"))

        if Kaneki == "I":
            analyzer = controller.InitCatalog()
            if analyzer != None:  
                print("Catalogo creado")
                sys.setrecursionlimit(20000)
                print("Limite de recursión ajustado a: " + str(sys.getrecursionlimit())) 
            else:
                print("Error al cargar el catalogo")
        
        elif Kaneki == "1":
            Req1(analyzer)

        elif Kaneki == "0":
            t1 = process_time()
            Data = controller.loadTrips(analyzer)
            t2 = process_time()
            print("Se cargaron los archivos:")
            print("\n")
            for n in Data:
                print(n)
            print("Tiempo",t2-t1)
        

        elif Kaneki == "2":
            origen = str(input("Escriba la estación de partida: "))
            limites = input("¿Limites de tiempo de 180 a 210 minutos?(True/False): ")
            t1 = process_time()
            Ciclos = controller.CiclosIdealesTurismo(analyzer, origen, limites)
            t2 = process_time()
            if Ciclos == False:
                print("Desde esta estación no se obtuvieron rutas ciclicas")
            elif Ciclos == "Vacio":
                print("Ninguna de las rutas ciclicas cumple con los tiempos establecidos")
            else:
                print("La(s) ruta(s) ideal(es) para hacer turismo desde esa estación es/son: ")
                for I in Ciclos:
                    print(graph.edges(Ciclos[I]))
                    prin("----------------------------------------------------------------------------")
            print("Tiempo de ejecución: ",t2-t1)     
        elif Kaneki == "6":  
            LatIn = str(input("Latitud inicio: "))
            LonIn = str(input("Longitud inicial: "))
            LatFi = str(input("latitud final: "))
            LonFi = str(input("Longitud final: "))
            A = controller.RutaDeTurismo(LatIn, LonIn, LatFi, LonFi, analyzer)
            print(A)
            
            


        elif Kaneki == "3":
            X = controller.estacionesCriticas(analyzer)
            printReq3(X)

        elif Kaneki == "5":
            G = input("Ingrese su rango de edad (0-10, 11-20, 21-30, 31-40, 41-50, 51-60, 60+): ")
            J = controller.recomendarRutas(analyzer, G)
            printReq5(J)

        elif Kaneki == "7":
            A = False
OpcionesMenu()

