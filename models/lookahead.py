import numpy as np
import pandas as pd

numgoals = 6

goals = ['teacher student book']
utterances = [u for u in goals[0].split(' ')]
for i in range(0, numgoals - 1):
    goals.append(f'teacher student Alt{i}')
    utterances.append(f'Alt{i}')

# very basic meaning function [[u]](s) returns true if u \in s
# we can play around with building out states to contain more abstract information
def meaning(goal, utt):
    return 1 if utt in goal else 0

# helper function
def normalize(d):
    if sum(d.values()) == 0:
        return {k : 0 for k in d}
    else:
        return {k : d[k] / sum(d.values()) for k in d}

def uniform(l):
    return {i : 1 / len(l) for i in l}

def expected(support, dist):
    e = 0
    for k in support:
        e += support[k] * dist[k]
    return e

# uniform
def automatic_policy(utt, state):
    return 1 / len(utterances)

def goal_prior(goal):
    return 1 / len(goals)

def reward(goal, utt, state):
    print('State:', state)
    print('Goal:', goal)
    print('Utt:', utt)

    cur_goals = [g for g in goals if set(state.split(' ')).issubset(set(g.split(' ')))]

    print(cur_goals)

    counts = {g : meaning(g, utt) * goal_prior(g) for g in cur_goals}
    return normalize(counts)[goal]

def policy(goal, utt, state, depth, a = 1, gamma = 0.1):
    print(goal, '\t', utt, '\t', state, '\t', depth)
    if depth == 0:
        return np.exp(reward(goal, utt, state)) * automatic_policy(utt, state)
    else:
        # we are going to define the value of an UTTERANCE u rather than a state s' by equating s' = s + u
        if state == '':
            newstate = utt
        else:
            newstate = f'{state} {utt}'
        
        value = {
            u : a * reward(goal, u, newstate) - np.log(policy(goal, utt, newstate, depth - 1) / automatic_policy(utt, newstate)) for u in utterances
        }

        return np.exp(a * reward(goal, utt, state) + gamma * expected(value, uniform(utterances))) * automatic_policy(utt, state)
    

probs = policy('teacher student book', 'book', '', 2, gamma = 0)
print(probs)