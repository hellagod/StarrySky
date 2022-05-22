import requests
import operator
from Planet import Planet
from scripts.name_translator import name_translator


def get_moons():
    res_moons = requests.get('https://api.le-systeme-solaire.net/rest.php/bodies?filter%5B%5D=isPlanet%2Ceq%2Cfalse')
    res_moons = res_moons.json()
    moons_list = res_moons.get("bodies")
    return moons_list


def get_planets():
    res_planets = requests.get('https://api.le-systeme-solaire.net/rest.php/bodies?filter%5B%5D=isPlanet%2Ceq%2Ctrue')
    res_planets = res_planets.json()
    planets_list = res_planets.get("bodies")
    for planet in planets_list:
        planet['name'] = name_translator(planet.get('name'))
    return order_planets(planets_list)


def order_planets(planets_list):
    planets_order_dict = {'Меркурий': 1, 'Венера': 2, 'Земля': 3, 'Марс': 4, 'Юпитер': 5,
                          'Сатурн': 6, 'Уран': 7, 'Нептун': 8}
    for planet in planets_list:
        dict_name = planet.get("name")
        planet["position"] = planets_order_dict[f'{dict_name}']
    planets_list.sort(key=operator.itemgetter('position'))
    return planets_list


def planet_list_generator():
    planets_list = get_planets()
    planets_obj_list = []
    for i in range(len(planets_list)):
        planets_obj_list.append(Planet(planets_list[i]))
    return planets_obj_list
