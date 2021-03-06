from crypt_utils import *


class GOST:
    # Box of 8 shuffle matrix S0 S1 S2 ... S8
    S = [[9, 6, 3, 2, 8, 11, 1, 7, 10, 4, 14, 15, 12, 0, 13, 5],
         [3, 7, 14, 9, 8, 10, 15, 0, 5, 2, 6, 12, 11, 4, 13, 1],
         [14, 4, 6, 2, 11, 3, 13, 8, 12, 15, 5, 10, 0, 7, 1, 9],
         [14, 7, 10, 12, 13, 1, 3, 9, 0, 2, 11, 4, 15, 8, 5, 6],
         [11, 5, 1, 9, 8, 13, 15, 0, 14, 4, 2, 3, 12, 7, 10, 6],
         [3, 10, 13, 12, 1, 2, 0, 11, 7, 5, 9, 4, 8, 15, 14, 6],
         [1, 13, 2, 9, 7, 10, 6, 0, 8, 12, 4, 5, 15, 3, 11, 14],
         [11, 10, 15, 5, 0, 12, 14, 8, 6, 2, 3, 9, 1, 7, 13, 4]]

    def encrypt(self, key, text):
        text = pad(text)
        return self.crypt(key, text, True)

    def decrypt(self, key, text):
        text = self.crypt(key, text, False)
        return unpad(text)

    def _CBC(self, text_bits, block_size, iv, is_encode):
        text_blocks = split(text_bits, block_size)
        iv = text_to_bits(iv)[:block_size]
        bits = []
        if is_encode:
            for text_block in text_blocks:
                iv = xor(text_block, iv)
                bits += iv
        else:
            for text_block in text_blocks:
                bits += xor(text_block, iv)
                iv = text_block
        return bits

    def crypt(self, key, text, is_encrypt=True):
        keys = self._gen_keys(key)
        iv = text_to_bits(key)[:64]
        bits = []

        # Split text into blocks of 8 chars
        text_blocks = split(text, 8)
        for text_block in text_blocks:
            # Convert 8 chars to 64 bits
            text_bits = text_to_bits(text_block)
            # Split text block into half: 64 -> 32 | 32
            if is_encrypt:
                text_bits = xor(iv, text_bits)

            l, r = split(text_bits, 32)

            for i in range(32):
                # Xor expanded left part with key: 32 -> 32
                if is_encrypt:
                    l0 = add(keys[i], l)
                else:
                    l0 = add(keys[31 - i], l)
                # Split l0 into 8 blocks of 4 bits
                l_blocks = split(l0, 4)
                for j in range(8):
                    # Shuffle l_block of 4 bits with S
                    l_blocks[j] = shuffle(l_blocks[j], self.S[j])
                # Merge l_blocks to l0
                l0 = merge(l_blocks)
                # Shift l into 11 bits left
                l0 = shift(l0, 11)
                l, r = xor(r, l0), l
            # Merge left and right part: 32 | 32 -> 64
            bits_block = r + l

            bits += bits_block if is_encrypt else xor(iv, bits_block)
            iv = bits_block if is_encrypt else text_bits

        return bits_to_text(bits)

    # Return 8 keys of 32 bits from initial key
    def _gen_keys(self, key):
        # Get 256 bits of initial key
        key = key[:32]
        # Translate key to bits
        key_bits = text_to_bits(key)
        # Split key into parts: 256 -> 8 * | 32 |
        key_blocks = split(key_bits, 32)

        # Add 3 * key + 1 reversed key
        keys = 3 * key_blocks
        keys += list(reversed(key_blocks))

        return keys


if __name__ == '__main__':
    g = GOST()

    d_key = (5 * "12345678")[:32]
    d_text = "Hello world123!!!"
    print('key:', d_key)
    print('text:', d_text)
    code = g.encrypt(d_key, d_text)
    print('encrypted:', code)
    d_text = g.decrypt(d_key, code)
    print('decrypted:', d_text)
