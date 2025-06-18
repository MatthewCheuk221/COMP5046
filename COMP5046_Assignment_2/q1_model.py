# This is the class you need to implement
class CodeModel:
    def __init__(self, labels, training_data):
        """Prepare the class member variables.
        Save the labels in self.labels and initialise all the weights to 0.

        Keyword arguments:
        labels -- a set of strings, each string is one SQL query
        training_data -- a list, each item is a tuple containing a question and an SQL query
        """
        
        self.weights = {}
        self.labels = sorted(labels)
        for label in labels:
            self.weights[label] = {}

        return

    def get_features(self, question, label):
        """Produce a list of features for a specific question and label.
        
        Keyword arguments:
        question -- a string, an English question
        label -- a string, an SQL query
        """

        features = []
        for word in question.split():
            features.append((word, label))
        
        return features

    def get_score(self, question, label):
        """Calculate the model's score for a question, label pair.
        
        Keyword arguments:
        question -- a string, an English question
        label -- a string, an SQL query
        """
        
        score = 0
        for feature in self.get_features(question, label):
            if feature in self.weights[label]:
                score += self.weights[label][feature]

        return score

    def update(self, question, label, change):
        """Modify the model.
        Changes all weights for features for the (question, SQL query) pair by the amount indicated.

        Keyword arguments:
        question -- a string, an English question
        label -- a string, an SQL query
        change -- an integer, how much to change the weights
        """
        
        for feature in self.get_features(question, label):
            if feature not in self.weights[label]:
                self.weights[label][feature] = 0
                
            self.weights[label][feature] += change
        
        return
