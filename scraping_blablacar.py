# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 12:54:59 2017

@author: psaffers
"""
import sys
sys.path.append("c:/users/psaffers/appdata/local/programs/python/python35/lib/site-packages")
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from datetime import date
from selenium import webdriver
import time
import googlemaps

#Définition des constantes de date
today = date.today()
tomor = date.today()+datetime.timedelta(1)
j_j   = str(today.year)+"-"+'0'*(1-len(str(today.month)))+str(today.month)+"-"+'0'*(2-len(str(today.day)))+str(today.day)
j_p_1 = str(tomor.year)+"-"+'0'*(1-len(str(tomor.month)))+str(tomor.month)+"-"+'0'*(2-len(str(tomor.day)))+str(tomor.day)
j_j_txt   = j_j.replace("-","")
j_p_1_txt = j_p_1.replace("-","")
#Définition des répertoires
output_rep = 'C:/Users/psaffers/Documents/POC/Parking/Data/Covoiturage'
chemin_exe = 'C:/Program Files (x86)/Google/Chrome/chromedriver'
#On ouvre une session requests
session = requests.Session()

#On récupère la structure de la page
page = session.get("https://www.blablacar.fr", headers={'User-Agent': 'Mozilla/5.0'})
page.status_code
print(page.content)

soup = BeautifulSoup(page.content, 'html.parser')
html = list(soup.children)[2]
body = list(html.children)[3]
div_ = list(body.children)[3]
main = list(div_.children)[9]
div1 = list(main.children)[3]
div2 = list(div1.children)[1]
arti = list(div2.children)[3]
div3 = list(arti.children)[1]
div4 = list(div3.children)[3]

###
#On crée une table contenant : le lien et le trajet pour les trajets
#ne concernant que Paris (lieu d'arrivée ou de départ)
###

#Traitement de la ligne des trois principaux#
principaux = list(div4.children)[3].findAll('a')
dep = []
arr = []
http = []
for i in [0,1,2]:
    http.append(principaux[i].get("href"))
    dep.append((list(principaux[i].children))[1].getText())
    arr.append((list(principaux[i].children))[3].getText())

#Traitement du reste du tableau
secondaire = list(div4.children)[5].findAll('a')
for j in range(0,len(secondaire)):
    http.append(secondaire[j].get("href"))
    dep.append((list(secondaire[j].children))[1].getText().split(' - ')[0])
    try:
        arr.append((list(secondaire[j].children))[1].getText().split(' - ')[1])
    except:
        arr.append("")
        
trajets_table = pd.DataFrame({'url':http,'start':dep,'end':arr})
trajets_table = trajets_table[(trajets_table['end']=='Paris')|(trajets_table['start']=='Paris')].reset_index()[['start','end','url']]

#On définit le webdriver
options = webdriver.ChromeOptions()
#options.add_argument('headless')
#options.add_argument('--log-level=3')
driver = webdriver.Chrome(chemin_exe)
#On définit notre future table d'étude
covoit = pd.DataFrame(columns=['date','type','place'])
#On itère sur les différentes URL trouvées
for i in range(0,len(trajets_table['url'])):
    #On récupère le code source de la page principale
    driver.get("https://www.blablacar.fr"+trajets_table['url'][i])
    #Initialisation des variables
    if trajets_table['start'][i]=='Paris':
        type= 'start'
    else:
        type= 'end'
    round     = 0
    stop_crit = 0
    start_temp=[]
    end_temp  =[]
    date_temp =[]
    type_temp =[]
    
    while stop_crit!=1:
        print(round)
        if round!=0:
            driver.get("https://www.blablacar.fr"+url_temp)
            time.sleep(5)
            #try:
             #   element = WebDriverWait(driver, 10).until(
              #          EC.presence_of_element_located((By.ID, "search-results"))
               #         )
            #except TimeoutException:
             #   print('Page not reachable')
        soup_temp = BeautifulSoup(driver.page_source, 'html.parser')
        dep_arr_t = soup_temp.findAll("dd")
        date_dep_ = soup_temp.findAll("h3", attrs={'class':'time u-darkGray'})
        for k in range(0,len(dep_arr_t)):
            bal_temp = soup_temp.findAll("dd")[k]
            if bal_temp.get("oldtitle")=='Départ':
                start_temp.append(bal_temp.getText().replace('\n','').strip())
            if bal_temp.get('oldtitle')=='Arrivée':
                end_temp.append(bal_temp.getText().replace('\n','').strip())
            if k%2==0:
                date_temp.append(date_dep_[int(k/2)].get("content"))
                if ((date_dep_[int(k/2)].get("content")!=j_p_1)&(date_dep_[int(k/2)].get("content")!=j_j)):
                    stop_crit=1
                type_temp.append(type)
        #On récupère le lien de la page suivante
        #1 - On repère le lien de la page active
        p_act = int(soup_temp.findAll("li",attrs={'class':'active'})[0].getText())
        #2 - On récupère l'ensemble des liens de pagination avec la valeur de page associée
        p_oth = soup_temp.findAll("a",attrs={'class':'js-trip-search-pagination'})
        for l in range(0,len(p_oth)):
            try:
                if int(p_oth[l].getText())==p_act+1:
                    url_temp = p_oth[l].get('href').replace('limit=10','limit=100')
            except:
                continue
        round=round+1
    
    if type=='start':
        covoit_temp = pd.DataFrame({'date':date_temp,'type':type_temp,'place':start_temp})[['date','type','place']]
    elif type=='end':
        covoit_temp = pd.DataFrame({'date':date_temp,'type':type_temp,'place':end_temp})[['date','type','place']]
    
    covoit = pd.concat([covoit,covoit_temp])

driver.quit()
del type
#Dédoublonnage et filtre sur la table 'covoit'
covoit_v1 = covoit.drop_duplicates()[(covoit.drop_duplicates()['date']==j_j)|(covoit.drop_duplicates()['date']==j_p_1)].reset_index()[['date','type','place']]

#On recherche les coordonnées GPS des départs et arrivés
gmaps = googlemaps.Client(key='AIzaSyBhDB0PdRyo2dVpbZxvB5c9n5egLmlkJ1Y')
#On géocode les lieux trouvés
covoit_v1['lat']=['' for place in covoit_v1['place']]
covoit_v1['lng']=covoit_v1['lat']
for l in range(0,len(covoit_v1['place'])):
    try:
        geocode_result      = gmaps.geocode(covoit_v1['place'][l]).pop()
        covoit_v1['lat'][l] = geocode_result['geometry']['location']['lat']
        print(geocode_result['geometry']['location']['lat'])
        covoit_v1['lng'][l] = geocode_result['geometry']['location']['lng']
        time.sleep(0.05)
    except:
        next

covoit_v1.to_csv(output_rep+'/covoit_'+j_j_txt+'.csv')