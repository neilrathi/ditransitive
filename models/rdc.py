import numpy as np

numgoals = 4

# we encode goals as sets of objects
# and we define states similarly as 'partial' goals
goals = [{'teacher', 'student', 'book'}]

utterances = [u for u in goals[0]]
for i in range(0, numgoals - 1):
    goals.append({'teacher', 'student', f'Alt{i}'})
    utterances.append(f'Alt{i}')

maxlen = max([len(x) for x in goals])

# and then we define the reward of an utterance u in terms of a goal and a state
def meaning(goal, utt):
    return 1 if utt in goal else 0

def normalize(l):
    if sum(l) != 0:
        return [i / sum(l) for i in l]
    else:
        return [0 for i in l]

def uniform(l):
    return {i : 1 / len(l) for i in l}

def expected(support, dist):
    e = 0
    for k in support:
        e += support[k] * dist[k]
    return e

def reward(goal, u, state):
    # a list of all goals compatible with the current state
    valid_goals = [g for g in goals if state.issubset(g)]
    counts = [meaning(g, u) if g in valid_goals and u not in state else 0 for g in goals]

    return normalize(counts)[goals.index(goal)]

def automatic(utt, state):
    return 1 / len(utterances)

"""

p(TSB, book | teacher) = exp ( aR(TSB, book | teacher) + ln p0(book | teacher) + g * (R(TSB, u | teacher book) + ln p(TSB, student | teacher book) / p0(student | teacher book) + g * V(teacher book)))

p(TSB, book | teacher) = exp ( aR(TSB, book | teacher) + ln p0(book | teacher) + g * V(teacher book))
V(TSB, teacher book) = R(TSB, u | teacher book) + ln p(TSB, u | teacher book) / p0(u | teacher book) + V(teacher book u)

"""

"""
policy({'teacher', 'student', 'book'}, 'book', {''})
    = 
"""

# the policy is defined recursively in terms of itself and the value, which is defined recursively in terms of itself and the policy.
def policy(goal, utt, state, depth = maxlen, a = 1, gamma = 0.5):
    if depth == 1:
        probs = [np.exp(a * reward(goal, u, state)) * automatic(u, state) for u in utterances]
        return [i / sum(probs) for i in probs][utterances.index(utt)]
    
print(policy({'teacher', 'student', 'book'}, 'student', {'teacher'}, depth = 1))