import requests
import pandas as pd

api = "https://fr.distance24.org/route.json?stops={}|{}"

cities = ['Paris',
	'Marseille',
	'Lyon',
	'Toulouse',
	'Nice',
	'Nantes',
	'Strasbourg',
	'Montpellier',
	'Bordeaux',
	'Lille',
	'Rennes',
	'Reims',
	'Le Havre',
	'Saint-Étienne',
	'Toulon',
	'Grenoble',
	'Dijon',
	'Nîmes',
	'Angers',
	'Villeurbanne',
	'Le Mans',
	'Saint-Denis',
	'Aix-en-Provence',
	'Clermont-Ferrand',
	'Brest',
	'Limoges',
	'Tours',
	'Amiens',
	'Perpignan',
	'Metz',
	'Besançon',
	'Boulogne-Billancourt',
	'Orléans',
	'Mulhouse',
	'Rouen',
	'Saint-Denis',
	'Caen',
	'Argenteuil',
	'Saint-Paul',
	'Montreuil',
	'Nancy',
	'Roubaix',
	'Tourcoing',
	'Nanterre',
	'Avignon',
	'Vitry-sur-Seine',
	'Créteil',
	'Dunkerque',
	'Poitiers',
	'Asnières-sur-Seine']



def distance(start_city, stop_city):
	r = requests.get(api.format(start_city, stop_city))
	data = r.json()
	distance = data['distance']
	#print("Distance de %s à %s est %s" %(start_city.upper(), stop_city.upper(), distance))
	return distance

if __name__ == "__main__":
    for city_start in cities:
    	line = ""
    	for city_stop in cities:
    		print("{} -> {} : {}".format(city_start.upper(), city_stop.upper(), distance(city_start, city_stop)))