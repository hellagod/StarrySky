import sys

from __init__ import ephem_bodies_list


class CelestialBody:
    def __init__(self, obj: dict):
        self.id = obj.get('id')
        self.name = obj.get('name')
        self.englishName = obj.get('englishName')
        self.img_high_res = f'{sys.path[0]}/planet_textures/{self.id}.jpeg'
        self.img_small_res = f'{sys.path[0]}/planet_textures_smaller/{self.id}.jpeg'
        self.radius = obj.get('meanRadius')
        self.mass = obj.get('mass').get('massValue') * pow(10, obj.get('mass').get('massExponent'))
        self.volume = obj.get('vol').get('volValue') * pow(10, obj.get('vol').get('volExponent'))

    def get_dynamic_data(self):
        get_earth_distance(self.englishName)


class Planet(CelestialBody):
    def __init__(self, obj: dict):
        super().__init__(obj)
        self.position = obj.get('position')
        self.number_of_moons = len(obj.get('moons')) if obj.get('moons') is not None else 0
        #self.moons = obj.get('moons')
        self.gravity = obj.get('gravity')
        self.temperature = round(int(obj.get('avgTemp')) - 273.15, 2)
        self.escape_velocity = obj.get('escape')

    def get_dynamic_data(self):
        if self.englishName == "Earth":
            return earth_data()
        else:
            return get_earth_distance(self.englishName, self.position)


class Star(CelestialBody):
    def __init__(self, obj: dict):
        super().__init__(obj)
        self.temperature = round(5780 - 273.15, 2)

    def get_dynamic_data(self):
        return get_earth_distance(self.englishName)


class Moon(CelestialBody):
    def __init__(self, obj: dict):
        super().__init__(obj)
        self.temperature = round(220 - 273.15, 2)
        self.discovery_date = obj.get('discoveryDate')
        self.discovered_by = obj.get('discoveredBy')
        self.gravity = obj.get('gravity')

    def get_dynamic_data(self):
        return get_earth_distance(self.englishName)


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


def earth_data():
    return None
