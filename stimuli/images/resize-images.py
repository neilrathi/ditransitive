import sys, argparse, os
from PIL import Image

allfiles = []
all_verbs = ['transitive', 'intransitive']

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

    result.resize((min_size, min_size), Image.Resampling.LANCZOS)
    return result

for verb in all_verbs:
    for img in os.listdir(f'../characters/{verb}/'):
        if img.endswith('.jpg'):
            allfiles.append(f'../characters/{verb}/{img}')

images = [[Image.open(x), x] for x in allfiles]

for img in images:
    im = make_square(img[0])
    im.save(img[1])