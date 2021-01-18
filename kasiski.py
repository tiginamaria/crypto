from collections import Counter
from math import gcd
from typing import Dict


class Kasiski:

    def __init__(self, alphabet):
        self.alphabet = alphabet
        self.alphabet_size = len(alphabet)

    def find_key_len(self, message, min_key_len=3):
        bigrams = self._get_ngrams(message, 2)
        trigrams = self._get_ngrams(message, 3)

        bigrams_gcds = self._get_ngrams_gcds(bigrams)
        trigrams_gcds = self._get_ngrams_gcds(trigrams)

        gcds = filter(lambda g: g > min_key_len, bigrams_gcds + trigrams_gcds)
        counter = Counter(gcds)
        return counter.most_common(1)[0][0]

    def find_key(self, message, min_key_len=3):
        key_len = self.find_key_len(message, min_key_len)
        key = ''
        for k in range(key_len):
            key += self._find_key_char(message[k:][::key_len])
        return key

    def _find_key_char(self, message):
        char_counter = Counter(message)
        char_counter.update({char: 0 for char in self.alphabet.keys()})
        message_dict = dict(sorted(char_counter.items(), key=lambda item: item[1]))
        alphabet_dict = dict(sorted(self.alphabet.items(), key=lambda item: item[1]))

        shifts = []
        for message_char, alphabet_char in zip(message_dict, alphabet_dict):
            shifts.append((ord(message_char) - ord(alphabet_char) + self.alphabet_size) % self.alphabet_size)
        shift_counter = Counter(shifts)
        shift = shift_counter.most_common(1)[0][0]
        return list(self.alphabet.keys())[shift]

    def _get_ngrams_gcds(self, ngrams):
        return [self._get_ngram_gcd(ngram_pos) for ngram, ngram_pos in ngrams.items() if len(ngram_pos) > 1]

    def _get_ngram_gcd(self, ngram_pos):
        ngram_gcd = 0
        for i in range(1, len(ngram_pos)):
            ngram_gcd = gcd(ngram_gcd, ngram_pos[i] - ngram_pos[i - 1])
        return ngram_gcd

    def _get_ngrams(self, message, n) -> Dict:
        ngrams = dict()
        for i in range(len(message) - n):
            ngram = message[i:i + n]
            if ngram not in ngrams:
                ngrams[ngram] = []
            ngrams[ngram].append(i)
        return ngrams