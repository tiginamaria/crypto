from crypt_utils import int_to_bits, text_to_bits, bits_to_text


class A5:

    def __init__(self):
        self.r1, self.r2, self.r3 = None, None, None

    def encrypt(self, key, text):
        return self._crypt(key, text)

    def decrypt(self, key, text):
        return self._crypt(key, text)

    def _crypt(self, key, text):
        key_bits = int_to_bits(key, 64)
        test_bits = text_to_bits(text)
        inf_key = self._gen_keys(key_bits)
        return bits_to_text([x ^ k for x, k in zip(test_bits, inf_key())])

    def return_bits(self):
        # get return bits from rs according to poly
        ret1 = self.r1[18] ^ self.r1[17] ^ self.r1[16] ^ self.r1[13] ^ 1
        ret2 = self.r2[21] ^ self.r2[20] ^ 1
        ret3 = self.r3[22] ^ self.r3[21] ^ self.r3[20] ^ self.r3[7] ^ 1
        return ret1, ret2, ret3

    def setup_keys(self, key_bits, frame_count):
        self.r1, self.r2, self.r3 = [0] * 19, [0] * 22, [0] * 23
        frame_bits = int_to_bits(frame_count, 22)

        # setup key xor with 64 key_bits + 22 frame bits ignore majority
        for b in key_bits + frame_bits:
            ret1, ret2, ret3 = self.return_bits()
            self.r1 = [ret1 ^ b] + self.r1[:18]
            self.r2 = [ret2 ^ b] + self.r2[:21]
            self.r3 = [ret3 ^ b] + self.r3[:22]

    def majority(self, sync1, sync2, sync3):
        # majority bit value
        return sync1 & sync2 | sync1 & sync3 | sync2 & sync3

    def clock(self):
        sync1, sync2, sync3 = self.r1[7], self.r2[9], self.r3[9]
        ret1, ret2, ret3 = self.return_bits()
        f = self.majority(sync1, sync2, sync3)
        res = 0
        if sync1 == f:
            res ^= self.r1[18]
            self.r1 = [ret1] + self.r1[:18]
        if sync2 == f:
            res ^= self.r2[21]
            self.r2 = [ret2] + self.r2[:21]
        if sync3 == f:
            res ^= self.r3[22]
            self.r3 = [ret3] + self.r3[:22]
        return res

    def _gen_keys(self, key_bits):

        def gen():
            i = 0
            while True:
                self.setup_keys(key_bits, i)
                for j in range(100 + 114):
                    res = self.clock()
                    if j >= 100:
                        yield res
                i += 1

        return gen


if __name__ == '__main__':
    g = A5()

    d_key = 42
    d_text = "Hello word!!!"
    print('key:', d_key)
    print('text:', d_text)

    code = g.encrypt(d_key, d_text)
    print('encrypted:', code)

    r_text = g.decrypt(d_key, code)
    print('decrypted:', r_text)
    assert d_text == r_text
