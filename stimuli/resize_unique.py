import sys, argparse, os
from PIL import Image
import pandas as pd

allfiles = []

def make_square(img, min_size = 360, background_color = (255, 255, 255)):
    x, y = img.size
    img = img.convert('RGB')

    if x == y:
        result = Image.new(img.mode, (x, y), background_color)
        result.paste(img, (0, 0))
    elif x > y:
        result = Image.new(img.mode, (x, x), background_color)
        result.paste(img, (0, (x - y) // 2))
    else:
        result = Image.new(img.mode, (y, y), background_color)
        result.paste(img, ((y - x) // 2, 0))

    result = result.resize((min_size, min_size), Image.Resampling.LANCZOS)
    return result

for img in os.listdir(f'../experiment/client/public/unique/'):
    if img.endswith('.png'):
        allfiles.append((f'../experiment/client/public/unique/{img}', img))

images = [[Image.open(x), y] for x, y in allfiles]

for img in images:
    im = make_square(img[0])
    print(im.size)
    im.save(f'unique/{img[1]}')