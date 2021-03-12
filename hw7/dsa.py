import random
from hashlib import sha256
from random import randrange


class DSA:

    def _is_prime(self, num):
        return self._miller_rabin(num)

    def _is_prime_sqrt(self, num):
        """
        Test to see the number is prime
        """
        if num == 2:
            return True
        if num < 2 or num % 2 == 0:
            return False
        for n in range(3, int(num ** 0.5) + 2, 2):
            if num % n == 0:
                return False
        return True

    def _miller_rabin(self, n, k=7):
        """Use Rabin-Miller algorithm to return True (n is probably prime)
           or False (n is definitely composite)"""
        if n < 6:
            return [False, False, True, True, False, True][n]
        elif n & 1 == 0:
            return False
        else:
            s, d = 0, n - 1
            while d & 1 == 0:
                s, d = s + 1, d >> 1

            for a in random.sample(range(2, n - 2), min(n - 4, k)):
                x = pow(a, d, n)
                if x != 1 and x + 1 != n:
                    for r in range(1, s):
                        x = pow(x, 2, n)
                        if x != 1:
                            return False
                        elif x != - 1:
                            break
                    else:
                        return False
            return True

    def _powmod(self, a, n, m):
        """
        Fast power a ^ n % m
        """
        res = 1
        while n != 0:
            if n % 2 != 0:
                res *= a
                res %= m
                n -= 1
            else:
                a *= a
                a %= m
                n //= 2
        return res

    def _egcd(self, a, b):
        """
        Euclid's extended algorithm
        """
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = self._egcd(b % a, a)
            return g, x - (b // a) * y, y

    def _mult_inverse(self, a, m):
        """
        Finding the multiplicative inverse of two numbers
        """
        g, x, y = self._egcd(a, m)
        if g != 1:
            raise Exception('modular inverse does not exist')
        else:
            return x % m

    def generate_params(self, L, N):
        while True:
            q = randrange(1, 2 ** N)
            if self._is_prime(q):
                break
        while True:
            p = randrange(2 ** (L - 1), 2 ** L)
            if self._is_prime(p) and (p - 1) % q == 0:
                break
        while True:
            h = randrange(2, p - 1)
            g = self._powmod(h, (p - 1) // q, p)
            if g > 1:
                break
        return p, q, g

    def generate_keys(self, g, p, q):
        x = randrange(2, q)
        y = self._powmod(g, x, p)
        return x, y

    def sign(self, message, p, q, g, x):
        while True:
            k = randrange(2, q)
            r = self._powmod(g, k, p) % q
            if r == 0:
                continue
            m = int(sha256(message).hexdigest(), 16)
            try:
                s = (self._mult_inverse(k, q) * (m + x * r)) % q
                return r, s
            except Exception:
                pass

    def verify(self, message, r, s, p, q, g, y):
        m = int(sha256(message).hexdigest(), 16)
        w = self._mult_inverse(s, q)
        u1 = (m * w) % q
        u2 = (r * w) % q
        v = (self._powmod(g, u1, p) * self._powmod(y, u2, p)) % p % q
        if v == r:
            return True
        return False


if __name__ == "__main__":
    N = 10
    L = 30
    dsa = DSA()
    p, q, g = dsa.generate_params(L, N)
    print(f"parameters: p={p} q={q} g={g}")
    x, y = dsa.generate_keys(g, p, q)
    print(f"keys: x={x} y={y}")

    text = "MISIS rocks"
    message = str.encode(text, "ascii")
    r, s = dsa.sign(message, p, q, g, x)
    print(f"sign: r={r} s={s}")
    if dsa.verify(message, r, s, p, q, g, y):
        print('All ok')

