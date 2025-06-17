'''Exhaustive Search (lecture 4)
In this question, you should explicitly consider every possible sequence labelling.

For example, in the two word sequence from the overview, Australia ! you should calculate the scores for:

LOC LOC

LOC O

O LOC

O O

Then return the highest probability sequence and its probability.

Note that, as discussed in lectures, this method does not scale well to long sequences or large sets of labels. All the test cases in this question will be small, so that isn't an issue.

We encourage you to use the itertools.product function (https://docs.python.org/3/library/itertools.html#itertools.product) in your implementation.'''
import itertools

# This is the function you need to implement


def exhaustive(tokens: str, distributions: list[dict[str, float]], transitions: dict[tuple[str, str], float], labels: set[str]):
    # TODO
    score = 0.0
    label_sequence = tuple()
    _labels = sorted(
        set((itertools.product(labels, repeat=len(tokens)))), reverse=True)

    for l in _labels:
        _score = 0.0

        for i, t in enumerate(tokens):
            label_possibility = distributions[i]

            if i == 0 and len(tokens) > 1:
                _score = label_possibility[l[i]] * transitions[tuple(
                    ("START", l[i]))] * transitions[tuple((l[i], l[i + 1]))]
            elif i != (len(tokens) - 1) and len(tokens) > 1:
                _score = _score * \
                    (label_possibility[l[i]] *
                     transitions[tuple((l[i], l[i + 1]))])
            elif i == (len(tokens) - 1) and len(tokens) > 1:
                _score = _score * \
                    (label_possibility[l[i]] *
                     transitions[tuple((l[i], "END"))])
            elif i == 0 and len(tokens) == 1:
                _score = label_possibility[l[i]] * transitions[tuple(
                    ("START", l[i]))] * transitions[tuple((l[i], "END"))]

        if _score > score:
            score = _score
            label_sequence = l

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

answer = exhaustive(tokens, distributions, transitions, labels)
if abs(answer[0] - 0.0058482000000000004) > 1e-10:
    print("Error in score")
if ' '.join(answer[1]) != 'LOC O O':
    print("Error in sequence")

print("Probability:", answer[0])
print("Label Sequence:", ' '.join(answer[1]))
# ans: 0.005842
