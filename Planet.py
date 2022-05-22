import sys

from scripts.name_translator import name_translator


class Planet:
    def __init__(self, obj: dict):
        self.name = obj.get('name')
        self.id = obj.get('id')
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


class Moon:
    def __init__(self, obj: dict):
        self.name = name_translator(obj.get('name'))
        self.id = obj.get('id')
        self.radius = obj.get('meanRadius')
        self.discovery_date = obj.get('discoveryDate')
        self.discovered_by = obj.get('discoveredBy')
        self.gravity = obj.get('gravity')
