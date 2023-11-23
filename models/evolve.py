import random
import numpy as np

numstates = 6

utt_categories = {
	'agent' : ['teacher', 'student', 'linguist', 'psychologist', 'kangaroo'],
	'recipient' : ['teacher', 'student', 'linguist', 'psychologist', 'kangaroo'],
	'theme' : ['book', 'chair', 'apple', 'banana', 'pen']
}
utterances = {u for c in utt_categories for u in utt_categories[c]}
states = []
while len(states) <= numstates:
	agent = random.choice(utt_categories['agent'])
	recipient = agent
	while recipient == agent:
		recipient = random.choice(utt_categories['recipient'])
	theme = random.choice(utt_categories['theme'])

	s = ' '.join([agent, recipient, theme])
	if s not in states:
		states.append(s)

# very straightforward MLE n-gram prior
def get_n_tuples(s, n):
	all_tuples = []
	for i, word in enumerate(s):
		if i <= len(s) - n:
			all_tuples.append(tuple(s[i:i+n]))
	return all_tuples

def generate_priors(corpus, n):
	counts = dict()
	normalizers = dict()
	for s in corpus:
		all_tuples = get_n_tuples(s.split(' '), n)
		for t in all_tuples:
			if t in counts:
				counts[t] += 1
			elif t not in counts:
				counts[t] = 1
			if t[:-1] in normalizers:
				normalizers[t[:-1]] +=1
			elif t[:-1] not in normalizers:
				normalizers[t[:-1]] = 1

	priors = dict()
	for t in counts:
		priors[t] = counts[t]/normalizers[t[:-1]]
	
	return priors

priors = generate_priors(states, 2)

def meaning(state, utt):
    return 1 if utt in state else 0

# helper function
def normalize(d):
    return {k : d[k] / sum(d.values()) for k in d}

# uniform
def automatic_policy(utt, c):
    return priors[tuple(c.extend(utt))]

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


print(pragmatic_speaker(states[0]))