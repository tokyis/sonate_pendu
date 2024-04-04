import unittest
from server import build_dictionary, normalize_string, get_masked_word, is_word_found


class TestBuildDictionary(unittest.TestCase):
    def setUp(self):
        self.test_file_path = "test_file.txt"

    def test_build_dictionary(self):
        # Prepare a test file
        with open(self.test_file_path, 'w', encoding='utf-8') as file:
            file.write("firstValue1;secondValue1\nfirstValue2;secondValue2")

        # Run the function with the test file path
        result = build_dictionary(self.test_file_path)

        # Assert the result is as expected
        self.assertEqual(result, ["firstValue1", "firstValue2"])

    def tearDown(self):
        # Remove the test file
        import os
        os.remove(self.test_file_path)


class TestNormalizeString(unittest.TestCase):
    def test_normalize_string_with_accents(self):
        input_str = "áéíóú'"
        expected_output = "aeiou'"
        self.assertEqual(normalize_string(input_str), expected_output)

    def test_normalize_string_without_accents(self):
        input_str = "aeiou'"
        expected_output = "aeiou'"
        self.assertEqual(normalize_string(input_str), expected_output)

    def test_normalize_string_empty_input(self):
        input_str = ""
        expected_output = ""
        self.assertEqual(normalize_string(input_str), expected_output)


class TestGetMaskedWord(unittest.TestCase):

    def test_get_masked_word_all_guessed(self):
        word = "programming"
        guessed_letters = ["p", "r", "o", "g", "a", "m", "i", "n"]
        result = get_masked_word(word, guessed_letters)
        self.assertEqual(result, "p r o g r a m m i n g")

    def test_get_masked_word_some_guessed(self):
        word = "programming"
        guessed_letters = ["p", "r", "o"]
        result = get_masked_word(word, guessed_letters)
        self.assertEqual(result, "p r o _ r _ _ _ _ _ _")

    def test_get_masked_word_none_guessed(self):
        word = "programming"
        guessed_letters = []
        result = get_masked_word(word, guessed_letters)
        self.assertEqual(result, "_ _ _ _ _ _ _ _ _ _ _")

    def test_get_masked_word_empty_word(self):
        word = ""
        guessed_letters = ["p", "r", "o"]
        result = get_masked_word(word, guessed_letters)
        self.assertEqual(result, "")

    def test_get_masked_word_empty_guessed_letters(self):
        word = "programming"
        guessed_letters = []
        result = get_masked_word(word, guessed_letters)
        self.assertEqual(result, "_ _ _ _ _ _ _ _ _ _ _")


class TestIsWordFound(unittest.TestCase):

    def test_all_letters_guessed(self):
        guessed = ['a', 'b', 'c']
        word = "cab"
        result = is_word_found(guessed, word)
        self.assertEqual(result, True)

    def test_some_letters_guessed(self):
        guessed = ['a', 'b']
        word = "cab"
        result = is_word_found(guessed, word)
        self.assertEqual(result, False)

    def test_no_letters_guessed(self):
        guessed = []
        word = "cab"
        result = is_word_found(guessed, word)
        self.assertEqual(result, False)

    def test_word_with_repeated_letters(self):
        guessed = ['a', 'b', 'c']
        word = "cabbac"
        result = is_word_found(guessed, word)
        self.assertEqual(result, True)


if __name__ == "__main__":
    unittest.main()
