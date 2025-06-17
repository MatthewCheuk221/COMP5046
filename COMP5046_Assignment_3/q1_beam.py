# This is the function you need to implement
def beam(tokens, distributions, transitions, labels, k):
    beams = []
    for label in labels:
        score = transitions.get(("START", label), 0) * distributions[0].get(label, 0)
        beams.append((score, [label]))
    
    for i in range(1, len(tokens)):
        label_beam = []
        for score, sequence in beams:
            for label in labels:
                label_score = score * transitions.get((sequence[-1], label), 0) * distributions[i].get(label, 0)
                label_beam.append((label_score, sequence + [label]))
        
        label_beam.sort(reverse=True)
        beams = label_beam[:k]

    final_beam = []
    for score, sequence in beams:
        final_score = score * transitions.get((sequence[-1], "END"), 0)
        final_beam.append((final_score, sequence))
    
    final_beam.sort(reverse=True)
    score, label_sequence = final_beam[0]
    
    return score, label_sequence