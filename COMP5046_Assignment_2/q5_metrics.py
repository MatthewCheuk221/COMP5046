# These are the functions you need to implement
def calculate_accuracy(confusion_matrix, labels):
    """Returns the accuracy based on the contents of a confusion matrix

    Keyword arguments:
    confusion_matrix -- a dictionary, as defined in the Confusion Matrix question
    labels -- a set of strings, all the possible labels
    """
    
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
    """Returns a dict containing the precision for each label based on the contents of a confusion matrix

    Keyword arguments:
    confusion_matrix -- a dictionary, as defined in the Confusion Matrix question
    labels -- a set of strings, all the possible labels
    """
    
    precision_dictionary = {}
    for label in labels:
        true_positive = confusion_matrix.get((label, label), 0)
        false_positive = 0
        for other in labels:
            if other != label:
                false_positive += confusion_matrix.get((other, label), 0)
        
        if true_positive == 0 and false_positive == 0:
            precision_dictionary[label] = 1.0
        else:
            precision_dictionary[label] = true_positive / (true_positive + false_positive)

    return precision_dictionary

def calculate_recall(confusion_matrix, labels):
    """Returns a dict containing the recall for each label based on the contents of a confusion matrix

    Keyword arguments:
    confusion_matrix -- a dictionary, as defined in the Confusion Matrix question
    labels -- a set of strings, all the possible labels
    """
    
    recall_dictionary = {}
    for label in labels:
        true_positive = confusion_matrix.get((label, label), 0)
        false_negative = 0
        for other in labels:
            if other != label:
                false_negative += confusion_matrix.get((label, other), 0)
        
        if true_positive == 0 and false_negative == 0:
            recall_dictionary[label] = 1.0
        else:
            recall_dictionary[label] = true_positive / (true_positive + false_negative)
    
    return recall_dictionary

def calculate_macro_f1(confusion_matrix, labels):
    """Returns the Macro F-Score based on the contents of a confusion matrix

    Keyword arguments:
    confusion_matrix -- a dictionary, as defined in the Confusion Matrix question
    labels -- a set of strings, all the possible labels
    """
    
    f_scores = []
    
    precision = calculate_precision(confusion_matrix, labels)
    recall = calculate_recall(confusion_matrix, labels)
    
    for label in labels:
        if precision[label] == 0 and recall[label] == 0:
            harmonic_mean = 1.0
        else:
            harmonic_mean = 2 * precision[label] * recall[label] / (precision[label] + recall[label])

        f_scores.append(harmonic_mean)
    
    if len(f_scores) == 0:
        macro_f1 = 1.0
    else:
        macro_f1 = sum(f_scores) / len(f_scores)
    
    return macro_f1
