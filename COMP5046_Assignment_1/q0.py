# This is the function you need to implement
def count_words(text: str, vocab: dict[str, int]) -> list[tuple[int, int]]:
    """Count the frequency of each word in a document.

    Args:
        text (str): the text of a document
        vocab (dict[str, int]): a dictionary that maps from strings to integers, where each string is a token and each integer is an ID

    Returns:
        list[tuple[int, int]]: A list of tuples, where each tuple has the ID of a word and the count of its frequency
    """

    counts = {}
    for token in text.split():
        if token in vocab:
            token_id = vocab[token]
            if token_id in counts:
                counts[token_id] += 1
            else:
                counts[token_id] = 1

    return list(counts.items())