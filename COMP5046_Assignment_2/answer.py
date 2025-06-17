import json

## Data

def read_data(filename):
    with open(filename, 'r') as json_file:
        json_data = json.load(json_file)

    data = {'train': [], 'dev': [], 'test': []}
    queries = set()
    for example in json_data:
        data[example['data']].append((example['question'], example['sql']))
        queries.add(example['sql'])

    return data, queries

## Model

class CodeModel:
    def __init__(self, labels, training_data):
        self.weights = {}
        self.labels = sorted(labels)
        for label in labels:
            self.weights[label] = {}

        pass

    def get_features(self, question, label):
        features = []
        for word in question.split():
            features.append((word, label))

        return features

    def get_score(self, question, label):
        score = 0
        for feature in self.get_features(question, label):
            if feature in self.weights[label]:
                score += self.weights[label][feature]

        return score

    def update(self, question, label, change):
        for feature in self.get_features(question, label):
            if feature not in self.weights[label]:
                self.weights[label][feature] = 0
                
            self.weights[label][feature] += change

        return

## Inference

def find_best_code(question, model):
    best_score = 0
    best_code = ""
    for label in model.labels:
        score = model.get_score(question, label)
        if score > best_score or best_code == "":
            best_score = score
            best_code = label

    return best_code

## Learning

def learn(question, answer, model, find_best_code):
    prediction = find_best_code(question, model)
    if prediction == answer:
        return
    else:
        model.update(question, answer, 1)
        model.update(question, prediction, -1)

## Confusion

def get_confusion_matrix(eval_data, model, find_best_code):
    confusion_matrix = {}
    for answer in model.labels:
        for guess in model.labels:
            confusion_matrix[(answer, guess)] = 0

    for question, answer in eval_data:
        confusion_matrix[(answer, find_best_code(question, model))] += 1

    return confusion_matrix

## Metrics

def calculate_accuracy(confusion_matrix, labels):
    correct = 0
    total = 0
    for answer, count in confusion_matrix.items():
        total += count
        if answer[1] == answer[0]:
            correct += count

    if total == 0:
        accuracy = 1.0
    else:
        accuracy = correct / total

    return accuracy

def calculate_precision(confusion_matrix, labels):
    precision_dictionary = {}
    for label in labels:
        true_positive = confusion_matrix.get((label, label), 0)
        false_positive = 0
        for other in labels:
            if other != label:
                false_positive += confusion_matrix.get((other, label), 0)

        if (true_positive == 0 and false_positive == 0):
            precision_dictionary[label] = 1.0
        else:
            precision_dictionary[label] = true_positive / (true_positive + false_positive)

    return precision_dictionary

def calculate_recall(confusion_matrix, labels):
    recall_dictionary = {}
    for label in labels:
        true_positive = confusion_matrix.get((label, label), 0)
        false_negative = 0
        for other in labels:
            if other != label:
                false_negative += confusion_matrix.get((label, other), 0)

        if (true_positive == 0 and false_negative == 0):
            recall_dictionary[label] = 1.0
        else:
            recall_dictionary[label] = true_positive / (true_positive + false_negative)

    return recall_dictionary

def calculate_macro_f1(confusion_matrix, labels):
    f_scores = []

    precision = calculate_precision(confusion_matrix, labels)
    recall = calculate_recall(confusion_matrix, labels)

    for label in labels:
        if (precision[label] == 0 and recall[label] == 0):
            harmonic_mean = 1.0
        else:
            harmonic_mean = 2 * precision[label] * recall[label] / (precision[label] + recall[label])

        f_scores.append(harmonic_mean)

    if len(f_scores) == 0:
        macro_f1 = 1.0
    else:
        macro_f1 = sum(f_scores) / len(f_scores)

    return macro_f1

## Combined

# def main(filename, iterations, read_data, model_maker, learn, find_best_code, get_confusion_matrix, calculate_accuracy, calculate_macro_f1):
def main(filename, iterations):
    data, queries = read_data(filename)
    model = CodeModel(queries, data['train'])
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

if __name__ == '__main__':
    print(main("long_training.json", 10))