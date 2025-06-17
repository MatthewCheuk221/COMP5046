'''Viterbi Search (lecture 5)
In this question, use Viterbi search to identify the highest probability label sequence.

For the Viterbi algorithm, we think about label sequences as paths through a lattice / grid. For example, here is a blue path through the red lattice of LOC and O labels for "Sydney is in Australia".


If you think of this like a graph, where each label is a node, then we are trying to find the path with the highest value. The Viterbi algorithm finds the highest probability path to every node in the lattice. The key idea is that the highest probability path to a particular spot (e.g., O above "in") is:

The highest probability path to some label, x, of the previous word
*
The probability of the edge from x to the label for this word

Re-using the example above, here are the two possibilities for this label. It could either come from LOC or O, followed by an edge / transition:


Given this observation, we can identify the best possible label sequence in two passes:

Move left-to-right through the sentence, working out for each word what the probability of reaching each possible label is, and noting what the previous label was

For the last word, work out the highest probability label and the previous label

Go backwards through the sentence, step-by-step, by going to the previous label written down at each step.

If we visualise what the algorithm would compute for the example above, it would look something like this (where the blue arrows indicate for each label what the previous label was, and the blue box indicates the best label of the last word):


In more detail, the steps of the algorithm are:

Calculate probabilities for the possible labels for the first word, taking into account the transition from START.

For every other word:

Consider each possible label, L

Consider each possible previous label, M

Calculate the probability of L, if we had come from M

Record the best way to get to L (ie., which label M was the best) and what the probability of it is

Determine the highest probability label for the final word by taking into consideration the END transition.

Starting from the final word and its label, go back through the lattice one step at a time to get the best sequence'''
# This is the function you need to implement


def calculate(distributions: list[dict[str, float]], transitions: dict[tuple[str, str], float], labels: set[str], prev_max_prob: list[list], str_len: int):
    _prev_max_prob = []

    for l in labels:
        prev_max_score = 0.0
        temp_max_seq = tuple()

        for _l in labels:
            prev_max = []

            for i in prev_max_prob:
                if i[0] == _l:
                    prev_max = i

            if len(prev_max[2]) == str_len + 1:
                return prev_max_prob

            temp_score = prev_max[1] * transitions[tuple((_l, l))]

            # if prev_max_score < temp_score:
            #     temp = list(prev_max[2])
            #     temp.append(l)
                
            #     temp_sorted = sorted(list((tuple(temp), temp_max_seq)), reverse=True)
                
            #     if (temp_sorted[0] == tuple(temp) and len(temp_max_seq) > 0) or len(temp_max_seq) == 0:
            #         prev_max_score = temp_score    
            #         temp_max_seq = tuple(temp)
            
            if prev_max_score < temp_score:
                prev_max_score = temp_score

                temp = list(prev_max[2])
                temp.append(l)
                temp_max_seq = tuple(temp)

        prev_max_score = prev_max_score * \
            (distributions[len(temp_max_seq) - 2][l])

        _prev_max_prob.append(list((l, prev_max_score, temp_max_seq)))

    return calculate(distributions, transitions, labels, _prev_max_prob, str_len)


def viterbi(tokens: str, distributions: list[dict[str, float]], transitions: dict[tuple[str, str], float], labels: set[str]):
    # TODO
    score = 0.0
    label_sequence = tuple()
    prev_max_prob = []

    first_seq_prob = dict()

    for i, (t_k, t_v) in enumerate(transitions.items()):
        if t_k[0] == "START" and t_k[1] != "END" and len(tokens) > 0 and t_k[1] in labels:
            temp_score = distributions[0][t_k[1]] * t_v

            temp = dict({t_k: temp_score})
            first_seq_prob.update(temp)
            prev_max_prob.append(list((t_k[1], temp_score, t_k)))
        elif t_k[0] == "START" and t_k[1] == "END" and len(tokens) == 0:
            temp_score = t_v

            temp = dict({t_k: temp_score})
            first_seq_prob.update(temp)
            prev_max_prob.append(list((t_k[1], temp_score, t_k)))

    prev_max_prob = calculate(
        distributions, transitions, labels, prev_max_prob, len(tokens))

    for _p in prev_max_prob:
        temp_score = _p[1] * transitions[tuple((_p[0], "END"))]

        if score < temp_score:
            score = temp_score

            temp1 = list(_p[2])
            temp1.pop(0)
            label_sequence = tuple(temp1)

    return score, label_sequence


# Sample data test
tokens = ["Sydney", "is", "nice"]
distributions = [
    {"LOC": 0.9, "O": 0.1},
    {"LOC": 0.05, "O": 0.95},
    {"LOC": 0.05, "O": 0.95},
]
transitions = {
    ("START", "O"): 0.8,
    ("START", "LOC"): 0.2,
    ("START", "END"): 0.0,
    ("O", "END"): 0.05,
    ("O", "O"): 0.9,
    ("O", "LOC"): 0.05,
    ("LOC", "END"): 0.05,
    ("LOC", "O"): 0.8,
    ("LOC", "LOC"): 0.2,
}
labels = {"LOC", "O"}

answer = viterbi(tokens, distributions, transitions, labels)
print("Probability:", answer[0])
print("Label Sequence:", ' '.join(answer[1]))

if abs(answer[0] - 0.0058482000000000004) > 1e-10:
    print("Error in score")
if ' '.join(answer[1]) != 'LOC O O':
    print("Error in sequence")
