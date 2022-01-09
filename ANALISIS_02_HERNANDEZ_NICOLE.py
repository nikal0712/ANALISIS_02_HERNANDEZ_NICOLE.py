#Programa para Synergy Logistics
#Análisis de 3 estrategias posibles para mejorar las operaciones:
    #1. RUTAS DE IMPORTACIÓN Y EXPORTACIÓN: enfocar esfuerzos en las 10 rutas más demandadas (para imp y exp)
    #2. MEDIO DE TRANSPORTE UTILIZADO: enfocarse en los 3 medios de transporte más importantes considerando el valor de las imps y exps.
    #3. VALOR TOTAL DE IMPS Y EXPS: enfocarse en los países que le generan el 80% del valor de las exps e imps.
#Justificar recomendación de enfoque en reporte respaldado por datos y análisis en una extensión máxima de 1.5 cuartillas
#ENTREGABLES:
    #1. Reporte: de max. 1.5 cuartillas señalando recomendación de enfoque/estrategia. Reporte se carga a plataforma. 
        #REPORTE_02_HERNANDEZ_NICOLE.pdf
    #2. Archivo en Python: con código implementado para análisis cargado al repositorio de Github.
        #ANALISIS_02_HERNANDEZ_NICOLE.py

import csv

imp_count = 0 #Número de importaciones
exp_count = 0 #Número de importaciones
origins = [] #Lista de países de origen
origins_as_dict = []
destinations = [] #Lista de países de destino
countries = [] #Lista de todos los países
countries_as_dict = []
paths = [] #Lista de rutas
paths_as_dict = [] 
transport_modes = [] #Lista de modos de transporte
transport_modes_as_dict = []
global_value = 0 #Suma de ganancias totales

with open("synergy_logistics_database.csv", "r") as csv_database:
    data_as_dict = csv.DictReader(csv_database)
    
    for line in data_as_dict:
        #Conteo de número de importaciones
        if line["direction"] == "Imports":
            imp_count += 1
        #Conteo de número de importaciones
        if line["direction"] == "Exports":
            exp_count += 1
        
        #Suma de ganancias totales
        global_value += int(line["total_value"])
        #Listas de países de origen y destino de cada operación
        origins.append(line["origin"])
        destinations.append(line["destination"])
        #Listas de países de origen y destino sin repetición a través de un conjunto
        origins_reduced = set(origins)
        destinations_reduced = set(destinations)
        countries = list(origins_reduced) + list(destinations_reduced) 
        countries_reduced = set(countries)
        #Lista de la ruta de cada operación
        paths.append((line["origin"], line["destination"]))
        #Lista de rutas sin repetición
        paths_reduced = set(paths)
        #Lista de los modos de transporte de cada ruta
        transport_modes.append(line["transport_mode"])
        #Lista de los modos de transporte sin repetición
        transport_modes_reduced = set(transport_modes)

#LLENADO DE LISTA DE DICCIONARIOS DE LOS MODOS DE TRANSPORTE
for transport_mode in transport_modes_reduced:
        transport_modes_as_dict.append({"transport_mode": transport_mode, "count": 0, "value": 0})
            
with open("synergy_logistics_database.csv", "r") as csv_database:
    data_as_dict = csv.DictReader(csv_database)
    
    for line in data_as_dict: 
        for transport_mode in transport_modes_as_dict:
            if transport_mode["transport_mode"] == line["transport_mode"]:
                transport_mode["count"] += 1
                transport_mode["value"] += int(line["total_value"])

for transport_mode in transport_modes_as_dict:
    transport_mode["percentage"] = transport_mode["value"]*100/global_value
    
sorted_transport_modes = sorted(transport_modes_as_dict, key = lambda i: i['percentage'], reverse=True)

#LLENADO DE LISTA DE DICCIONARIOS DE LAS RUTAS
for path in paths_reduced:
    paths_as_dict.append({"origin": path[0], "destination": path[1], "count": 0, "value": 0, "percentage": 0})

with open("synergy_logistics_database.csv", "r") as csv_database:
    data_as_dict = csv.DictReader(csv_database)
    
    for line in data_as_dict: 
        for path in paths_as_dict:
            if path["origin"]==line["origin"] and path["destination"]==line["destination"]:
                path["count"] += 1
                path["value"] += int(line["total_value"])

for path in paths_as_dict:
    path["percentage"] = path["value"]*100/global_value

sorted_paths = sorted(paths_as_dict, key = lambda i: i['count'], reverse=True)

#LLENADO DE LISTA DE DICCIONARIOS DE TODOS LOS PAÍSES
for country in countries_reduced:
        countries_as_dict.append({"country": country, "value": 0, "percentage": 0})
            
with open("synergy_logistics_database.csv", "r") as csv_database:
    data_as_dict = csv.DictReader(csv_database)
    
    for line in data_as_dict: 
        for country in countries_as_dict:
            if country["country"] == line["origin"] or country["country"] == line["destination"]:
                country["value"] += (int(line["total_value"])/2)

for country in countries_as_dict:
    country["percentage"] = country["value"]*100/global_value
    
sorted_countries = sorted(countries_as_dict, key = lambda i: i['percentage'], reverse=True)


#IMPRESIONES
print("ENFOQUES DE ESTRATEGIA")

count = 0
print("\n1. Enfoque en las principales rutas:")
print("Total de rutas:", len(sorted_paths))
print("Listado de rutas y el número de veces que se utilizaron.")
for path in sorted_paths:
    count+=1
    if count <= 10:
        print(count, ".", path["origin"], "a", path["destination"], ":", path["count"], "veces")
    else:
        break

count = 0
print("\n2. Enfoque en los medios de transporte que más generaron valor.")
for transport_mode in sorted_transport_modes:
    count+=1
    if count <= 10:
        print(count, ".", transport_mode["transport_mode"], ":", round(transport_mode["percentage"], 2), "%")
    else:
        break
    
count = 0
i = 0
print("\n3. Enfoque en los países que proporcionen el 80% del valor.")
print("Número total de países: ", len(sorted_countries))
for country in sorted_countries:
    i += 1
    if count <= 80:
        count += country["percentage"]
        print(i, ".", country["country"], ":", round(country["percentage"], 2), "%")
    else:
        break
