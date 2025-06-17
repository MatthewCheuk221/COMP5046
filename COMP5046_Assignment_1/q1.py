# These are the classes you need to implement
class DocVector(object):
    def __init__(self, vocab_length: int, doc: list[int]) -> None:
        """Store a document using a list the size of the vocabulary.

        Args:
            vocab_length (int): the size of the vocabulary
            doc (list[int]): a list of token IDs that represent a document
        """

        self.vector = [0 for _ in range(vocab_length)]
        for token in doc:
            self.vector[token] += 1
        self.length = math.sqrt(sum(v*v for v in self.vector))

    def get_count(self, token: int) -> int:
        """Get how frequently a given token appeared in the document.

        Args:
            token (int): the token ID

        Returns:
            int: the frequency of the token
        """

        return self.vector[token]

    def cosine_similarity(self, other: "DocVector") -> float:
        """Compare two documents of the same object type.

        Args:
            other (DocVector): the other document, also represented by this class you are defining

        Returns:
            float: the cosine similarity of the two documents
        """

        total = 0
        for i, count in enumerate(self.vector):
            total += count * other.vector[i]
        return total / (self.length * other.length)

class DocSparse(object):
    def __init__(self, doc: list[int]) -> None:
        """Store a document using a list, with tuples (token ID, count) for just the tokens in this document

        Arg:
            doc (list[int]): a list of token IDs that represent a document
        """

        doc.sort()
        self.vector = [[doc[0], 1]]
        for token in doc[1:]:
            if token == self.vector[-1][0]:
                self.vector[-1][1] += 1
            else:
                self.vector.append([token, 1])
        self.length = math.sqrt(sum(v[1]*v[1] for v in self.vector))

    def get_count(self, token: int) -> int:
        """Get how frequently a given token appeared in the document.

        Args:
            token (int): the token ID

        Returns:
            int: the frequency of the token
        """

        for num, count in self.vector:
            if num == token:
                return count
        return 0

    def cosine_similarity(self, other: "DocSparse") -> float:
        """Compare two documents of the same object type.

        Args:
            other (DocSparse): the other document, also represented by this class you are defining

        Returns:
            float: the cosine similarity of the two documents
        """

        total, cpos, opos = 0, 0, 0
        while cpos < len(self.vector) and opos < len(other.vector):
            cnum, ccount = self.vector[cpos]
            onum, ocount = other.vector[opos]
            if cnum == onum:
                total += ccount * ocount
                cpos += 1
                opos += 1
            elif cnum < onum:
                cpos += 1
            else:
                opos += 1
        return total / (self.length * other.length)

class DocDict(object):
    def __init__(self, doc: list[int]) -> None:
        """Store a document using a dictionary with token IDs as keys and counts as values.

        Args:
            doc (list[int]): a list of token IDs that represent a document
        """

        self.count_map = {}
        for token in doc:
            self.count_map[token] = self.count_map.get(token, 0) + 1
        self.length = math.sqrt(sum(v*v for v in self.count_map.values()))

    def get_count(self, token: int) -> int:
        """Get how frequently a given token appeared in the document.

        Args:
            token (int): the token ID

        Returns:
            int: the frequency of the token
        """

        return self.count_map.get(token, 0)

    def cosine_similarity(self, other: "DocDict") -> float:
        """Compare two documents of the same object type.

        Args:
            other (DocDict): the other document, also represented by this class you are defining

        Returns:
            float: the cosine similarity of the two documents
        """

        total = 0
        for token, count in self.count_map.items():
            if count > 0:
                total += count * other.count_map.get(token, 0)
        return total / (self.length * other.length)