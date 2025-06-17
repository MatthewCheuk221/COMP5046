'''Beam Search (lecture 4)
In this question, use beam search to identify a label sequence. Since beam search is approximate, it may not be the highest probability sequence.

As a reminder, beam search works by labelling the sequence word by word, keeping track of a small number (K) of complete label sequences. At each step, we consider all possible ways to extend the current sequences one step. Then we keep the top K of those options.

This is an efficient method, but is not guaranteed to get the optimal solution.

For example, in the three word sequence Sydney is cool and labels LOC and O if the beam size is two, then you would:

Calculate probabilities for the two options on the first token (Sydney), taking into consideration the initial transition from START to a label.

Consider all possible ways of extending those initial sequences to also cover is.

Keep the top two sequences.

Consider all possible ways of extending to cover cool.

Keep the top two sequences.

Update the probabilities to consider the transition to END.

Return the highest probability option and it's probability.'''
# This is the function you need to implement
import itertools


def gen_new_beam(_beam: dict[tuple[str, str], float], distributions: list[dict[str, float]], transitions: dict[tuple[str, str], float], labels: set[str], k: int, str_len: int):

    new_beam = dict()

    for b_k, b_v in _beam.items():
        cur_temp_label = b_k[len(b_k) - 1]

        cur_token_index = len(b_k) - 2

        if cur_token_index == str_len:
            return _beam

        if cur_token_index < str_len - 1:
            for l in labels:
                temp = list(b_k)
                temp.append(l)
                temp_seq = tuple(temp)

                temp_score = b_v * \
                    distributions[cur_token_index + 1][l] * \
                    transitions[tuple((cur_temp_label, l))]

                new_beam.update({temp_seq: temp_score})
        elif cur_token_index == str_len - 1:
            temp = list(b_k)
            temp.append("END")
            temp_seq = tuple(temp)

            temp_score = b_v * transitions[tuple((cur_temp_label, "END"))]

            new_beam.update({temp_seq: temp_score})

    new_beam = dict(
        sorted(new_beam.items(), key=lambda item: (item[1], item[0]), reverse=True)[:k])
    
    print(new_beam)

    return gen_new_beam(new_beam, distributions, transitions, labels, k, str_len)


def beam(tokens: str, distributions: list[dict[str, float]], transitions: dict[tuple[str, str], float], labels: set[str], k: int):
    # TODO
    _beam = dict()

    for i, (t_k, t_v) in enumerate(transitions.items()):
        if t_k[0] == "START" and t_k[1] != "END" and len(tokens) > 0 and t_k[1] in labels:
            temp_score = distributions[0][t_k[1]] * t_v

            _beam.update({t_k: temp_score})
        elif t_k[0] == "START" and t_k[1] == "END" and len(tokens) == 0:
            temp_score = t_v

            _beam.update({t_k: temp_score})

    _beam = gen_new_beam(_beam, distributions,
                         transitions, labels, k, len(tokens))

    result = list(_beam.items())[:1][0]

    score = result[1]

    temp = []
    for i, r in enumerate(result[0]):
        if i >= 1 and i < len(result[0]) - 1:
            temp.append(r)
    label_sequence = tuple((temp))

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
k = 5

answer = beam(tokens, distributions, transitions, labels, k)

print("Probability:", answer[0])
print("Label Sequence:", ' '.join(answer[1]))

if abs(answer[0] - 0.0058482000000000004) > 1e-10:
    print("Error in score")
if ' '.join(answer[1]) != 'LOC O O':
    print("Error in sequence")
