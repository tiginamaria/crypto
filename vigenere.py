class Vigenere:

    def __init__(self, alphabet, key):
        self.alphabet = alphabet
        self.key = key

        self.alphabet_size = len(alphabet)
        self.key_size = len(key)

        self.letter_to_index = {letter: i for i, letter in enumerate(alphabet)}
        self.index_to_letter = {i: letter for i, letter in enumerate(alphabet)}

        self.key_shifts = [self.letter_to_index[letter] for letter in key]

    def encrypt(self, word):
        return self._crypt(word, 1)

    def decrypt(self, word):
        return self._crypt(word, -1)

    def _shift(self, word_pos: int, char_index, shift_sign: int):
        shift = self.key_shifts[word_pos % self.key_size]
        return (char_index + shift_sign * shift) % self.alphabet_size

    def _word_to_char_indexes(self, word):
        return [self.letter_to_index[letter] for letter in word]

    def _char_indexes_to_word(self, char_indexes):
        return ''.join([self.index_to_letter[char_index] for char_index in char_indexes])

    def _crypt(self, word, shift_sign):
        char_indexes = self._word_to_char_indexes(word)
        shifted_char_indexes = [self._shift(word_pos, char_index, shift_sign)
                                for word_pos, char_index in enumerate(char_indexes)]
        shifted_word = self._char_indexes_to_word(shifted_char_indexes)
        return shifted_word

