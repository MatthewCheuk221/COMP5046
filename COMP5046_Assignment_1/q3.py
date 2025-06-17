import math

# This is the function you need to implement
def word_analogy(vector_dictionary: list[list[float]], word1: int, word2: int, word3: int) -> tuple[float, int]:
    """Predict a word given its context.

    Args:
        vector_dictionary (list[list[float]]): the vectors for each word in the vocabulary
        word1 (int): the first word in the equation
        word2 (int): the second word in the equation
        word3 (int): the third word in the equation

    Returns:
         tuple[float, int]: A tuple containing the similarity of the closest answer and the token ID of that answer
    """

    vector1 = vector_dictionary[word1]
    vector2 = vector_dictionary[word2]
    vector3 = vector_dictionary[word3]
    query_vector = []
    for i in range(len(vector_dictionary[0])):
        query_vector.append(vector1[i] - vector2[i] + vector3[i])

    excluded_words = {word1, word2, word3}
    max_similarity = 0
    closest_word = 0
    for i in range(len(vector_dictionary)):
        if i in excluded_words:
            continue

        dot_product = 0
        magnitude1 = 0
        magnitude2 = 0
        for j in range(len(vector_dictionary[0])):
            dot_product += query_vector[j] * vector_dictionary[i][j]
            magnitude1 += query_vector[j] ** 2
            magnitude2 += vector_dictionary[i][j] ** 2

        if magnitude1 == 0 or magnitude2 == 0 or dot_product == 0:
            similarity = 0
        else:
            similarity = dot_product / (math.sqrt(magnitude1) * math.sqrt(magnitude2))

        if similarity > max_similarity:
            max_similarity = similarity
            closest_word = i

    return max_similarity, closest_word