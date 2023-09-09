import sys, argparse, os
from PIL import Image, ImageOps, ImageDraw, ImageFont
import random

import csv

verbs = ['give', 'offer', 'throw', 'show', 'sell']
informativities = ['control', 'low', 'high']

recipients = {v : [] for v in verbs}

for recipient_file in os.listdir('../characters/recipient/'):
    if recipient_file.endswith('-sell.png'):
        recipients['sell'].append((Image.open(f'../characters/recipient/{recipient_file}'),
                    recipient_file.split('-')[0]))
    elif recipient_file.endswith('.png'):
        for v in verbs:
            if v != 'sell':
                recipients[v].append((Image.open(f'../characters/recipient/{recipient_file}'),
                    recipient_file.split('.')[0]))

def make_or_append(d, k, v):
    if k not in d:
        d[k] = [v]
    else:
        d[k].append(v)

def make_grid(verb, informativity):
    all_agents = {}

    for agent_file in os.listdir(f'../characters/{verb}/'):
        if not agent_file.endswith('.png'):
            continue
        make_or_append(all_agents, agent_file.split('-')[0], agent_file)

    themes = []

    if informativity == 'control':
        agent = max(all_agents, key = lambda x : len(all_agents[x]))
        agent_themes = all_agents[agent]
        random.shuffle(agent_themes)

        scene_recipients = random.sample(recipients[verb], 4)

        for theme in agent_themes:
            themes.append((Image.open(f'../characters/{verb}/{theme}'), theme.split('-')[2][:-4]))

        scene_list = [[r[0], t[0]] for t, r in zip(themes, scene_recipients)]
        labels = [f'{agent}-{verb}-{t[1]}-{r[1]}' for t, r in zip(themes, scene_recipients)]

    else:
        agent = random.choice(list(all_agents.keys()))
        agent_themes = all_agents[agent]

        for theme in agent_themes:
            themes.append((Image.open(f'../characters/{verb}/{theme}'), theme.split('-')[2][:-4]))

        if informativity == 'low':
            scene_themes = random.sample(themes, 2)
            scene_recipients = random.sample(recipients[verb], 2)

        if informativity == 'high':
            scene_themes = random.sample(themes, 1)
            scene_recipients = random.sample(recipients[verb], 4)

        scene_list = [[r[0], t[0]] for t in scene_themes for r in scene_recipients]
        labels = [f'{agent}-{verb}-{t[1]}-{r[1]}' for t in scene_themes for r in scene_recipients]

    scene = []

    for i, images in enumerate(scene_list):
        widths, heights = zip(*(i.size for i in images))
        total_width = sum(widths)
        max_height = max(heights)

        new_img = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for img in images:
            new_img.paste(img, (x_offset, 0))
            x_offset += img.size[0]

        scene.append((new_img, labels[i]))

    # scene = [img, img, img, img]
    random.shuffle(scene)

    for img in scene:
        img[0].save('../../experiment/client/public/img/' + img[1] + '.png')

    return labels

with open('../../experiment/server/src/samplestims.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['trialid', 'images', 'target', 'verb'])
    i = 1
    for verb in verbs:
        for informativity in informativities:
            labels = make_grid(verb, informativity)
            writer.writerow([i, ','.join(labels), labels[random.randrange(4)], verb])
            i += 1


