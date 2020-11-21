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
assert config

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
    for i in resp["salidas"]:
        print("- "+i)
    print("\n")
    print("TOP 3 ESTACIONES DE DESTINO")
    for i in resp["llegadas"]:
        print("- "+i)
    print("\n")
    print("TOP 3 ESTACIONES MENOS USADAS")
    itresp = it.newIterator(resp["usadas"])
    while it.hasNext(itresp):
        R = it.next(itresp)
        print("- "+R)
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
            else:
                print("Error al cargar el catalogo")
        
        elif Kaneki == "1":
            Req1(analyzer)

        elif Kaneki == "0":
            Data = controller.loadTrips(analyzer)
            print("Se cargaron los archivos:")
            print("\n")
            for n in Data:
                print(n)

        elif Kaneki == "3":
            X = controller.estacionesCriticas(analyzer)
            printReq3(X)

        elif Kaneki == "7":
            A = False
OpcionesMenu()