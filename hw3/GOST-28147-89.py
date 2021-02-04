class GOST:
    # Box of 8 substitution matrix S0 S1 S2 ... S8
    S = [[9, 6, 3, 2, 8, 11, 1, 7, 10, 4, 14, 15, 12, 0, 13, 5],
         [3, 7, 14, 9, 8, 10, 15, 0, 5, 2, 6, 12, 11, 4, 13, 1],
         [14, 4, 6, 2, 11, 3, 13, 8, 12, 15, 5, 10, 0, 7, 1, 9],
         [14, 7, 10, 12, 13, 1, 3, 9, 0, 2, 11, 4, 15, 8, 5, 6],
         [11, 5, 1, 9, 8, 13, 15, 0, 14, 4, 2, 3, 12, 7, 10, 6],
         [3, 10, 13, 12, 1, 2, 0, 11, 7, 5, 9, 4, 8, 15, 14, 6],
         [1, 13, 2, 9, 7, 10, 6, 0, 8, 12, 4, 5, 15, 3, 11, 14],
         [11, 10, 15, 5, 0, 12, 14, 8, 6, 2, 3, 9, 1, 7, 13, 4]]

    def encrypt(self, key, text, pad=True):
        if pad:
            text = self._pad(text)
        print('after pad:', text)
        return self.crypt(key, text, True)

    def decrypt(self, key, text, unpad=True):
        text = self.crypt(key, text, False)
        print('before unpad:', text)
        if unpad:
            return self._unpad(text)
        return text

    def crypt(self, key, text, is_encrypt=True):
        keys = self._gen_keys(key)
        bits = []

        # Split text into blocks of 8 chars
        text_blocks = self._split(text, 8)
        for text_block in text_blocks:
            # Convert 8 chars to 64 bits
            text_bits = self._text_to_bits(text_block)
            # Split text block into half: 64 -> 32 | 32
            l, r = self._split(text_bits, 32)

            for i in range(32):
                # Xor expanded left part with key: 32 -> 32
                if is_encrypt:
                    l0 = self._add(keys[i], l)
                else:
                    l0 = self._add(keys[31 - i], l)
                # Split l0 into 8 blocks of 4 bits
                l_blocks = self._split(l0, 4)
                for j in range(8):
                    # Shuffle l_block of 4 bits with S
                    l_blocks[j] = self._apply(l_blocks[j], self.S[j])
                # Merge l_blocks to l0
                l0 = self._merge(l_blocks)
                # Shift l into 11 bits left
                l0 = self._shift(l0, 11)
                l, r = self._xor(r, l0), l
            # Merge left and right part: 32 | 32 -> 64
            bits_block = r + l

            bits += bits_block
        return self._bits_to_text(bits)

    # Return 8 keys of 32 bits from initial key
    def _gen_keys(self, key):
        # Get 256 bits of initial key
        key = key[:32]
        # Translate key to bits
        key_bits = self._text_to_bits(key)
        # Split key into parts: 256 -> 8 * | 32 |
        key_blocks = self._split(key_bits, 32)

        keys = 3 * key_blocks + list(reversed(key_blocks))

        return keys

    def _pad(self, text):
        b = 8 - (len(text) % 8)
        return text + b * chr(b)

    def _unpad(self, text):
        b = ord(text[-1])
        return text[:-b]

    def _text_to_bits(self, text):
        bits = []
        for char in text:
            bits += self._char_to_bits(char, 8)
        return bits

    def _char_to_bits(self, value, size):
        bits = (bin(value)[2:] if isinstance(value, int) else bin(ord(value))[2:]).zfill(size)
        return [int(bit) for bit in bits]

    def _bits_to_text(self, bits):
        text = ''.join([chr(int(y, 2)) for y in [''.join([str(x) for x in byte]) for byte in self._split(bits, 8)]])
        return text

    def _split(self, array, n):
        return [array[i:i + n] for i in range(0, len(array), n)]

    def _merge(self, arrays):
        result = []
        for array in arrays:
            result += array
        return result

    def _shift(self, array, n):
        return array[n:] + array[:n]

    def _xor(self, a1, a2):
        return [x ^ y for x, y in zip(a1, a2)]

    def _add(self, array1, array2):
        result = []
        extra = 0
        for a1, a2 in reversed(list(zip(array1, array2))):
            r = a1 + a2 + extra
            result.append(r % 2)
            extra = r // 2
        return list(reversed(result))

    def _to_int(self, array):
        return int(''.join([str(x) for x in array]), 2)

    def _apply(self, array, matrix):
        j = self._to_int(array)
        return [int(bit) for bit in bin(matrix[j])[2:].zfill(4)]


if __name__ == '__main__':
    g = GOST()

    d_key = (5 * "12345678")[:32]
    d_text = "abcdefghij"
    print('key:', d_key)
    print('input:', d_text)
    code = g.encrypt(d_key, d_text)
    print('encrypt:', code)
    d_text = g.decrypt(d_key, code)
    print('output:', d_text)


