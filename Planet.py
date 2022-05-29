"""
Planet.py file contains custom astronomic bodies classes that help
to store and fetch data acquired from the database
"""

import sys
from __init__ import ephem_bodies_list, wiki_queries_dict

"""
CelestialBody is the parent class for all celestial bodies to store info acquired from the database
"""


class CelestialBody:
    def __init__(self, obj: dict):
        self.id = obj.get('id')
        self.name = obj.get('name')
        self.description = wiki_queries_dict.get(f'{self.id}')
        self.englishName = obj.get('englishName')
        self.img_high_res = f'{sys.path[0]}/planet_textures/{self.id}.jpeg'
        self.img_small_res = f'{sys.path[0]}/planet_textures_smaller/{self.id}.jpeg'
        self.radius = obj.get('meanRadius')
        self.mass = obj.get('mass').get('massValue') * pow(10, obj.get('mass').get('massExponent'))
        self.volume = obj.get('vol').get('volValue') * pow(10, obj.get('vol').get('volExponent'))

    """
    get_dynamic_data() is the class function that returns real-time data for bodies. 
    Returns current distance between the body and the planet Earth
    """

    def get_dynamic_data(self):
        get_earth_distance(self.englishName)


"""
Planet is the child class of the CelestialBody class, describing inner data for planet-alike bodies. 
Meant to represent planets of Solar System.
"""


class Planet(CelestialBody):
    def __init__(self, obj: dict):
        super().__init__(obj)
        self.position = obj.get('position')
        self.number_of_moons = len(obj.get('moons')) if obj.get('moons') is not None else 0
        # self.moons = obj.get('moons')
        self.gravity = obj.get('gravity')
        self.temperature = round(int(obj.get('avgTemp')) - 273.15, 2)
        self.escape_velocity = obj.get('escape')

    """
    overriding of the get_dynamic_data() class function for planets
    """

    def get_dynamic_data(self):
        if self.englishName == "Earth":
            return earth_data()
        else:
            return get_earth_distance(self.englishName, self.position)


"""
Star is the child class of the CelestialBody class, describing inner data for star-alike bodies. 
Meant to represent the Sun.
"""


class Star(CelestialBody):
    def __init__(self, obj: dict):
        super().__init__(obj)
        self.temperature = round(5780 - 273.15, 2)

    def get_dynamic_data(self):
        return get_earth_distance(self.englishName)


"""
Moon is the child class of the CelestialBody class, describing inner data for moon-alike bodies. 
Meant to represent the Moon.
"""


class Moon(CelestialBody):
    def __init__(self, obj: dict):
        super().__init__(obj)
        self.temperature = round(220 - 273.15, 2)
        self.discovery_date = obj.get('discoveryDate')
        self.discovered_by = obj.get('discoveredBy')
        self.gravity = obj.get('gravity')

    def get_dynamic_data(self):
        return get_earth_distance(self.englishName)


"""
a function, computing the distance between the body and the planet Earth.
Takes two arguments. Second argument is optional, for the positions are defined only for planets,
but not for the sun and the moon
"""


def get_earth_distance(english_name, position=None):
    if english_name == "Sun":
        sun = ephem_bodies_list[0]
        sun.compute()
        return sun.earth_distance
    if english_name == "Moon":
        moon = ephem_bodies_list[1]
        moon.compute()
        return moon.earth_distance
    else:
        ephem_planet = ephem_bodies_list[position + 1]
        ephem_planet.compute()
        return ephem_planet.earth_distance


"""
Auxiliary function that could be used to return the data related to the Earth
"""


def earth_data():
    return None
