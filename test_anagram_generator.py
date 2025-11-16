import unittest
from anagram_generator import AnagramGenerator


class TestAnagramGenerator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Set up test data once for all tests."""
        cls.test_file = "test_words.txt"
        cls.generator = AnagramGenerator()

    def test_initialization(self):
        """Test that generator initializes with a dictionary."""
        self.assertIsNotNone(self.generator.dictionary)

    # generate_anagrams

    def test_generate_anagrams_returns_correct_count(self):
        """Test that generate_anagrams returns correct number of anagrams."""
        anagrams = self.generator.generate_anagrams(word_size=5, count=3, count_fake=0)
        self.assertEqual(len(anagrams), 3)

    def test_generate_anagrams_correct_length(self):
        """Test that generated anagrams have the correct length."""
        word_size = 6
        anagrams = self.generator.generate_anagrams(word_size=word_size, count=5, count_fake=0)

        for anagram in anagrams:
            self.assertEqual(len(anagram), word_size)

    def test_generate_anagrams_are_shuffled(self):
        """Test that generated anagrams are shuffled (not original words)."""
        anagrams = self.generator.generate_anagrams(word_size=6, count=10, count_fake=0)

        for anagram in anagrams:
            solutions = self.generator.solve(anagram)
            self.assertTrue(anagram.upper() not in solutions)

    def test_generate_zero_anagrams(self):
        """Test generating zero anagrams."""
        anagrams = self.generator.generate_anagrams(word_size=5, count=0, count_fake=0)
        self.assertEqual(len(anagrams), 0)

    def test_generate_one_anagram(self):
        """Test generating exactly one anagram."""
        anagrams = self.generator.generate_anagrams(word_size=5, count=1, count_fake=0)
        self.assertEqual(len(anagrams), 1)
        self.assertEqual(len(anagrams[0]), 5)

    def test_generate_anagrams_with_fakes(self):
        """Test generating anagrams with fake words."""
        anagrams = self.generator.generate_anagrams(word_size=5, count=5, count_fake=2)

        self.assertEqual(len(anagrams), 5)

        # Two should be fake (not solvable)
        fake_count = 0
        for anagram in anagrams:
            if len(self.generator.solve(anagram)) == 0:
                fake_count += 1

        self.assertEqual(fake_count, 2)

    def test_generate_anagrams_raises_on_too_many_fakes(self):
        """Test that error is raised when count_fake > count."""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_anagrams(word_size=5, count=3, count_fake=5)

        self.assertIn("fake anagrams cannot be greater",
                      str(context.exception))

    def test_generate_anagrams_raises_on_insufficient_words(self):
        """Test that error is raised when not enough words of desired length."""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_anagrams(word_size=25, count=100, count_fake=0)

        self.assertIn("Not enough words", str(context.exception))

    def test_generate_anagrams_raises_on_insufficient_words_skip_unmixable_words(
            self):
        """Test that error is raised when not enough words of desired length after unmixable words are ignored."""
        with self.assertRaises(ValueError) as context:
            self.generator.generate_anagrams(word_size=2, count=89, count_fake=0)

        self.assertIn("Not enough words", str(context.exception))

    def test_generate_anagrams_no_fakes(self):
        """Test generating anagrams with no fakes (all solvable)."""
        anagrams = self.generator.generate_anagrams(word_size=4, count=3, count_fake=0)

        for anagram in anagrams:
            solutions = self.generator.solve(anagram)
            self.assertGreater(len(solutions), 0,
                               f"Anagram '{anagram}' should be solvable")

    def test_generate_all_fakes(self):
        """Test generating anagrams where all are fake."""
        anagrams = self.generator.generate_anagrams(word_size=5, count=5, count_fake=5)

        # All should be fake
        fake_count = 0
        for anagram in anagrams:
            if len(self.generator.solve(anagram)) == 0:
                fake_count += 1

        self.assertEqual(fake_count, 5)

    # solve

    def test_solve_finds_anagrams(self):
        """Test that solve finds all anagrams of a word."""
        result = self.generator.solve("SILENT")
        self.assertIn("LISTEN", result)
        self.assertIn("SILENT", result)
        self.assertIn("ENLIST", result)

    # verify

    def test_verify_with_correct_answer(self):
        """Test verify returns True for valid anagram."""
        self.assertTrue(self.generator.verify("SILENT", "LISTEN"))
        self.assertTrue(self.generator.verify("TAC", "CAT"))

    def test_verify_with_incorrect_answer(self):
        """Test verify returns False for non-anagram."""
        self.assertFalse(self.generator.verify("HELLO", "WORLD"))
        self.assertFalse(self.generator.verify("CAT", "DOG"))

    def test_verify_case_insensitive(self):
        """Test that verify works with different cases."""
        self.assertTrue(self.generator.verify("cat", "ACT"))
        self.assertTrue(self.generator.verify("LISTEN", "silent"))

    def test_verify_with_same_word(self):
        """Test verify when anagram and answer are the same."""
        self.assertTrue(self.generator.verify("LISTEN", "LISTEN"))

    # _fakify

    def test_fakify_creates_unsolvable_word(self):
        """Test that _fakify creates words that can't be solved."""
        # Get a real anagram first
        real_anagrams = self.generator.generate_anagrams(word_size=5, count=1, count_fake=0)
        real_anagram = real_anagrams[0]

        # Fakify it
        fake = self.generator._fakify(real_anagram)

        # The fake should not be solvable
        solutions = self.generator.solve(fake)
        self.assertEqual(len(solutions), 0, f"Fake word '{fake}' should not be solvable")

    # constants

    def test_vowels_constant(self):
        """Test that _VOWELS constant is defined correctly."""
        expected_vowels = ['A', 'E', 'I', 'O', 'U']
        self.assertEqual(self.generator._VOWELS, expected_vowels)

    def test_easy_consonants_constant(self):
        """Test that _EASY_CONSONANTS constant is defined."""
        self.assertIsInstance(self.generator._COMMON_CONSONANTS, list)
        self.assertGreater(len(self.generator._COMMON_CONSONANTS), 0)
        self.assertIn('B', self.generator._COMMON_CONSONANTS)
        self.assertIn('T', self.generator._COMMON_CONSONANTS)

    def test_easy_vowels_constant(self):
        """Test that _EASY_VOWELS constant is defined."""
        expected_easy_vowels = ['A', 'E', 'I', 'O']
        self.assertEqual(self.generator._COMMON_VOWELS, expected_easy_vowels)


if __name__ == '__main__':
    unittest.main()
