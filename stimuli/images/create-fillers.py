import sys, argparse, os
from PIL import Image, ImageOps, ImageDraw, ImageFont
import random

transitivities = ['transitive', 'intransitive']

def make_or_append(d, k, v):
    if k not in d:
        d[k] = [v]
    else:
        d[k].append(v)

def create_grid(scene, padding = 20):
    max_width = max(image[0].width for image in scene)
    max_height = max(image[0].height for image in scene)

    for j, image in enumerate(scene):
        scene[j][0] = image[0].resize((max_width, max_height), Image.Resampling.LANCZOS)

    grid = Image.new("RGB", (4 * padding + 2 * max_width + 1, 4 * padding + 2 * max_height + 1), 'white')

    x = 0
    y = 0

    for image in scene:
        grid.paste(image[0], (x + padding, y + padding))
        x += max_width + 2 * padding + 1
        if x >= grid.width:
            x = 0
            y += max_height + 2 * padding + 1

    return grid

def draw_lines(grid, padding = 20, verb = '', text = False):
    if text == True:
        text_grid = Image.new(grid.mode, (grid.width, grid.height + 106), (255, 255, 255))
        text_grid.paste(grid, (0, 0))

        draw = ImageDraw.Draw(text_grid)
        draw.line([(grid.width // 2, padding), (grid.width // 2, grid.height - padding)], fill=(0, 0, 0), width=1)
        draw.line([(padding, grid.height // 2), (grid.width - padding, grid.height // 2)], fill=(0, 0, 0), width=1)
        draw.line([(0, grid.height + 5), (text_grid.width, grid.height + 5)], fill=(0, 0, 0), width=1)

        font = ImageFont.truetype("/Library/Fonts/Canela-Light-Trial.otf", 50)

        text_bbox = draw.textbbox((0, 0), verb, font=font)
        x = (text_grid.width - text_bbox[2]) // 2
        y = grid.height + (106 - text_bbox[3]) // 2

        draw.text((x, y), verb, font=font, fill=(0, 0, 0))

    else:
        text_grid = Image.new(grid.mode, (grid.width, grid.height), (255, 255, 255))
        text_grid.paste(grid, (0, 0))

        draw = ImageDraw.Draw(text_grid)
        draw.line([(grid.width // 2, padding), (grid.width // 2, grid.height - padding)], fill=(0, 0, 0), width=1)
        draw.line([(padding, grid.height // 2), (grid.width - padding, grid.height // 2)], fill=(0, 0, 0), width=1)
        draw.line([(0, grid.height + 5), (text_grid.width, grid.height + 5)], fill=(0, 0, 0), width=1)

    return text_grid


def make_transitive_grid():
    images = []

    for file in os.listdir(f'../characters/transitive/'):
        if not file.endswith('.jpg'):
            continue
        images.append([Image.open(f'../characters/transitive/{file}'), file[:-4]])

    random.shuffle(images)

    all_scenes = [images[i * 4 : (i + 1) * 4] for i in range(len(images) // 4)]

    for i, scene in enumerate(all_scenes):
        # scene = [[img, verb], [img, verb], [img, verb], [img, verb]]
        random.shuffle(scene)

        listener_grid = create_grid(scene)

        random.shuffle(scene)

        target = random.randrange(4)
        scene[target][0] = ImageOps.expand(scene[target][0], border=5, fill='red')
        verb = scene[target][1].split('-')[1]
        title = scene[target][1]

        speaker_grid = create_grid(scene)

        speaker = draw_lines(speaker_grid, verb = verb, text = True)
        listener = draw_lines(listener_grid)

        speaker.save(f'transitive/speaker/{title}.pdf')
        listener.save(f'transitive/listener/{title}.pdf')

def make_intransitive_grid():
    all_images = []

    for file in os.listdir(f'../characters/intransitive/'):
        if not file.endswith('.jpg'):
            continue
        all_images.append([Image.open(f'../characters/intransitive/{file}'), file[:-4]])

    distractors = []

    for file in os.listdir(f'../characters/intransitive/distractors/'):
        if not file.endswith('.jpg'):
            continue
        distractors.append([Image.open(f'../characters/intransitive/distractors/{file}'), file[:-4]])

    images = [all_images.pop(random.randrange(len(all_images))) for _ in range(6)]
    distractors.extend(all_images)
    random.shuffle(distractors)
    
    all_scenes = [[images[i]] + distractors[i * 3 : (i + 1) * 3] for i in range(len(images))]

    for i, scene in enumerate(all_scenes):
        target = scene[0]
        random.shuffle(scene)

        listener_grid = create_grid(scene)

        random.shuffle(scene)

        target_index = scene.index(target)

        scene[target_index][0] = ImageOps.expand(scene[target_index][0], border=5, fill='red')
        verb = scene[target_index][1].split('-')[1]
        title = scene[target_index][1]

        speaker_grid = create_grid(scene)

        speaker = draw_lines(speaker_grid, verb = verb, text = True)
        listener = draw_lines(listener_grid)

        speaker.save(f'intransitive/speaker/{title}.pdf')
        listener.save(f'intransitive/listener/{title}.pdf')


make_transitive_grid()
make_intransitive_grid()

