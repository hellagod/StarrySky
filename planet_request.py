import requests
import json
import operator
from googletrans import Translator, constants

from Planet import Planet


def get_moons():
    res_moons = requests.get('https://api.le-systeme-solaire.net/rest.php/bodies?filter%5B%5D=isPlanet%2Ceq%2Cfalse')
    res_moons = res_moons.json()
    moons_list = res_moons.get("bodies")
    return moons_list


def get_planets():
    res_planets = requests.get('https://api.le-systeme-solaire.net/rest.php/bodies?filter%5B%5D=isPlanet%2Ceq%2Ctrue')
    res_planets = res_planets.json()

    planets_list = res_planets.get("bodies")
    planets_list.sort(key=operator.itemgetter('name'))

    return planets_list

moons_list = get_moons()
planets_list = get_planets()

print(moons_list)
for moon in moons_list:
    print(moon["dimension"])


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

for planet in planets_list:
    print(planet.get('name'))
    moons = planet.get('moons')
    if moons is not None:
        print(len(planet.get('moons')))
    else:
        print(0)

for planet in planets_list:
    print(len(planet.get('moons')) if planet.get('moons') is not None else 0)


print(planets_list)




def planet_list_generator():
    planets_list = get_planets()
    planets_obj_list = []
    for i in range(len(planets_list)):
        planets_obj_list.append(Planet(planets_list[i]))
        print(planets_list)
    return planets_obj_list

print(planet_list_generator())