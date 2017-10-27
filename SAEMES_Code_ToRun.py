#Libraries
import requests
import json
import sqlite3
import numpy as np
import pandas as pd

#Proxy parameters
proxies = {
  "http":"http://four:a27JG7WX@proxyban:8080/",
  "https":"https://four:a27JG7WX@proxyban:8080/",
}

#Load Data
q1 = requests.get('https://opendata.saemes.fr/api/records/1.0/search/?dataset=places-disponibles-parkings-saemes&rows=200&sort=nom_parking&facet=date&facet=nom_parking&facet=type_de_parc&facet=horaires_d_acces_au_public_pour_les_usagers_non_abonnes&facet=countertype&facet=counterfreeplaces') #,proxies=proxies)
print(q1)
data=q1.json()#Mine car park names
def mine_car_park_information(attribute):
	T=[]
	nbre_parking=int(data["nhits"])
	for i in range(nbre_parking):
		try:
			T.append(data['records'][i]["fields"][attribute])
		except KeyError:	
			T.append("")
	return T

def mine_car_park_information2(attribute1,attribute2):
	T=[]
	nbre_parking=int(data["nhits"])
	for i in range(nbre_parking):
		try:
			T.append(data['records'][i]["fields"][attribute1] + '_' + data['records'][i]["fields"][attribute2])
		except KeyError:	
			T.append("")
	return T
 
#Build Panda Data Frame
def panda_car_park_data_frame():
	a1=mine_car_park_information("nom_parking")
	a2=mine_car_park_information2("pmo_number","countertype")
	a3=mine_car_park_information("pmo_number")
	a4=mine_car_park_information("countertype")
	a5=mine_car_park_information("date")
	a6=mine_car_park_information("counterfreeplaces")
	raw_data={"nom_parking":a1,"pmo_number_countertype":a2,"pmo_number":a3,"countertype":a4,"date":a5,"counterfreeplaces":a6}
	df = pd.DataFrame(raw_data, columns = ['nom_parking','pmo_number_countertype', 'pmo_number','countertype', 'date','counterfreeplaces'])
	return df

#Export pd to csv
datam=panda_car_park_data_frame()
#print(datam)
#mode='a to add the result following the last saved result
datam.to_csv('SAEMES_Places_Disponibles_Parking.csv',sep=';',mode='a',header=False,index=False)