import sys, argparse, os
from PIL import Image, ImageOps, ImageDraw, ImageFont
import random

import csv
import itertools

verbs = ['give', 'offer', 'throw', 'show', 'sell']
informativities = ['control', 'low', 'high']

all_conditions = [list(cond) for cond in itertools.permutations(informativities, 3)]
conditions = []
for cond in all_conditions:
    conditions.append((cond[0], cond[0], cond[1], cond[1], cond[2]))

recipients = {v : [] for v in verbs}

for recipient_file in os.listdir('characters/recipient/'):
    if recipient_file.endswith('-sell.png'):
        recipients['sell'].append((Image.open(f'characters/recipient/{recipient_file}'),
                    recipient_file.split('-')[0]))
    elif recipient_file.endswith('.png'):
        for v in verbs:
            if v != 'sell':
                recipients[v].append((Image.open(f'characters/recipient/{recipient_file}'),
                    recipient_file.split('.')[0]))

def make_or_append(d, k, v):
    if k not in d:
        d[k] = [v]
    else:
        d[k].append(v)

# creates grid of four images for TEST condition (i.e. ditransitive)
def make_test_grid(verb, informativity):
    all_agents = {}

    for agent_file in os.listdir(f'characters/{verb}/'):
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
            themes.append((Image.open(f'characters/{verb}/{theme}'), theme.split('-')[2][:-4]))

        scene_list = [[r[0], t[0]] for t, r in zip(themes, scene_recipients)]
        labels = [f'{agent}-{verb}-{t[1]}-{r[1]}' for t, r in zip(themes, scene_recipients)]

    else:
        agent = random.choice(list(all_agents.keys()))
        agent_themes = all_agents[agent]

        for theme in agent_themes:
            themes.append((Image.open(f'characters/{verb}/{theme}'), theme.split('-')[2][:-4]))

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

        flipped = ImageOps.mirror(new_img)
        scene.append((flipped, labels[i]))

    # scene = [img, img, img, img]
    random.shuffle(scene)

    for img in scene:
        img[0].save('../experiment/client/public/img/' + img[1] + '.png')

    return (labels, verb, informativity)

def make_intransitive_grid():
    intransitives = []

    for file in os.listdir(f'characters/intransitive/'):
        if not file.endswith('.jpg'):
            continue
        intransitives.append([Image.open(f'characters/intransitive/{file}'), file[:-4]])

    # all of the non-target images (transitive distractors + a couple intransitives)
    distractors = []
    for file in os.listdir(f'characters/intransitive/distractors/'):
        if not file.endswith('.jpg'):
            continue
        distractors.append([Image.open(f'characters/intransitive/distractors/{file}'), file[:-4]])

    images = [intransitives.pop(random.randrange(len(intransitives))) for _ in range(6)] # randomly select 6 images to use
    distractors.extend(intransitives) # add other images to distractors
    random.shuffle(distractors) # shuffle !
    
    # a scene consists of a target image + 3 distractors
    all_scenes = [[images[i]] + distractors[i * 3 : (i + 1) * 3] for i in range(len(images))]

    all_labels = []
    for i, scene in enumerate(all_scenes):
        verb = scene[0][1].split('-')[1]
        all_labels.append(([x[1] for x in scene], verb, 'filler'))

        for img in scene:
            img[0].save('../experiment/client/public/img/' + img[1] + '.png')

    return all_labels

def make_transitive_grid():
    images = []

    for file in os.listdir(f'characters/transitive/'):
        if not file.endswith('.jpg'):
            continue
        images.append([Image.open(f'characters/transitive/{file}'), file[:-4]])

    random.shuffle(images)

    all_scenes = [images[i * 4 : (i + 1) * 4] for i in range(len(images) // 4)]

    all_labels = []
    for i, scene in enumerate(all_scenes):
        random.shuffle(scene)
        verb = scene[0][1].split('-')[1]
        all_labels.append(([x[1] for x in scene], verb, 'filler'))

        for img in scene:
            img[0].save('../experiment/client/public/img/' + img[1] + '.png')
    
    return all_labels

with open('allstims.csv', 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['images', 'target', 'verb', 'informativity'])

    all_labels = []

    for verb in verbs:
        for informativity in informativities:
            labels = make_test_grid(verb, informativity)
            all_labels.append(labels)
    
    all_labels.extend(make_intransitive_grid())
    all_labels.extend(make_transitive_grid())

    for labels in all_labels:
        writer.writerow([','.join(labels[0]), labels[0][0], labels[1], labels[2]])

for cond in conditions:
    condition_rows = []
    with open('allstims.csv', 'r') as f:
        reader = csv.reader(f)
        cur_index = 0
        for row in reader:
            if row[3] == 'filler':
                condition_rows.append(row)
            if cur_index > 4:
                continue
            if row[2] == verbs[cur_index] and row[3] == cond[cur_index]:
                condition_rows.append(row)
                cur_index += 1
    
    random.shuffle(condition_rows)

    with open(f'../experiment/server/src/stims-{"".join([x[0] for x in cond])}.csv', 'w') as f:
        writer = csv.writer(f)
        writer.writerow(['trialid', 'images', 'target', 'verb', 'informativity'])
        i = 1
        for row in condition_rows:
            writer.writerow([i] + row)
            i += 1