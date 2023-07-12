import sys, argparse, os
from PIL import Image

"""parser = argparse.ArgumentParser()
parser.add_argument('--agent', type = str)
parser.add_argument('--theme', type = str, help = 'theme')
parser.add_argument('--recipient', type = str, help = 'recipient')
args = parser.parse_args()"""

all_verbs = ['give', 'offer', 'throw', 'show', 'sell']
normal_recipients = []
sell_recipients = []

for recipient in os.listdir('../characters/recipient/'):
    if recipient.endswith('-sell.png'):
        sell_recipients.append(recipient)
    elif recipient.endswith('.png'):
        normal_recipients.append(recipient)

for verb in all_verbs:
    if verb != 'sell':
        for agent in os.listdir(f'../characters/{verb}/'):
            if not agent.endswith('.png'):
                continue
            agent_file = f'../characters/{verb}/{agent}'
            for recipient in normal_recipients:
                recipient_file = f'../characters/recipient/{recipient}'
                images = [Image.open(x) for x in [recipient_file, agent_file]]
                widths, heights = zip(*(i.size for i in images))

                total_width = sum(widths)
                max_height = max(heights)

                new_im = Image.new('RGB', (total_width, max_height))

                x_offset = 0
                for im in images:
                    new_im.paste(im, (x_offset, 0))
                    x_offset += im.size[0]

                new_im.save(f'{verb}/{agent[:-4]}-{recipient[:-4]}.png')
    elif verb == 'sell':
        for agent in os.listdir(f'../characters/{verb}/'):
            if not agent.endswith('.png'):
                continue
            agent_file = f'../characters/{verb}/{agent}'
            for recipient in sell_recipients:
                recipient_file = f'../characters/recipient/{recipient}'
                images = [Image.open(x) for x in [recipient_file, agent_file]]
                widths, heights = zip(*(i.size for i in images))

                total_width = sum(widths)
                max_height = max(heights)

                new_im = Image.new('RGB', (total_width, max_height))

                x_offset = 0
                for im in images:
                    new_im.paste(im, (x_offset, 0))
                    x_offset += im.size[0]

                new_im.save(f'{verb}/{agent[:-4]}-{recipient[:-9]}.png')

"""
for verb in all_verbs:
    if verb != 'sell':
        for agent in os.listdir(f'../characters/{verb}/'):
            f = os.path.join(directory, filename)
            # checking if it is a file
            if os.path.isfile(f):
                print(f)
        agent = f'../characters/{verb}/{args.agent}-{verb}-{args.theme}.png'
        recipient = f'../characters/recipient/{args.recipient}.png'

        images = [Image.open(x) for x in [recipient, agent]]
        widths, heights = zip(*(i.size for i in images))

        total_width = sum(widths)
        max_height = max(heights)

        new_im = Image.new('RGB', (total_width, max_height))

        x_offset = 0
        for im in images:
            new_im.paste(im, (x_offset, 0))
            x_offset += im.size[0]

        new_im.save(f'{args.agent}-{verb}-{args.theme}-{args.recipient}.png')"""