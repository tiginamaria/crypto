class DES:

    # Text initial permutation matrix
    PI = [58, 50, 42, 34, 26, 18, 10, 2,
          60, 52, 44, 36, 28, 20, 12, 4,
          62, 54, 46, 38, 30, 22, 14, 6,
          64, 56, 48, 40, 32, 24, 16, 8,
          57, 49, 41, 33, 25, 17, 9, 1,
          59, 51, 43, 35, 27, 19, 11, 3,
          61, 53, 45, 37, 29, 21, 13, 5,
          63, 55, 47, 39, 31, 23, 15, 7]

    # Inverse text initial permutation matrix
    INV_PI = [40, 8, 48, 16, 56, 24, 64, 32,
              39, 7, 47, 15, 55, 23, 63, 31,
              38, 6, 46, 14, 54, 22, 62, 30,
              37, 5, 45, 13, 53, 21, 61, 29,
              36, 4, 44, 12, 52, 20, 60, 28,
              35, 3, 43, 11, 51, 19, 59, 27,
              34, 2, 42, 10, 50, 18, 58, 26,
              33, 1, 41, 9, 49, 17, 57, 25]

    # Text explosion matrix
    E = [32, 1, 2, 3, 4, 5,
         4, 5, 6, 7, 8, 9,
         8, 9, 10, 11, 12, 13,
         12, 13, 14, 15, 16, 17,
         16, 17, 18, 19, 20, 21,
         20, 21, 22, 23, 24, 25,
         24, 25, 26, 27, 28, 29,
         28, 29, 30, 31, 32, 1]

    # Box of 8 substitution matrix S0 S1 S2 ... S8
    S = [
        [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
         [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
         [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
         [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13],
         ],
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
         [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
         [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
         [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9],
         ],
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
         [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
         [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
         [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12],
         ],
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
         [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
         [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
         [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14],
         ],
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
         [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
         [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
         [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3],
         ],
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
         [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
         [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
         [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13],
         ],
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
         [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
         [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
         [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12],
         ],
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
         [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
         [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
         [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11],
         ]
    ]

    # Text permutation matrix
    P = [16, 7, 20, 21, 29, 12, 28, 17,
         1, 15, 23, 26, 5, 18, 31, 10,
         2, 8, 24, 14, 32, 27, 3, 9,
         19, 13, 30, 6, 22, 11, 4, 25]

    # Key permutation matrix
    CD = [57, 49, 41, 33, 25, 17, 9,
          1, 58, 50, 42, 34, 26, 18,
          10, 2, 59, 51, 43, 35, 27,
          19, 11, 3, 60, 52, 44, 36,
          63, 55, 47, 39, 31, 23, 15,
          7, 62, 54, 46, 38, 30, 22,
          14, 6, 61, 53, 45, 37, 29,
          21, 13, 5, 28, 20, 12, 4]

    # Key shift matrix
    CD_SHIFT = [1, 1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 1]

    # Key selection matrix
    SEL = [14, 17, 11, 24, 1, 5, 3, 28,
           15, 6, 21, 10, 23, 19, 12, 4,
           26, 8, 16, 7, 27, 20, 13, 2,
           41, 52, 31, 37, 47, 55, 30, 40,
           51, 45, 33, 48, 44, 49, 39, 56,
           34, 53, 46, 42, 50, 36, 29, 32]

    def encrypt(self, key, text):
        text = self._pad(text)
        return self.crypt(key, text, True)

    def decrypt(self, key, text):
        text = self.crypt(key, text, False)
        return self._unpad(text)

    def crypt(self, key, text, is_encrypt=True):
        keys = self._gen_keys(key)
        bits = []

        # Split text into blocks of 8 chars
        text_blocks = self._split(text, 8)
        for text_block in text_blocks:

            # Convert 8 chars to 64 bits
            text_bits = self._text_to_bits(text_block)

            # Permute text block bits: 64 -> 64
            text_bits = self._apply(text_bits, self.PI)

            # Split text block into half: 64 -> 32 | 32
            l, r = self._split(text_bits, 32)

            for i in range(16):
                # Expand right part to match key len: 32 -> 48
                r0 = self._apply(r, self.E)
                # Xor expanded right part with key: 48 -> 48
                if is_encrypt:
                    r0 = self._xor(keys[i], r0)
                else:
                    r0 = self._xor(keys[15 - i], r0)
                # Substitute and compress: 48 -> 32
                r0 = self._substitute(r0)
                # Permute: 32 -> 32
                r0 = self._apply(r0, self.P)
                # Xor with left part: 32 -> 32
                r0 = self._xor(l, r0)
                # Swap left and right parts
                l, r = r, r0
            # Merge left and right part: 32 | 32 -> 64
            bits_block = r + l
            # Apply inverse permutation : 64 -> 64
            bits_block = self._apply(bits_block, self.INV_PI)

            bits += bits_block
        return self._bits_to_text(bits)

    # Return 16 keys of 48 bits from initial key
    def _gen_keys(self, key):
        # Get 64 bits of initial key
        key = key[:8]
        # Translate key to bits
        key_bits = self._text_to_bits(key)
        # Permute key and apply remove control bits: 64 -> 56
        key_bits = self._apply(key_bits, self.CD)
        # Split key into parts: 56 -> 28 | 28
        c, d = self._split(key_bits, 28)

        keys = []
        for i in range(16):
            # Shift key part: 28 -> 28
            c = self._shift(c, self.CD_SHIFT[i])
            # Shift key part: 28 -> 28
            d = self._shift(d, self.CD_SHIFT[i])
            # Merge key part: 28 | 28 -> 56
            key_bits = c + d
            # Select key bits: 56 -> 48
            key_bits = self._apply(key_bits, self.SEL)
            keys.append(key_bits)
        return keys

    def _substitute(self, array):
        # Split bits to 8 blocks of 6 bits
        blocks = self._split(array, 6)
        bits = []
        for k, block in enumerate(blocks):
            # Merge 1-4 bits and convert to number
            i = int(str(block[0]) + str(block[5]), 2)
            # Merge 0 and 5 bits and convert to number
            j = int(''.join([str(x) for x in block[1:][:-1]]), 2)
            # Get substitution by pos (i, j)
            s = self.S[k][i][j]
            # Convert to 4 bits
            bits += self._char_to_bits(s, 4)
        return bits

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

    def _shift(self, array, n):
        return array[n:] + array[:n]

    def _xor(self, a1, a2):
        return [x ^ y for x, y in zip(a1, a2)]

    def _apply(self, array, matrix):
        return [array[i - 1] for i in matrix]


if __name__ == '__main__':
    d = DES()
    d_key = "encryptk"
    d_text = "Hello world!!!"
    code = d.encrypt(d_key, d_text)
    print(code)
    d_text = d.decrypt(d_key, code)
    print(d_text)
