# -*- coding: utf-8 -*-
"""
Created on Mon Oct 11 18:27:13 2021

@author: Sergio Alejandro Sánchez Juárez
"""

import csv

# Lista con datos del archivo csv
sinergy_database = []

# Administrador de contexto con with
with open("synergy_logistics_database.csv", "r") as archivo:
    lector = csv.DictReader(archivo)

    for registro in lector:
        sinergy_database.append(registro)


# =============================================================================
# Opción 1) Rutas de importación y exportación. Synergy logistics está 
# considerando la posibilidad de enfocar sus esfuerzos en las 10 rutas más 
# demandadas.
# =============================================================================

# Funcion para opcion 1
def rutas_exportacion_importacion (direccion):
    contador = 0     # Variable de cantidad de registros de la ruta
    totales = 0 # Variable para los valores totales de la ruta
    rutas_revisadas = []    #Origen, destino de la ruta
    rutas = []  #Origen, destino, contador, totales y transporte

    for ruta in sinergy_database:
        # Si es la misma direccion, obtenemos una ruta actual a buscar
        if ruta["direction"] == direccion:
            ruta_actual = [ruta["origin"], ruta["destination"]]
            transporte = []
            # Si ruta actual no esta en la lista, procedera a buscarla
            if ruta_actual not in rutas_revisadas:
                for n_ruta in sinergy_database:
                    # Si coincide la ruta actual, se incrementa al contador y se suma el total_value, ademas de verificar que medios de transporte usa la ruta
                    if ruta_actual == [n_ruta["origin"], n_ruta["destination"]] and n_ruta["direction"] == direccion and int(n_ruta["total_value"]) != 0:
                        contador += 1
                        totales += int(n_ruta["total_value"])
                        if n_ruta["transport_mode"] not in transporte:
                            transporte.append(n_ruta["transport_mode"])
                        
                # Se agrega un nuevo elemento a la listas correspondientes, y se reinician variables de calculos
                rutas_revisadas.append(ruta_actual)
                rutas.append([ruta["origin"], ruta["destination"], contador, totales, transporte])
                contador = 0
                totales = 0
                
    #Se ordena la lista
    rutas.sort(reverse = True, key = lambda x:x[3])
    
    return rutas


# Funcion para imprimir en forma tabular la informacion requerida de las rutas demandadas
def mostrar_rutas(rutas):
    print(f"{'Origen':20} {'Destino':20} {'Operaciones':11} {'Valores totales':15} {'Transporte':20}\n")
    for i in range(0, 10):
        print(f"{rutas[i][0]:20} {rutas[i][1]:20} {rutas[i][2]:11d} {rutas[i][3]:15d} {str(rutas[i][4]):20}")

# Llamas a las funciones anteriores
print("\nRutas demandadas de exportación\n")
mostrar_rutas(rutas_exportacion_importacion("Exports"))

print("\nRutas demandadas de importación\n")
mostrar_rutas(rutas_exportacion_importacion("Imports"))

# =============================================================================
# Opción 2) Medio de transporte utilizado. ¿Cuáles son los 3 medios de transporte 
# más importantes para Synergy logistics considerando el valor de las 
# importaciones y exportaciones? ¿Cuál es medio de transporte que podrían 
# reducir? 
# =============================================================================

# Funcion para opcion 2
def medios_transporte (direccion):
    contador = 0     # Cantidad de registros
    totales = 0     # Cantidad de valores totales de las exp e imp.
    medios_transporte = []   # Medio de transporte
    transportes = []    # Medio de transporte, contador y totales

    for medio in sinergy_database:
        # Si es igual la direccion, se obtiene un medio de transporte a buscar.
        if medio["direction"] == direccion:
            medio_actual = medio["transport_mode"]
            # Si no esta el transporte en la lista, realiza operaciones
            if medio_actual not in medios_transporte:
                for transporte in sinergy_database:
                    # Si es igual con el medio de transporte a buscar, incrementa contador y totales
                    if medio_actual == transporte["transport_mode"] and transporte["direction"] == direccion and int(transporte["total_value"]) != 0:
                        contador += 1
                        totales += int(transporte["total_value"])

                # Se agrega un nuevo elemento a la listas correspondientes, y se reinician variables de calculos
                medios_transporte.append(medio_actual)
                transportes.append([medio["transport_mode"], contador, totales])
                contador = 0
                totales = 0

    # Ordena la lista de forma descendente
    transportes.sort(reverse = True, key = lambda x:x[2])
    
    # Imprime resultados de forma tabular de los 3 medios de transporte mas importantes
    print(f"{'Transporte':10} {'Operaciones':11} {'Valores totales':15}\n")
    for i in range(0, 3):
        print(f"{transportes[i][0]:10} {transportes[i][1]:11d} {transportes[i][2]:15d}")
        
# Llamada a funciones
print("\nPrincipales medios de transporte en exportaciones\n")
medios_transporte("Exports")
print("\nPrincipales medios de transporte en importaciones\n")
medios_transporte("Imports")

# =============================================================================
# Opción 3) Valor total de importaciones y exportaciones. Si Synergy Logistics 
# quisiera enfocarse en los países que le generan el 80% del valor de las 
# exportaciones e importaciones ¿en qué grupo de países debería enfocar sus 
# esfuerzos?
# =============================================================================

# Funcion para opcion 3
# Funcion obtiene los valores totales de cada pais segun sea exportancion o importacion
def valores_exp_imp(direccion):
    paises_revisados = []   # Origen
    valores_paises = []     # Origen, valor, operaciones
    
    for ruta in sinergy_database:
        # Si coincide la direccion, obtiene un pais e inicializa variables de calculo
        if direccion == ruta["direction"]:
            actual = ruta["origin"]
            valor = 0
            operaciones = 0
            
            # Si el pais no ha sido buscado, realiza procesos.
            if actual not in paises_revisados:
                for rutas in sinergy_database:
                    # Si coincide pais, direccion, incrementas variables
                    if actual == rutas["origin"] and direccion == rutas["direction"] and int(rutas["total_value"]) != 0:
                        valor += int(rutas["total_value"])
                        operaciones += 1
                        
                # Se agrega el elemento a las listas correspodientes.
                paises_revisados.append(actual)
                valores_paises.append([actual, valor, operaciones])
    
    #Ordenamiento descendente 
    valores_paises.sort(reverse=True, key=lambda x:x[1])
    return valores_paises


# Funcion para obtener porcentajes de cada pais conforme a exportaciones o importaciones
def porcentajes(paises, porcentaje = 0.8):
    valor_total = 0     # Total de exp o imp.
    porcentajes = 0     # Suma de porcentajes
    top_paises = []     # Pais, valor, operaciones, porcentaje segun la cantidad de exp o imp.
    
    # Obtenemos el total del valor de las exp o imp.
    for pais in paises:
        valor_total += pais[1]
    
    # Obtenemos % de cada pais segun del valor total de exp o imp
    for pais in paises:
        porcentaje_actual = round(pais[1]/valor_total, 3)
        porcentajes += porcentaje_actual
        
        # Si no es >= 80, agrega el pais a una lista, sino detiene el ciclo
        if porcentajes <= porcentaje:
            top_paises.append([pais[0], pais[1], pais[2], porcentaje_actual])
        else:
            break
    
    return top_paises

# Funcion imprime de forma tabular los resultados para la opcion 3
def mostrar_porcentajes(paises):
    print(f"{'País':20} {'Valores totales':15} {'Operaciones':11} {'Porcentaje':10}\n")
    for pais in paises:
        print(f"{pais[0]:20} {pais[1]:15d} {pais[2]:11d} {pais[3]:10f}")


print("\nPrincipales países con mayor exportación\n")
mostrar_porcentajes(porcentajes(valores_exp_imp("Exports")))
print("\nPrincipales países con mayor importación\n")
mostrar_porcentajes(porcentajes(valores_exp_imp("Imports")))