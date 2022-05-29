"""
image_resizer.py is a utility script, that helps to make the rendering of textures faster.
Changes the 2k resolution texture to a smaller one, for the sake of
faster loading of the main menu with planets' cards.
"""

import sys

from PIL import Image
import os
files = os.listdir(sys.path[0]+'/planet_textures')
path = sys.path[0]+'/planet_textures/'
for file in files:
    extension = os.path.splitext(file)[1]
    if extension == ".jpeg":
        image = Image.open(path + file)
        width, height = image.size
        width = int(width/5)
        height = int(height/5)
        size = width, height
        image_resized = image.resize(size)
        image_resized.save(sys.path[0]+f"/planet_textures_smaller/{file}")
