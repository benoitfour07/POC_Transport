# -*- coding: utf-8 -*-
"""
Created on Mon Nov  6 13:40:24 2017

@author: psaffers
"""
#Import des librairies
import os
import sys
sys.path.append("c:/users/psaffers/appdata/local/programs/python/python35/lib/site-packages")
import pandas as pd
import requests
from datetime import date
from requests.auth import HTTPDigestAuth
from selenium import webdriver

#Définition des constantes de date
today = date.today()
j_j   = str(today.year)+'0'*(1-len(str(today.month)))+str(today.month)+'0'*(2-len(str(today.day)))+str(today.day)

#Définition des constantes
park_rep   = 'C:/Users/psaffers/Documents/POC/Parking/Data/Patrimoine'
chemin_exe = 'C:/Program Files (x86)/Google/Chrome/chromedriver'
output_rep = 'C:/Users/psaffers/Documents/POC/Parking/Data/Meteo'

#Définition des fonctions
def import_fich(directory): #Importe le dernier fichier par ordre alphabétique d'un répertoire
    liste_fich = sorted(os.listdir(directory))
    fich       = liste_fich[len(liste_fich)-1]
    table      = pd.read_csv(directory+'/'+fich, sep = ';', encoding = 'utf-8',
                             header = 0)
    return(table)

def arrondi_dec(table,var): #Renvoie un couple d'arrondi à 10-1 près pour au plus 1 variable d'une table
    table[var] = [round(valeur,1) for valeur in table[var]]
    return(table[var])

def authentification(login,password):
    data = requests.post("https://energylab.sia-partners.com/sialab/api/v1/auth?login=" + login + "&password=" + password, verify=False)
    return data.json()['token']

def get_meteo(lat,lng,var,token):
    return(requests.get('https://energylab.sia-partners.com/sialab/api/v1/meteo_etalab/point/'+str(lat)+'/'+str(lng)+'/'+var+'/'+j_j+'000000?token='+token,
                        verify=False).json())
###
#On importe le dernier fichier de covoiturage pour répérer les latitudes et longitudes
#sur lesquelles requêter
###
table_par = import_fich(park_rep)
table_par['lat'] = arrondi_dec(table_par,'lat')
table_par['lng'] = arrondi_dec(table_par,'lng')
list_lat_lng     = table_par[['lat','lng']].drop_duplicates().reset_index().dropna()[['lat','lng']]

###
#Pour la liste de couples latitude, longitude récupérés, on récupère les prévisions météorologiques
###

#Etape 1 : authentification, on récupère le token
token = authentification('USER_POC_WEATHER','pocweather2017')

#Etape 2 : on boucle sur les latitudes, longitudes et on stocke les températures, sur une table
#          au format lat|lng|horodate|tempe_2|humid_2|preci_0|cloud_0
to_export = pd.DataFrame()
for i in range(0,len(list_lat_lng)):
    lat   = list_lat_lng['lat'][i]
    lng   = list_lat_lng['lng'][i]
    gen = pd.DataFrame() 
    for type_var in ['tempe_2','humid_2','preci_0','cloud_0']:             
        var  = []
        date = []
        lati = []
        long = []
        content = get_meteo(lat,lng,'tempe_2',token)
        for k in range(0,24):
            print(content['data']['valeur'][k])
            var.append(content['data']['valeur'][k])
            if type_var == 'tempe_2':
                date.append(content['data']['date_valid'][k])
                lati.append(lat)
                long.append(lng)
        if type_var == 'tempe_2':
            gen = pd.concat([gen,pd.DataFrame({'lat':lati,'lng':long,'horodate':date,
                                               type_var:var})])
        else:
            gen = pd.concat([gen,pd.DataFrame({type_var:var})],axis=1)
    to_export = pd.concat([to_export,gen],axis=0)
    
to_export.reset_index().to_csv(output_rep+'/meteo_'+j_j+'.csv')