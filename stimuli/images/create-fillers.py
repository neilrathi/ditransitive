import sys, argparse, os
from PIL import Image, ImageOps, ImageDraw, ImageFont
import random

transitivities = ['transitive', 'intransitive']

def make_or_append(d, k, v):
    if k not in d:
        d[k] = [v]
    else:
        d[k].append(v)

def make_grid(transitivity):
    images = []

    for file in os.listdir(f'../characters/{transitivity}/'):
        if not file.endswith('.jpg'):
            continue
        images.append(Image.open(f'../characters/{transitivity}/{file}'))

    random.shuffle(images)
    all_scenes = [images[i * 4 : (i + 1) * 4] for i in range(len(images) // 4)]

    for i, scene in enumerate(all_scenes):
        target = random.randrange(4)
        scene[target] = ImageOps.expand(scene[target], border=5, fill='red')
        random.shuffle(scene)

        max_width = max(image.width for image in scene)
        max_height = max(image.height for image in scene)

        for j, image in enumerate(scene):
            scene[j] = image.resize((max_width, max_height), Image.Resampling.LANCZOS)

        padding = 20
        grid = Image.new("RGB", (4 * padding + 2 * scene[0].width + 1, 4 * padding + 2 * scene[0].height + 1), 'white')

        x = 0
        y = 0

        for image in scene:
            grid.paste(image, (x + padding, y + padding))
            x += scene[0].width + 2 * padding + 1
            if x >= grid.width:
                x = 0
                y += scene[0].height + 2 * padding + 1

        grid.save(f'{transitivity}/{i}.pdf')

for transitivity in transitivities:
    make_grid(transitivity)

