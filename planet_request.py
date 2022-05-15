import requests
import json
import operator
from googletrans import Translator, constants

res_moons = requests.get('https://api.le-systeme-solaire.net/rest.php/bodies?filter%5B%5D=isPlanet%2Ceq%2Cfalse')
res_moons = res_moons.json()
moons_list = res_moons.get("bodies")
print(moons_list)

res_planets = requests.get('https://api.le-systeme-solaire.net/rest.php/bodies?filter%5B%5D=isPlanet%2Ceq%2Ctrue')
res_planets = res_planets.json()

planets_list = res_planets.get("bodies")
planets_list.sort(key=operator.itemgetter('name'))
id_list = []
print(planets_list)

for el in planets_list:
    id_list.append(el.get("id"))

translator = Translator()
print(planets_list)
for planet in planets_list:
    planet["name"] = translator.translate(planet["name"], dest="ru").text
print(planets_list)

for planet in planets_list:
    print(planet["id"])
    print(planet.get('mass'))
    print(planet.get('mass').get('massValue')*pow(10, planet.get('mass').get('massExponent')))
    print(planet.get('vol').get('volValue') * pow(10, planet.get('vol').get('volExponent')))
    print(round(int(planet.get('avgTemp')) - 273.15, 2))


# planets = res["bodies"]
# print(planets)


# список спутников --> discoveredBy; discoveryDate
# avgTemp
# gravity
# polar radius
# equatorial radius
# escape velocity
