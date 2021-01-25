class Vigenere:

    def __init__(self, alphabet, key):
        self.alphabet = alphabet
        self.key = key

        self.alphabet_size = len(alphabet)
        self.key_size = len(key)

        self.letter_to_index = {letter: i for i, letter in enumerate(alphabet)}
        self.index_to_letter = {i: letter for i, letter in enumerate(alphabet)}

        self.key_shifts = [self.letter_to_index[letter] for letter in key]

    def encrypt(self, message):
        return self._crypt(message, 1)

    def decrypt(self, message):
        return self._crypt(message, -1)

    def _shift(self, word_pos: int, char_index, shift_sign: int):
        shift = self.key_shifts[word_pos % self.key_size]
        return (char_index + shift_sign * shift) % self.alphabet_size

    def _message_to_char_indexes(self, word):
        return [self.letter_to_index[letter] for letter in word]

    def _char_indexes_to_message(self, char_indexes):
        return ''.join([self.index_to_letter[char_index] for char_index in char_indexes])

    def _crypt(self, message, shift_sign):
        char_indexes = self._message_to_char_indexes(message)
        shifted_char_indexes = [self._shift(word_pos, char_index, shift_sign)
                                for word_pos, char_index in enumerate(char_indexes)]
        shifted_message = self._char_indexes_to_message(shifted_char_indexes)
        return shifted_message

