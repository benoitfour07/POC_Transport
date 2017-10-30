# -*- coding: utf-8 -*-
"""
Created on Mon Oct 23 12:54:59 2017

@author: psaffers
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
from datetime import date

#Définition des constantes de date
today = date.today()
tomor = date.today()+datetime.timedelta(1)
j_j   = str(today.year)+"-"+str(today.month)+"-"+str(today.day)
j_p_1 = str(tomor.year)+"-"+str(tomor.month)+"-"+str(tomor.day)

#On récupère la structure de la page
page = requests.get("https://www.blablacar.fr", headers={'User-Agent': 'Mozilla/5.0'})
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


###
#On parcourt alors chacun des tops trajets définis
###
page_temp = requests.get("https://www.blablacar.fr"+trajets_table['url'][0], 
                          headers={'User-Agent': 'Mozilla/5.0'})
#Initialisation des variables
if trajets_table['start'][0]=='Paris':
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
        page_temp = requests.get("https://www.blablacar.fr"+url_temp, 
                                  headers={'User-Agent': 'Mozilla/5.0'})
    soup_temp = BeautifulSoup(page_temp.content, 'html.parser')
    dep_arr_t = soup_temp.findAll("dd")
    date_dep_ = soup_temp.findAll("h3", attrs={'class':'time u-darkGray'})
    for k in range(0,len(dep_arr_t)):
        bal_temp = soup_temp.findAll("dd")[k]
        if bal_temp.get("title")=='Départ':
            start_temp.append(bal_temp.getText().replace('\n','').strip())
        if bal_temp.get('title')=='Arrivée':
            end_temp.append(bal_temp.getText().replace('\n','').strip())
        if k%2==0:
            date_temp.append(date_dep_[int(k/2)].get("content"))
            print(date_dep_[int(k/2)].get("content"))
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
                url_temp = p_oth[l].get('href')
        except:
            continue
    round=round+1
    
print(start_temp)

page_tst = requests.get("https://www.blablacar.fr/#?fn=Paris&fc=48.856614%7C2.3522219&fcc=FR&fp=0&tn=Lyon&tc=45.764043%7C4.835659&tcc=FR&tp=0&sort=trip_date&order=asc&radius=40.149&limit=10&page=1", 
                                  headers={'User-Agent': 'Mozilla/5.0'})
page_tst.content