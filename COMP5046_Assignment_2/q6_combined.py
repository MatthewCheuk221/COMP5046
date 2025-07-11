# This is the function you need to implement
def main(filename, iterations, read_data, model_maker, learn, find_best_code, get_confusion_matrix, calculate_accuracy, calculate_macro_f1):
    """Trains and evaluates a model on some read_data

    Keyword arguments:
    filename -- a string, the location of a json file containing data
    iterations -- an integer, the number of iterations of training to do
    read_data -- a function, as defined in the Data question
    model_maker -- a class, as defined in the Model question
    learn -- a function, as defined in the Learning question
    find_best_code -- a function, as defined in the Inference question
    get_confusion_matrix -- a function, as defined in the Confusion Matrix question
    calculate_accuracy -- a function, as defined in the Evaluation Metrics question
    calculate_macro_f1 -- a function, as defined in the Evaluation Metrics question
    """

    data, queries = read_data(filename)
    model = model_maker(queries, data['train'])
    dev_scores = []
    for _ in range(iterations):
        for question, answer in data["train"]:
            learn(question, answer, model, find_best_code)

        development_confusion_matrix = get_confusion_matrix(data['dev'], model, find_best_code)
        development_accuracy = calculate_accuracy(development_confusion_matrix, queries)
        development_f_score = calculate_macro_f1(development_confusion_matrix, queries)
        dev_scores.append({'accuracy': development_accuracy, 'macro-f1': development_f_score})

    testing_confusion_matrix = get_confusion_matrix(data['test'], model, find_best_code)
    testing_accuracy = calculate_accuracy(testing_confusion_matrix, queries)
    testing_f_score = calculate_macro_f1(testing_confusion_matrix, queries)
    test_score = {'accuracy': testing_accuracy, 'macro-f1': testing_f_score}

    return dev_scores, test_score
