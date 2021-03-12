import random


class RSA:
    def _gcd(self, a, b):
        """
        Euclid's algorithm to find GCD
        """
        while b != 0:
            a, b = b, a % b
        return a

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

    def _is_prime(self, num):
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


    def gen_keys(self, p, q):
        if not (self._is_prime(p) and self._is_prime(q)):
            raise ValueError('Both numbers must be prime.')
        elif p == q:
            raise ValueError('p and q cannot be equal')
        # n = pq
        n = p * q

        # Phi is the totient of n
        phi = (p - 1) * (q - 1)

        # Choose an integer e such that e and phi(n) are coprime
        e = random.randint(1, phi)

        # Use Euclid's Algorithm to verify that e and phi(n) are comprime
        g = self._gcd(e, phi)
        while g != 1:
            e = random.randint(1, phi)
            g = self._gcd(e, phi)

        # Use Extended Euclid's Algorithm to generate the private key
        d = self._mult_inverse(e, phi)

        # Return public (e, n) and private (d, n) keypair
        return (e, n), (d, n)

    def _power(self, a, n, m):
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

    def encrypt(self, p, text):
        # Unpack the key into it's components
        key, n = p
        # Convert each letter in the plaintext to numbers based on the character using a^b mod m
        cipher = [self._power(ord(char), key, n) for char in text]
        # Return the array of bytes
        return cipher

    def decrypt(self, p, text):
        # Unpack the key into its components
        key, n = p
        # Generate the plaintext based on the ciphertext and key using a^b mod m
        plain = [chr(self._power(char, key, n)) for char in text]
        # Return the array of bytes as a string
        return ''.join(plain)


if __name__ == '__main__':
    rsa = RSA()

    p, q = 3557, 2579
    public, private = rsa.gen_keys(p, q)
    print(f"Public key: {public})")
    print(f"Private key: {private}")
    text = "Hello word!!!"

    print("Text:", text)
    encrypted_msg = rsa.encrypt(private, text)
    print("Encrypted:", ''.join(map(lambda x: str(x), encrypted_msg)))

    decrypted_msg = rsa.decrypt(public, encrypted_msg)
    print("Decrypted:", decrypted_msg)
