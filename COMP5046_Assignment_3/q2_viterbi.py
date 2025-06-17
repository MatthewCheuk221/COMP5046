# This is the function you need to implement
def viterbi(tokens, distributions, transitions, labels):
    dp_table = []
    backtrack = []
    for _ in range(len(tokens)):
        dp_table.append({})
        backtrack.append({})
        
    for label in labels:
        dp_table[0][label] = transitions[("START", label)] * distributions[0][label]
        backtrack[0][label] = None

    for i in range(1, len(tokens)):
        for current_label in labels:
            current_score = 0
            best_prev_label = None
            for prev_label in labels:
                prob = dp_table[i-1][prev_label] * transitions[(prev_label, current_label)] * distributions[i][current_label]
                if prob > current_score:
                    current_score = prob
                    best_prev_label = prev_label

            dp_table[i][current_label] = current_score
            backtrack[i][current_label] = best_prev_label

    score = 0
    best_label = None
    for label in labels:
        prob = dp_table[len(tokens)-1][label] * transitions[(label, "END")]
        if prob > score:
            score = prob
            best_label = label

    label_sequence = [None] * len(tokens)
    label_sequence[-1] = best_label
    for i in range(len(tokens)-1, 0, -1):
        label_sequence[i-1] = backtrack[i][label_sequence[i]]

    return score, label_sequence