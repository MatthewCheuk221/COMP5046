# This is the function you need to implement
def get_confusion_matrix(eval_data, model, find_best_code):
    """Creates a confusion matrix by predicting the SQL for a question and recording how the answer compares with the true answer 

    Keyword arguments:
    eval_data -- a list of tuples containing the English question and the true SQL query
    model -- a CodeModel, as defined in the Model question
    find_best_code -- a function, the one defined the Inference question
    """
    
    confusion_matrix = {}
    for answer in model.labels:
        for guess in model.labels:
            confusion_matrix[(answer, guess)] = 0

    for question, answer in eval_data:
        confusion_matrix[(answer, find_best_code(question, model))] += 1

    return confusion_matrix