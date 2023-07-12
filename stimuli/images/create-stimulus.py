import sys, argparse, os
from PIL import Image, ImageOps, ImageDraw, ImageFont
import random

verbs = ['give', 'offer', 'throw', 'show', 'sell']
informativities = ['control', 'low', 'high']

recipients = {v : [] for v in verbs}

for recipient_file in os.listdir('../characters/recipient/'):
    if recipient_file.endswith('-sell.png'):
        recipients['sell'].append(Image.open(f'../characters/recipient/{recipient_file}'))
    elif recipient_file.endswith('.png'):
        for v in verbs:
            if v != 'sell':
                recipients[v].append(Image.open(f'../characters/recipient/{recipient_file}'))

def make_grid(verb, informativity):
    agents = []

    for agent_file in os.listdir(f'../characters/{verb}/'):
        if not agent_file.endswith('.png'):
            continue
        agents.append(Image.open(f'../characters/{verb}/{agent_file}'))

    if informativity == 'control':
        scene_agents = random.sample(agents, 4)
        scene_recipients = random.sample(recipients[verb], 4)

    if informativity == 'low':
        scene_agents = 2 * random.sample(agents, 2)
        scene_recipients = random.sample(recipients[verb], 4)

    if informativity == 'high':
        scene_agents = 4 * random.sample(agents, 1)
        scene_recipients = random.sample(recipients[verb], 4)

    scene_list = zip(scene_recipients, scene_agents)
    scene = []

    for images in scene_list:
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)

        new_img = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for img in images:
            new_img.paste(img, (x_offset, 0))
            x_offset += img.size[0]

        scene.append(new_img)

    # randomly select target image
    target = random.randrange(4)
    scene[target] = ImageOps.expand(scene[target], border=5, fill='red')
    random.shuffle(scene)

    max_width = max(image.width for image in scene)
    max_height = max(image.height for image in scene)

    for i, image in enumerate(scene):
        scene[i] = image.resize((max_width, max_height), Image.Resampling.LANCZOS)

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
    text_grid.save(f'{verb}/{informativity}.pdf')

for verb in verbs:
    for informativity in informativities:
        make_grid(verb, informativity)

