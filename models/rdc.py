from transformers import GPT2Tokenizer, GPT2LMHeadModel
import torch
import numpy as np
import pandas as pd

OUTPUT_DIR = "gpt2"
device = 'cpu'
if torch.cuda.is_available():
    device = 'cuda'

tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")
model = model.to(device)

# extract p(w | context)
def prob(context, next_word):
    cur_ids = torch.tensor(tokenizer.encode(context)).unsqueeze(0).long().to(device)
    model.eval()
    with torch.no_grad():
        outputs = model(cur_ids, labels=cur_ids)
        loss, logits = outputs[:2]
        softmax_logits = torch.softmax(logits[0,-1], dim=0)
    return softmax_logits.to('cpu')[tokenizer(next_word)['input_ids']].numpy()[0]

def context(agent): return f'The {agent} gave the'

def reward(u, g, s, numalts):
    if u in s:
        pL = 1/numalts
    elif u in g:
        pL = 1
    else:
        pL = 0
    return np.log(pL*numalts)

def speaker(g, s, numalts):
    c = context(g.split(' ')[0])
    probs = {}
    for u in g.split(' ')[1:]:
        probs[u] = np.exp(np.log(prob(c, u)) + reward(u, g, s, numalts))
    factor = 1.0/sum(probs.values())
    return {k: v*factor for k, v in probs.items() }

print(speaker('teacher student book', 'teacher student', 2))