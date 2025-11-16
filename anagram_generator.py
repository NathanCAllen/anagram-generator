from collections import defaultdict
from random import choice, sample, shuffle


class AnagramGenerator:
    """Helper class to generate, solve, and verify anagram puzzles."""

    def __init__(self, file_name: str = "./sowpods.txt"):
        self.dictionary = AnagramGenerator.Dictionary(file_name)

    def generate_anagrams(self, word_size: int, count: int, count_fake: int) -> list[str]:
        """Return a list of anagram puzzles of provided size with a given number of fake puzzles."""

        if count_fake > count:
            raise ValueError("Number of fake anagrams cannot be greater than number of total anagrams requested")

        if count == 0:
            return []

        anagrams = self._get_anagrams(word_size, count)

        # take count_fake words from this list and replace letters until we get a unique fake
        idxs_to_fakify = sample(range(len(anagrams)), count_fake)
        for idx in idxs_to_fakify:
            word_to_fakify = anagrams[idx]
            # run fakify until word is not in anagrams list
            while word_to_fakify in anagrams:
                word_to_fakify = self._fakify(word_to_fakify)
            anagrams[idx] = word_to_fakify

        return anagrams

    def solve(self, anagram: str) -> set[str]:
        """Return set of possible solutions for anagram."""
        return self.dictionary.solve(anagram)

    def verify(self, anagram: str, answer: str) -> bool:
        """Determine whether answer is a valid solution to anagram."""
        return answer.upper() in self.solve(anagram)

    def _get_anagrams(self, word_size: int, count: int) -> list[str]:
        """Return a list of unique anagrams."""

        # filter dictionary to words of provided size
        words = list(self.dictionary.get_letter_combos_by_length(word_size))

        # we want to avoid words that can't be anagramed into non-words
        # only two-letter words fall into this category, so we can focus on those
        if word_size == 2:
            words = [w for w in words if not self.dictionary.contains(w[::-1])]

        if len(words) < count:
            raise ValueError("Not enough words of desired length")

        anagrams: list[str] = []
        # retrieve desired number of words and create anagrams
        for pw in sample(words, count):
            chars = list(pw)
            solutions_for_pw = self.dictionary.solve(pw)
            while "".join(chars) in solutions_for_pw:
                shuffle(chars)
            anagrams.append("".join(chars))

        return anagrams

    # constants for fakifying words

    _VOWELS = ['A', 'E', 'I', 'O', 'U']

    # only use relatively common letters to make the fakes more believable
    _COMMON_CONSONANTS = ['B', 'C', 'D', 'F', 'G', 'H', 'K', 'L', 'M', 'N', 'P', 'R', 'S', 'T']
    _COMMON_VOWELS = ['A', 'E', 'I', 'O']

    def _fakify(self, anagram: str) -> str:
        """Create a fake but believable anagram by replacing one letter."""
        new_word = anagram
        while len(self.solve(new_word)) != 0:
            letter_to_change = choice(new_word)
            # replacing letter with another of its type will hopefully make these more believable
            if letter_to_change in self._VOWELS:
                new_word = new_word.replace(letter_to_change, choice(self._COMMON_VOWELS), 1)
            else:
                new_word = new_word.replace(letter_to_change, choice(self._COMMON_CONSONANTS), 1)
        return new_word

    class Dictionary:
        """Dictionary for help with generating verifying, and solving anagram puzzles."""

        class Node:
            """Node for AnagramDictionary's word tree."""

            def __init__(self):
                self.words: set[str] = set()
                self.children: defaultdict[str, AnagramGenerator.Dictionary.Node] = defaultdict(
                    AnagramGenerator.Dictionary.Node)

            def traverse(self, path: str) -> set[str]:
                """Travel path to end node and return words."""
                if path == "":
                    return self.words
                else:
                    return self.children[path[0]].traverse(path[1:])

        def __init__(self, file_name: str = "./sowpods.txt"):
            # sets of unique letter combinations that can be made into valid words
            self._letterCombosByLength: defaultdict[int, set[str]] = defaultdict(set)
            self._wordTree = AnagramGenerator.Dictionary.Node()

            with open(file_name) as file:
                for line in file.read().splitlines():
                    self.insert(line)

        def insert(self, word: str):
            """Add word to dictionary."""
            self._letterCombosByLength[len(word)].add("".join(sorted(word)))

            # insert into tree
            node = self._wordTree
            sorted_chars = sorted(word)
            for c in sorted_chars:
                node = node.children[c]
            node.words.add(word)

        def get_letter_combos_by_length(self, length: int) -> set[str]:
            """Return set of letter combinations of provided length that can be anagramed into one or more words in the dictionary."""
            if length < 2:
                raise ValueError("No words are less than 2 characters long")
            return self._letterCombosByLength[length]

        def solve(self, anagram: str) -> set[str]:
            """Return set of possible solutions for anagram."""
            return self._wordTree.traverse("".join(sorted(anagram.upper())))

        def contains(self, word: str) -> bool:
            """Determine whether word is in the dictionary."""
            return word in self.solve(word)
