import math
# This is the function you need to implement
def predict_word_and_dist(vector_dictionary: list[list[float]], matrix: list[list[float]], words: list[int]) -> tuple[int, float, list[float]]:
    """Predict a word given its context.

    Args:
        vector_dictionary (list[list[float]]): the vectors for each word in the vocabulary
        matrix (list[list[float]]): the weight matrix, arranged so that there are |vocab| vectors, all the same length
        words (list[int]): the token IDs for the words/tokens in the document

    Returns:
        tuple[int, float, list[float]]: A tuple containing the ID of the highest probability word, the probability of that word, and the distribution of probabilities
    """

    vectors = []
    for word in words:
        vectors.append(vector_dictionary[word])

    sum_vectors = [0] * len(vectors)
    avg_vectors = sum_vectors
    for vector in vectors:
        for i in range(len(vector)):
            sum_vectors[i] += vector[i]

    for i in range(len(vectors)):
        avg_vectors[i] = sum_vectors[i] / len(vectors)

    dot_products = []
    for row in matrix:
        value = 0
        for row_element, avg_vectors_element in zip(row, avg_vectors):
            value += row_element * avg_vectors_element
        dot_products.append(value)

    exponentials = []
    for dot_product in dot_products:
        exponentials.append(math.exp(dot_product - max(dot_products)))

    probabilities = []
    for exponential in exponentials:
        probabilities.append(exponential / sum(exponentials))

    highest_prob_value = probabilities[0]
    highest_prob_token = 0
    for i in range(len(probabilities)):
        if probabilities[i] > highest_prob_value:
          highest_prob_value = probabilities[i]
          highest_prob_token = i

    return highest_prob_token, highest_prob_value, probabilities

vector_dictionary = [[1, 1], [0, 0.2], [1.1, 1.2]]
matrix = [[1.2, 1.2], [1, 0.9], [1.1, 1.01]]
words = [0, 1]  #Context words
print(predict_word_and_dist(vector_dictionary, matrix, words))
