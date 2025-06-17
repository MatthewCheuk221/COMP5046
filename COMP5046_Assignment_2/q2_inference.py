# This is the function you need to implement
def find_best_code(question, model):
    """Predicts the SQL for a question by using a model to try all possible labels.

    Keyword arguments:
    question -- a string, the English question
    model -- a CodeModel, as defined in the Model question
    """
    
    best_score = 0
    best_code = ""
    for label in model.labels:
        score = model.get_score(question, label)
        if score > best_score or best_code == "":
            best_score = score
            best_code = label
            
    return best_code