import sys, argparse, os
from PIL import Image

allfiles = []
all_verbs = ['transitive', 'intransitive']

def make_square(im, min_size=360, fill_color=(0, 0, 0, 0)):
    x, y = im.size
    size = max(min_size, x, y)
    new_im = Image.new('RGBA', (size, size), fill_color)
    new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    return new_im

for verb in all_verbs:
    for character in os.listdir(f'../characters/{verb}/'):
        if character.endswith('.png'):
            allfiles.append(f'../characters/{verb}/{character}')

images = [[Image.open(x), x] for x in allfiles]

baseheight = 360
for img in images:
    hpercent = (baseheight/float(img[0].size[1]))
    wsize = int((float(img[0].size[0])*float(hpercent)))
    im = img[0].resize((wsize,baseheight), Image.Resampling.LANCZOS)
    im.save(img[1])