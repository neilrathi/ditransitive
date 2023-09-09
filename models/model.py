import numpy as np
import pandas as pd

numstates = 6

states = ['teacher student book']
utterances = [u for u in states[0].split(' ')]
for i in range(0, numstates - 1):
    states.append(f'teacher student Alt{i}')
    utterances.append(f'Alt{i}')

# very basic meaning function [[u]](s) returns true if u \in s
# we can play around with building out states to contain more abstract information
def meaning(state, utt):
    return 1 if utt in state else 0

# helper function
def normalize(d):
    return {k : d[k] / sum(d.values()) for k in d}

# uniform
def automatic_policy(utt):
    return 1 / len(utterances)

def state_prior(state):
    return 1 / len(states)

def literal_listener(utt):
    counts = {state : meaning(state, utt) * state_prior(state) for state in states}
    return normalize(counts)

def pragmatic_speaker(state, a = 1):
    probs = {}
    for utt in utterances:
        probs[utt] = np.exp(a * literal_listener(utt)[state]) * automatic_policy(utt)
    return normalize(probs)

def pragmatic_listener(utt):
    probs = {}
    for state in states:
        probs[state] = pragmatic_speaker(state)[utt] * state_prior(state)
    return normalize(probs)

probs = pragmatic_listener('book')
print(probs)

def policy(utt, goal, state, depth, a = 1, g = 0):
    if depth == 0:
        return np.exp(a * reward(utt, goal, state)) * automatic_policy(utt, state)
    else:
        value = normalize({u : reward(u, goal, f'{state} {utt}') - np.log(policy(u, goal, state, depth - 1)/automatic_policy(u, state)) for u in utterances})
        return np.exp(a * reward(utt, goal) + g * value)

probs = policy('book', 'teacher student book', '', 2)
print(probs)