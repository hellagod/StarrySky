import sys
import ephem

from __init__ import ephem_planets_list
from scripts.name_translator import name_translator


class Planet:
    def __init__(self, obj: dict):
        self.name = obj.get('name')
        self.englishName = obj.get('englishName')
        self.id = obj.get('id')
        self.position = obj.get('position')
        self.img_high_res = f'{sys.path[0]}/planet_textures/{self.id}.jpeg'
        self.img_small_res = f'{sys.path[0]}/planet_textures_smaller/{self.id}.jpeg'
        self.number_of_moons = len(obj.get('moons')) if obj.get('moons') is not None else 0
        #self.moons = obj.get('moons')
        self.gravity = obj.get('gravity')
        self.temperature = round(int(obj.get('avgTemp')) - 273.15, 2)
        self.radius = obj.get('meanRadius')
        self.mass = obj.get('mass').get('massValue') * pow(10, obj.get('mass').get('massExponent'))
        self.volume = obj.get('vol').get('volValue') * pow(10, obj.get('vol').get('volExponent'))
        self.escape_velocity = obj.get('escape')

    def get_dynamic_data(self):
        if self.englishName == "Earth":
            return earth_data()
        else:
            return get_sun_distance(self.position)


class Moon:
    def __init__(self, obj: dict):
        self.name = name_translator(obj.get('name'))
        self.id = obj.get('id')
        self.radius = obj.get('meanRadius')
        self.discovery_date = obj.get('discoveryDate')
        self.discovered_by = obj.get('discoveredBy')
        self.gravity = obj.get('gravity')


def get_sun_distance(position):
    ephem_planet = ephem_planets_list[position - 1]
    ephem_planet.compute()
    return ephem_planet.earth_distance


def earth_data():
    return None
