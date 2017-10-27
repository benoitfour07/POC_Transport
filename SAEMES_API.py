#Libraries
import requests
import json
from io import StringIO
import sqlite3
import numpy as np
import csv
import pandas as pd


#Proxy parameters
proxies = {
  "http":"http://four:a27JG7WX@proxyban:8080/",
  "https":"https://four:a27JG7WX@proxyban:8080/",
}


#Load Data
q1 = requests.get('https://opendata.saemes.fr/api/records/1.0/search/?dataset=places-disponibles-parkings-saemes&rows=200&sort=nom_parking&facet=date&facet=nom_parking&facet=type_de_parc&facet=horaires_d_acces_au_public_pour_les_usagers_non_abonnes&facet=countertype&facet=counterfreeplaces') #,proxies=proxies)
print(q1)
data=q1.json()


# Function that mines information for one car park (finally not necessary)
def mine_car_park_disponibility_information(n):
	T=[]
	try:
		T.append(data['records'][n]["fields"]["nom_parking"])
	except KeyError:	
		T.append("")
	try:	
		T.append(data['records'][n]["fields"]["pmo_number"])
	except KeyError:	
		T.append("")
	try:
		T.append(data['records'][n]["fields"]["date"])	
	except KeyError:	
		T.append("")
	try:
		T.append(data['records'][n]["fields"]["counterfreeplaces"])
	except KeyError:	
		T.append("")
	return T

	
#Function that list information for all car park (finally not necessary: linked to mine_parking_disponibility_information)
def mine_entire_car_park_information():
	P=[]
	nbre_parking=int(data["nhits"])
	for i in range(nbre_parking):
		P.append(mine_car_park_disponibility_information(i))
	return P


#Write into csv
c = csv.writer(open("MONFICHIER.csv", "w"))
	
	
#Mine car park names
def mine_car_park_information(attribute):
	T=[]
	nbre_parking=int(data["nhits"])
	for i in range(nbre_parking):
		try:
			T.append(data['records'][i]["fields"][attribute])
		except KeyError:	
			T.append("")
	return T

#Build Panda Data Frame
def panda_car_park_data_frame():
	a1=mine_car_park_information("nom_parking")
	a2=mine_car_park_information("pmo_number")
	a3=mine_car_park_information("date")
	a4=mine_car_park_information("counterfreeplaces")
	raw_data={"nom_parking":a1,"pmo_number":a2,"date":a3,"counterfreeplaces":a4}
	df = pd.DataFrame(raw_data, columns = ['nom_parking', 'pmo_number', 'date','counterfreeplaces'])
	return df

#Export pd to csv
datam=panda_car_park_data_frame()
print(datam)
datam.to_csv('example3.csv',sep=';')


# Get global car park information
q2 = requests.get('https://opendata.saemes.fr/api/records/1.0/search/?dataset=referentiel-parkings-saemes&rows=100&sort=code_postal&facet=type_de_parc&facet=code_postal&facet=ville&facet=nombre_de_places&facet=hauteur_maximum&facet=erp_etablissements_recevant_du_public&facet=acces_motos&facet=acces_velos&facet=accessibilite_pmr&facet=liber_t&facet=carte_total_gr&facet=reservation_de_place_sur_internet&facet=autolib&facet=autopartage&facet=bornes_de_recharge_vehicule_electrique&facet=consigne_a_casques_gratuite&facet=lavage_voitures_et_ou_motos&facet=horaire_vl_15mn_15_min&facet=horaire_vl_3h00_3_hr&facet=horaire_moto_15mn_15_min') #,proxies=proxies)
print(q2)
data=q2.json()

def mine_global_car_park_information(n):
	T=[]
	try:
		T.append(data['records'][n]["fields"]["nom_parking"])
	except KeyError:	
		T.append("")
	try:	
		T.append(data['records'][n]["fields"]["nombre_de_places"])
	except KeyError:	
		T.append("")
	return T	

		












































