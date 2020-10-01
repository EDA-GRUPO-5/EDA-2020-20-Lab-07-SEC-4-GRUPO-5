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
import config
from DISClib.ADT import list as lt
from DISClib.ADT import orderedmap as om
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import map as m
import datetime
assert config

"""
En este archivo definimos los TADs que vamos a usar,
es decir contiene los modelos con los datos en memoria

Se define la estructura de un catálogo de libros.
El catálogo tendrá  una lista para los libros.

Los autores, los tags y los años se guardaran en
tablas de simbolos.
"""

# -----------------------------------------------------
# API del TAD Catalogo de Libros
# -----------------------------------------------------


def newAnalyzer():
    """ Inicializa el analizador

    Crea una lista vacia para guardar todos los accidentes
    Se crean indices (Maps) por los siguientes criterios:
    -Fechas

    Retorna el analizador inicializado.
    """
    analyzer = {'accidents': None,
                'dateIndex': None
                }

    analyzer['accidents'] = lt.newList('SINGLE_LINKED', compareIds)
    analyzer['dateIndex'] = om.newMap(omaptype='BST',
                                      comparefunction=compareDates)
    return analyzer


# Funciones para agregar informacion al catalogo


def addAccident(analyzer, accident):
    """
    """
    lt.addLast(analyzer['accidents'], accident)
    updateDateIndex(analyzer['dateIndex'], accident)
    return analyzer


def updateDateIndex(map, accident):
    """
    Se toma la fecha del accidente y se busca si ya existe en el arbol
    dicha fecha.  Si es asi, se adiciona a su lista de accidentes
    y se actualiza el indice de tipos de accidentes.

    Si no se encuentra creado un nodo para esa fecha en el arbol
    se crea y se actualiza el indice de tipos de accidentes
    """
    start_time = accident['Start_Time']
    accidentdate = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
    entry = om.get(map, accidentdate.date())
    if entry is None:
        datentry = newDataEntry(accident)
        om.put(map, accidentdate.date(), datentry)
    else:
        datentry = me.getValue(entry)
    addDateIndex(datentry, accident)
    return map


def addDateIndex(datentry, accident):
    """
    Actualiza un indice de tipo de accidentes.  Este indice tiene una lista
    de accidentes y una tabla de hash cuya llave es el tipo de accidentes y
    el valor es una lista con los accidentes de dicho tipo en la fecha que
    se está consultando (dada por el nodo del arbol)
    """
    lst = datentry['lstaccidents']
    lt.addLast(lst, accident)
    severityIndex = datentry['severityIndex']
    offentry = m.get(severityIndex, accident['Severity'])
    if (offentry is None):
        entry = newSeverityEntry(accident['Severity'], accident)
        lt.addLast(entry['lstseverities'], accident)
        m.put(severityIndex, accident['Severity'], entry)
    else:
        entry = me.getValue(offentry)
        lt.addLast(entry['lstseverities'], accident)
    return datentry


def newDataEntry(accident):
    """
    Crea una entrada en el indice por fechas, es decir en el arbol
    binario.
    """
    entry = {'severityIndex': None, 'lstaccidents': None}
    entry['severityIndex'] = m.newMap(numelements=30,
                                     maptype='PROBING',
                                     comparefunction=compareSeverities)
    entry['lstaccidents'] = lt.newList('SINGLE_LINKED', compareDates)
    return entry


def newSeverityEntry(severitygrp, accident):
    """
    Crea una entrada en el indice por tipo de crimen, es decir en
    la tabla de hash, que se encuentra en cada nodo del arbol.
    """
    ofentry = {'severity': None, 'lstseverities': None}
    ofentry['severity'] = severitygrp
    ofentry['lstseverities'] = lt.newList('SINGLELINKED', compareSeverities)
    return ofentry


# ==============================
# Funciones de consulta
# ==============================


def accidentSize(analyzer):
    """
    Número de libros en el catago
    """
    return lt.size(analyzer['accidents'])


def indexHeight(analyzer):
    """Numero de autores leido
    """
    return om.height(analyzer['dateIndex'])


def indexSize(analyzer):
    """Numero de autores leido
    """
    return om.size(analyzer['dateIndex'])


def minKey(analyzer):
    """Numero de autores leido
    """
    return om.minKey(analyzer['dateIndex'])


def maxKey(analyzer):
    """Numero de autores leido
    """
    return om.maxKey(analyzer['dateIndex'])


def getAccidentsBySeverity(analyzer, initialDate, severity):
    accidentdate = om.get(analyzer['dateIndex'], initialDate)
    if accidentdate['key'] is not None:
        severitymap = me.getValue(accidentdate)['severityIndex']
        numseverities = m.get(severitymap, severity)
        if numseverities is not None:
            return m.size(me.getValue(numseverities)['lstseverities'])
        return 0
        
def getAccidentsByRange(analyzer, initialDate, finalDate):
    """
    Retorna el numero de accidentes en un rango de fechas.
    """
    lst = om.values(analyzer['dateIndex'], initialDate, finalDate)
    
    d = {'1': 0,'2': 0,'3':0, '4':0}

    for i in range(lt.size(lst)):
        d['1'] += int(getAccidentsBySeverity(analyzer, lt.getElement(lst, i), '1'))
        d['2'] += int(getAccidentsBySeverity(analyzer, lt.getElement(lst, i), '2'))
        d['3'] += int(getAccidentsBySeverity(analyzer, lt.getElement(lst, i), '3'))
        d['4'] += int(getAccidentsBySeverity(analyzer, lt.getElement(lst, i), '4'))
    
    rtaSeverityMostCommon= max(d, key=d.get)
    return sum(d.values()), rtaSeverityMostCommon


def getAccidentsByHours(analyzer, initialHour, finalHour):
    """
    Retorna los accidentes ocurridos en un rango de horas(aproximadas)
    """
    lst = om.values(analyzer['dateIndex'], om.minKey(analyzer['dateIndex']), om.maxKey(analyzer['dateIndex']))

    rta = {'1': 0,'2': 0,'3':0, '4':0}

    #for i in range(lt.size(lst)):
    for i in range(2):
        k = lt.getElement(lst, i)
        originalMap = me.getValue(om.get(analyzer['dateIndex'], k))['severityIndex']
        d1 = m.get(originalMap, '1')
        d2 = m.get(originalMap, '2')
        d3 = m.get(originalMap, '3')
        d4 = m.get(originalMap, '4')


        if d1 is not None:
            l1 = me.getValue(d1)['lstseverities']
            for j1 in range(lt.size(l1)):
                if (initialHour < datetime.datetime.strptime(lt.getElement(l1, j1)['Start_Time'][-8:-3], '%H:%M') < finalHour):
                    rta['1'] += 1
            
        if d2 is not None:
            l2 = me.getValue(d2)['lstseverities']
            for j2 in range(lt.size(l2)):
                if (initialHour < datetime.datetime.strptime(lt.getElement(l2, j2)['Start_Time'][-8:-3], '%H:%M') < finalHour):
                    rta['2'] += 1

        if d3 is not None:
            l3 = me.getValue(d3)['lstseverities']
            for j3 in range(lt.size(l3)):
                if (initialHour < datetime.datetime.strptime(lt.getElement(l3, j3)['Start_Time'][-8:-3], '%H:%M') < finalHour):
                    rta['3'] += 1

        if d4 is not None:
            l4 = me.getValue(d4)['lstseverities']
            for j4 in range(lt.size(l4)):
                if (initialHour < datetime.datetime.strptime(lt.getElement(l4, j4)['Start_Time'][-8:-3], '%H:%M') < finalHour):
                    rta['4'] += 1
        
        t = sum(rta.values())
        xd = {x: rta[x]*100/t for x in rta} if t != 0 else {x :0.0 for x in rta}
        return rta, xd, t


def getCrimesByRangeCode(analyzer, initialDate, offensecode):
    """
    Para una fecha determinada, retorna el numero de crimenes
    de un tipo especifico.
    """
    crimedate = om.get(analyzer['dateIndex'], initialDate)
    if crimedate['key'] is not None:
        offensemap = me.getValue(crimedate)['offenseIndex']
        numoffenses = m.get(offensemap, offensecode)
        if numoffenses is not None:
            return m.size(me.getValue(numoffenses)['lstoffenses'])
        return 0
    

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


def compareDates(date1, date2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    if (date1 == date2):
        return 0
    elif (date1 > date2):
        return 1
    else:
        return -1


def compareSeverities(severity1, severity2):
    """
    Compara dos ids de libros, id es un identificador
    y entry una pareja llave-valor
    """
    severity = me.getKey(severity2)
    if (severity1 == severity):
        return 0
    elif (severity1 > severity):
        return 1
    else:
        return -1
