import itertools

# This is the function you need to implement
def exhaustive(tokens, distributions, transitions, labels):
    score = 0
    label_sequence = []
    sequences = itertools.product(labels, repeat=len(tokens))
    for sequence in sequences:
        sequence_score = 1
        sequence_score *= transitions.get(("START", sequence[0]), 0)
        for i in range(len(tokens)):
            sequence_score *= distributions[i].get(sequence[i], 0)
            if i < len(tokens) - 1:
                sequence_score *= transitions.get((sequence[i], sequence[i+1]), 0)
        
        sequence_score *= transitions.get((sequence[-1], "END"), 0)
        if sequence_score > score or sequence_score == score and list(sequence) > label_sequence:
            score = sequence_score
            label_sequence = list(sequence)
    
    return score, label_sequence