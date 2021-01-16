import unittest
from parameterized import parameterized
import string

from vigenere import Vigenere


class VigenereTest(unittest.TestCase):

    def setUp(self) -> None:
        self.alphabet = list(string.ascii_lowercase)

    @parameterized.expand([
        ("short word", "abc", "c"),
        ("long word", "abc", "cccc"),
        ("different letters", "abc", "abcdefgh"),
    ])
    def test_encrypt_decrypt(self, test_name, key, word):
        v = Vigenere(self.alphabet, key)
        self.assertEqual(word, v.decrypt(v.encrypt(word)))
