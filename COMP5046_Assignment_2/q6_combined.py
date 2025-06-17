from q0_data import read_data
from q1_model import CodeModel as model_maker
from q2_inference import find_best_code
from q3_learning import learn
from q4_confusion import get_confusion_matrix
from q5_metrics import calculate_accuracy, calculate_macro_f1

# This is the function you need to implement
def main(filename, iterations):
    """Trains and evaluates a model on some read_data

    Keyword arguments:
    filename -- a string, the location of a json file containing data
    iterations -- an integer, the number of iterations of training to do
    """

    data, queries = read_data(filename)
    model = model_maker(queries, data['train'])
    dev_scores = []
    for i in range(iterations):
        print(f"Training Round {i+1} starts.")
        for question, answer in data["train"]:
            learn(question, answer, model, find_best_code)
        
        development_confusion_matrix = get_confusion_matrix(data['dev'], model, find_best_code)
        development_accuracy = calculate_accuracy(development_confusion_matrix, queries)
        development_f_score = calculate_macro_f1(development_confusion_matrix, queries)
        dev_scores.append({'accuracy': development_accuracy, 'macro-f1': development_f_score})
        print(f"Training Round {i+1} finishes.")

    print("Testing starts.")
    testing_confusion_matrix = get_confusion_matrix(data['test'], model, find_best_code)
    testing_accuracy = calculate_accuracy(testing_confusion_matrix, queries)
    testing_f_score = calculate_macro_f1(testing_confusion_matrix, queries)
    test_score = {'accuracy': testing_accuracy, 'macro-f1': testing_f_score}
    print("Testing finishes.")

    return dev_scores, test_score

if __name__ == '__main__':
    print(main("long_training.json", 10))