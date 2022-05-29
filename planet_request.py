import requests
import operator
from Planet import Planet
from scripts.name_translator import name_translator


def get_moons():
    res_moons = requests.get('https://api.le-systeme-solaire.net/rest.php/bodies?filter%5B%5D=isPlanet%2Ceq%2Cfalse')
    res_moons = res_moons.json()
    moons_list = res_moons.get("bodies")
    for moon in moons_list:
        moon['name'] = name_translator(moon.get('name'))
    return order_planets(moons_list)


def get_planets():
    res_planets = requests.get('https://api.le-systeme-solaire.net/rest.php/bodies?filter%5B%5D=isPlanet%2Ceq%2Ctrue')
    res_planets = res_planets.json()
    planets_list = res_planets.get("bodies")
    for planet in planets_list:
        planet['name'] = name_translator(planet.get('name'))
    return order_planets(planets_list)


def get_bodies():
    res_bodies = requests.get('https://api.le-systeme-solaire.net/rest.php/bodies')
    res_bodies = res_bodies.json().get("bodies")
    planet_list = []
    for body in res_bodies:
        if body["englishName"] == 'Moon':
            moon = body
        if body["englishName"] == 'Sun':
            sun = body
        if body["isPlanet"]:
            planet_list.append(body)
    for planet in planet_list:
        planet['name'] = name_translator(planet.get('name'))
    planet_list = order_planets(planet_list)
    sun['name'] = name_translator(sun.get('name'))
    moon['name'] = name_translator(moon.get('name'))
    sun['avgTemp'] = 5780
    moon['avgTemp'] = 220
    planet_list.insert(0, sun)
    planet_list.insert(4, moon)
    return planet_list


def order_planets(planets_list):
    planets_order_dict = {'Меркурий': 1, 'Венера': 2, 'Земля': 3, 'Марс': 4, 'Юпитер': 5,
                          'Сатурн': 6, 'Уран': 7, 'Нептун': 8}
    for planet in planets_list:
        dict_name = planet.get("name")
        planet["position"] = planets_order_dict[f'{dict_name}']
    planets_list.sort(key=operator.itemgetter('position'))
    return planets_list


def planet_list_generator():
    planets_list = get_bodies()
    planets_obj_list = []
    for i in range(len(planets_list)):
        planets_obj_list.append(Planet(planets_list[i]))
    return planets_obj_list
