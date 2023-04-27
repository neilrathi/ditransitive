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

def sent_probs(sentence):
    outputs = []
    s_list = sentence.split()
    for i in range(1, len(s_list)):
        context = ' '.join(s_list[:i])
        outputs.append(prob(context, " " + s_list[i]))
    return outputs

words = {
    'book' : 'IO',
    'student' : 'OO',
    'television' : 'IO',
    'anteater' : 'OO'
}

tests = [{
        'IO' : 'the teacher gave the book to the student',
        'OO' : 'the teacher gave the student the book'
    }, {
        'IO' : 'the linguist gave the television to the anteater',
        'OO' : 'the linguist gave the anteater the television'
    }]

outputs = [[], []]

i = 0
for test_set in tests:
    for test in test_set:
        j = -1
        for word in test_set[test].split(' '):
            if word in words and words[word] == test:
                outputs[i].append([word, sent_probs(test_set[test])[j]])
            j += 1
    i += 1

df_likely = pd.DataFrame(outputs[0], columns=['support', 'prob'])
df_likely.to_csv('priors_likely.csv', sep = '\t', index = False)

df_unlikely = pd.DataFrame(outputs[1], columns=['support', 'prob'])
df_unlikely.to_csv('priors_unlikely.csv', sep = '\t', index = False)