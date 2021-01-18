import unittest
from parameterized import parameterized
import string

from kasiski import Kasiski
from messege_utils import preprocess_message
from vigenere import Vigenere


class VigenereTest(unittest.TestCase):

    def setUp(self) -> None:
        self.alphabet = {
            'a': 8.12,
            'b': 1.49,
            'c': 2.71,
            'd': 4.32,
            'e': 12.0,
            'f': 2.30,
            'g': 2.03,
            'h': 5.92,
            'i': 7.31,
            'j': 0.10,
            'k': 0.69,
            'l': 3.98,
            'm': 2.61,
            'n': 6.95,
            'o': 7.68,
            'p': 1.82,
            'q': 0.11,
            'r': 6.02,
            's': 6.28,
            't': 9.10,
            'u': 2.88,
            'v': 1.11,
            'w': 2.09,
            'x': 0.17,
            'y': 2.11,
            'z': 0.07}

    @parameterized.expand([
        ("short word", "abc", "c"),
        ("long word", "abc", "cccc"),
        ("different letters", "abc", "abcdefgh"),
    ])
    def test_encrypt_decrypt(self, test_name, key, word):
        v = Vigenere(self.alphabet, key)
        self.assertEqual(word, v.decrypt(v.encrypt(word)))

    @parameterized.expand([
        ("key with different letters", "crypt"),
        ("key with common letters", "mamaroma"),
        ("complicated key", "abcdefgh"),
    ])
    def test_kasiski(self, test_name, key):
        with open('message_1', 'r') as file:
            message = preprocess_message(file.read(), self.alphabet)
        v = Vigenere(self.alphabet.keys(), key)
        k = Kasiski(self.alphabet)
        self.assertEqual(len(key), k.find_key_len(v.encrypt(message)))
        self.assertEqual(key, k.find_key(v.encrypt(message)))

    def test_large_message(self):
        with open('message', 'r') as file:
            message = preprocess_message(file.read(), self.alphabet)
        key = 'crypt'
        v = Vigenere(self.alphabet.keys(), key)
        self.assertEqual(message, v.decrypt(v.encrypt(message)))
