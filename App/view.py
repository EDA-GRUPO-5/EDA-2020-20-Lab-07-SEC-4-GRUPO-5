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
 """

import sys
import config
from DISClib.ADT import list as lt
from App import controller
assert config

"""
La vista se encarga de la interacción con el usuario.
Presenta el menu de opciones  y  por cada seleccion
hace la solicitud al controlador para ejecutar la
operación seleccionada.
"""

# ___________________________________________________
#  Ruta a los archivos
# ___________________________________________________


accidentsfileSmall = 'us_accidents_small.csv'
accidentsfile = 'us_accidents_dis_2016.csv'
accidentsfileBIG = 'US_Accidents_BIG.csv'

# ___________________________________________________
#  Menu principal
# ___________________________________________________


def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido\n")
    print("1- Inicializar Analizador")
    print("2- Cargar información de accidentes")
    print("3- Conocer los accidentes en una fecha REQ1")
    print("4- Conocer los accidentes anteriores a una fecha REQ2")
    print("5- Conocer los accidentes en un rango de fechas REQ3")
    print("6- Conocer el estado con mas accidentes REQ4")
    print("7- Conocer los accidentes por rango de horas REQ5")
    print("8- Conocer la zona geográfica mas accidentada REQ6")
    print("9- Usar el conjunto completo de datos REQ7")
    print("0- Salir")
    print("*******************************************")
    print("\n")


"""
Menu principal
"""

while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n>')

    if int(inputs[0]) == 1:
        print("\nInicializando....")
        # cont es el controlador que se usará de acá en adelante
        cont = controller.init()

    elif int(inputs[0]) == 2:
        print("\nCargando información de accidentes....")
        controller.loadData(cont, accidentsfileSmall)
        print('\nAccidentes cargados: ' + str(controller.accidentsSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))

    elif int(inputs[0]) == 3:
        initialDate = input("\nIngrese la fecha (YYYY-MM-DD): ")
        print("\nBuscando accidentes de " + initialDate + "....")
        severity1 = int(controller.getAccidentsBySeverity(cont, initialDate, '1'))
        severity2 = int(controller.getAccidentsBySeverity(cont, initialDate, '2'))
        severity3 = int(controller.getAccidentsBySeverity(cont, initialDate, '3'))
        severity4 = int(controller.getAccidentsBySeverity(cont, initialDate, '4'))
        severities = severity1+severity2+severity3+severity4
        print("\nEn " + initialDate + " ocurrieron " + str(severities) + " accidentes." + 
            " Sus severidades fueron: \n\nSeveridad 1: " + str(severity1) + "\nSeveridad 2: " + str(severity2) +
            "\nSeveridad 3: " + str(severity3) + "\nSeveridad 4: " + str(severity4))

    elif int(inputs[0]) == 4:
        print("\nConociendo los accidentes anteriores a una fecha ")
    
    elif int(inputs[0]) == 5:
        
        centiY, centiM, centiD = True, True, True

        while centiY:
            yyyy1 = int(input('Ingresa el anio inicial\n>'))
            yyyy2 = int(input('Ingresa el anio final\n>'))
            yyyy2, yyyy1 = max(yyyy1, yyyy2), min(yyyy1, yyyy2)

            if (999 < yyyy1 < 2999 and 999 < yyyy2 < 2999):
                centiY = False
            else:
                print('Ingrese anios validos')

        while centiM:
            mm1 = int(input('Ingresa el mes inicial\n>'))
            mm2 = int(input('Ingresa el mes final\n>'))

            if yyyy1 == yyyy2:
                mm2,mm1 = max(mm1,mm2), min(mm1,mm2)

            if (0 < mm1 < 13 and 0 < mm2 < 13):
                centiM = False
            else:
                print('Ingrese meses validos')

        while centiD:
            dd1 = int(input('Ingresa el dia inicial\n>'))
            dd2 = int(input('Ingresa el dia final\n>'))

            if (yyyy1 == yyyy2) and (mm1 == mm2):
                dd2, dd1 = max(dd1,dd2), min(dd2,dd1)

            if (0 < dd1 < 32 and 0 < dd2 < 32):
                centiD = False
            else:
                print('Ingresa un dias validos')
        
        dateMin = f'{yyyy1}-{mm1:02}-{dd1:02}'
        dateMax = f'{yyyy2}-{mm2:02}-{dd2:02}'
        print(f"\nBuscando accidentes en el rango de fechas <{dateMin}> - <{dateMax}>...")
        total, sev = controller.getAccidentsByDates(cont, dateMin, dateMax)
        print(f'La cantidad de accidentes entre <{dateMin}> y <{dateMax}> son: {total}')
        print(f'La categoria mas recurrente es: {sev}')

    elif int(inputs[0]) == 6:
        print("\nBuscando el estado con más accidentes: ")

    elif int(inputs[0]) == 7:
        
        centiH, centiM, cetinD = True, True, True

        while centiH:
            hh1 = int(input('Ingrese la hora inicial\n>'))
            hh2 = int(input('Ingrese la hora final\n>'))

            hh2, hh1 = max(hh1, hh2), min(hh1, hh2)

            if (-1 < hh1 < 24) and (-1 < hh2 < 24):
                centiH = False
            else:
                print('Ingrese horas validas\n')
        
        while centiM:
            mm1 = int(input('Ingrese el minuto inicial\n>'))
            mm2 = int(input('Ingrese el minuto final\n>'))

            if (0 <= mm1 < 60) and (0 <= mm2 < 60):
                centiM = False

                if hh1 == hh2:
                    mm2,mm1 = max(mm1,mm2),min(mm1,mm2)

                if mm1 > 30:
                    mm1 = 0
                    hh1 += 1
                elif 0 < mm1 < 30:
                    mm1 = 30
                
                if mm2 > 30:
                    mm2 = 0
                    hh2 += 1
                elif 0 < mm2 < 30:
                    mm2 = 30
            else:
                print('Ingrese minutos validos\n')
        
        initialTime = f'{hh1:02}:{mm1:02}'
        finalTime = f'{hh2:02}:{mm2:02}'

        print(f'\nConociendo accidentes en el rango de horas <{initialTime}>-<{finalTime}>...')
        rta, total = controller.getAccidentsByHours(cont, initialTime, finalTime)
        print(f'Hay {total} accidentes en el rango de horas <{initialTime}>-<{finalTime}>:')
        print(f'Categoria 1: {lt.getElement(rta, 1)[0]} (Aportando un {lt.getElement(rta, 1)[1]} %)')
        print(f'Categoria 2: {lt.getElement(rta, 2)[0]} (Aportando un {lt.getElement(rta, 2)[1]} %)')
        print(f'Categoria 3: {lt.getElement(rta, 3)[0]} (Aportando un {lt.getElement(rta, 3)[1]} %)')
        print(f'Categoria 4: {lt.getElement(rta, 4)[0]} (Aportando un {lt.getElement(rta, 4)[1]} %)')
    
    elif int(inputs[0]) == 8:
        print("\nZona geografica más accidentada: ")

    elif int(inputs[0]) == 9:
        print("\n------======<Precaucion>======------\nSe recomienda Cerrar toda pestaña para evitar que su computador explote\nCargando información de accidentes (archivo grande)....")

        controller.loadData(cont, accidentsfileBIG)
        print('\nAccidentes cargados: ' + str(controller.accidentsSize(cont)))
        print('Altura del arbol: ' + str(controller.indexHeight(cont)))
        print('Elementos en el arbol: ' + str(controller.indexSize(cont)))
        print('Menor Llave: ' + str(controller.minKey(cont)))
        print('Mayor Llave: ' + str(controller.maxKey(cont)))
    else:
        sys.exit(0)
sys.exit(0)
