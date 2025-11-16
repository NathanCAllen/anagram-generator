import unittest
from anagram_generator import AnagramGenerator


class TestDictionary(unittest.TestCase):
    """Test suite for nested AnagramGenerator.Dictionary class."""

    @classmethod
    def setUpClass(cls):
        """Create a temporary test file with known words."""
        cls.test_file = "test_words.txt"
        cls.test_words = [
            "CAT", "DOG", "ACT", "TAC", "GOD", "BIRD", "LISTEN", "SILENT",
            "ENLIST", "EAT", "TEA", "ATE", "AT", "TA"
        ]

    def setUp(self):
        """Set up a fresh Dictionary for each test."""
        self.dictionary = AnagramGenerator.Dictionary(self.test_file)

    def test_initialization(self):
        """Test that dictionary initializes and loads words."""
        self.assertIsNotNone(self.dictionary._letterCombosByLength)
        self.assertIsNotNone(self.dictionary._wordTree)

    # insert

    def test_insert_new_word(self):
        """Test inserting a new word."""
        new_dict = AnagramGenerator.Dictionary(self.test_file)
        new_dict.insert("NEW")

        self.assertTrue(new_dict.contains("NEW"))

    def test_insert_anagram(self):
        """Test inserting a word that's an anagram of existing word."""
        new_dict = AnagramGenerator.Dictionary(self.test_file)

        new_dict.insert("NEWS")

        initial_result = new_dict.solve("NEWS")
        initial_count = len(initial_result)

        new_dict.insert("SEWN")

        new_result = new_dict.solve("NEWS")
        self.assertGreater(len(new_result), initial_count)

    # get_letter_combos_by_length

    def test_letter_combos_by_length(self):
        """Test that letter combos are correctly grouped by length."""
        length_2_words = self.dictionary.get_letter_combos_by_length(2)
        length_3_words = self.dictionary.get_letter_combos_by_length(3)
        length_4_words = self.dictionary.get_letter_combos_by_length(4)
        length_6_words = self.dictionary.get_letter_combos_by_length(6)

        self.assertEqual(len(length_2_words), 1)
        self.assertEqual(len(length_3_words), 3)
        self.assertEqual(len(length_4_words), 1)
        self.assertEqual(len(length_6_words), 1)

    def test_get_letter_combos_by_length_empty(self):
        """Test getting letter combos for a length that doesn't exist."""
        result = self.dictionary.get_letter_combos_by_length(100)
        self.assertEqual(result, set())

    def test_get_letter_combos_by_length_too_short(self):
        """Test getting letter combos for a length that is too short."""
        with self.assertRaises(ValueError) as context:
            self.dictionary.get_letter_combos_by_length(1)

        self.assertIn("No words are less than 2 characters long",
                      str(context.exception))

    def test_letter_combos_by_length_structure(self):
        """Test that _letterCombosByLength stores sorted character strings."""
        length_3 = self.dictionary.get_letter_combos_by_length(3)

        for sorted_word in length_3:
            self.assertEqual(len(sorted_word), 3)

    # solve

    def test_solve_simple_anagram(self):
        """Test solving a simple anagram."""
        result = self.dictionary.solve("TAC")
        self.assertEqual(len(result), 3)
        self.assertIn("CAT", result)
        self.assertIn("ACT", result)
        self.assertIn("TAC", result)

    def test_solve_another_anagram(self):
        """Test solving anagram with different letters."""
        result = self.dictionary.solve("ODG")
        self.assertIn("DOG", result)
        self.assertIn("GOD", result)

    def test_solve_long_anagram(self):
        """Test solving a longer anagram."""
        result = self.dictionary.solve("SILENT")
        self.assertIn("LISTEN", result)
        self.assertIn("SILENT", result)
        self.assertIn("ENLIST", result)

    def test_solve_scrambled_letters(self):
        """Test that solve works regardless of letter order."""
        result1 = self.dictionary.solve("EAT")
        result2 = self.dictionary.solve("TEA")
        result3 = self.dictionary.solve("ATE")

        self.assertEqual(result1, result2)
        self.assertEqual(result2, result3)
        self.assertIn("EAT", result1)
        self.assertIn("TEA", result1)
        self.assertIn("ATE", result1)

    def test_solve_nonexistent_anagram(self):
        """Test solving an anagram that doesn't exist."""
        result = self.dictionary.solve("XYZ")
        self.assertEqual(result, set())

    def test_solve_case_insensitive(self):
        """Test that solve handles lowercase input."""
        result_upper = self.dictionary.solve("CAT")
        result_lower = self.dictionary.solve("cat")

        self.assertEqual(result_upper, result_lower)

    def test_solve_with_extra_letters(self):
        """Test that solve doesn't match words with fewer letters."""
        result = self.dictionary.solve("CATS")

        self.assertNotIn("CAT", result)
        self.assertNotIn("ACT", result)

    def test_solve_with_fewer_letters(self):
        """Test that solve doesn't match words with more letters."""
        result = self.dictionary.solve("CA")

        self.assertNotIn("CAT", result)
        self.assertNotIn("ACT", result)

    # contains

    def test_contains_existing_word(self):
        """Test contains method with existing word."""
        self.assertTrue(self.dictionary.contains("CAT"))
        self.assertTrue(self.dictionary.contains("DOG"))
        self.assertTrue(self.dictionary.contains("LISTEN"))

    def test_contains_anagram_of_word(self):
        """Test that contains returns true for anagrams."""
        self.assertTrue(self.dictionary.contains("ACT"))  # anagram of CAT
        self.assertTrue(self.dictionary.contains("TAC"))  # anagram of CAT

    def test_contains_nonexistent_word(self):
        """Test contains method with non-existent word."""
        self.assertFalse(self.dictionary.contains("FAKE"))
        self.assertFalse(self.dictionary.contains("XYZ"))


if __name__ == '__main__':
    unittest.main()
