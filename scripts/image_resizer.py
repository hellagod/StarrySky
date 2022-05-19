from PIL import Image
import os

files = os.listdir('./planet_textures/')
path = './planet_textures/'
for file in files:
    extension = os.path.splitext(file)[1]
    if extension == ".jpeg":
        image = Image.open(path + file)
        width, height = image.size
        width = int(width/5)
        height = int(height/5)
        size = width, height
        image_resized = image.resize(size)
        image_resized.save(f"./planet_textures_smaller/smaller_{file}")