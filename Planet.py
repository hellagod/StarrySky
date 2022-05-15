class Planet:
    def __init__(self, obj: dict):
        self.name = obj.get('name')
        self.id = obj.get('id')
        self.img_high_res = f'/StarrySky/planet_textures/{self.id}.jpg'
        #self.moons = obj.get('moons')
        self.gravity = obj.get('gravity')
        self.temperature = round(int(obj.get('avgTemp')) - 273.15, 2)
        self.radius = obj.get('meanRadius')
        self.mass = obj.get('mass').get('massValue') * pow(10, obj.get('mass').get('massExponent'))
        self.volume = obj.get('vol').get('volValue') * pow(10, obj.get('vol').get('volExponent'))
        self.escape_velocity = obj.get('escape')

class Moon:
    def __init__(self, obj: dict):
        self.f


# скачать в 2к и положить в отдельную папку
# уменьшить в 5 раз
