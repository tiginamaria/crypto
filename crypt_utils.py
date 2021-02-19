def pad(text, d=8):
    b = d - (len(text) % d)
    return text + b * chr(0)


def unpad(text, d=8):
    b = ord(text[-1])
    return text[:-b]


def bits_to_int(bits) -> int:
    return int(''.join([str(x) for x in bits]), 2)


def text_to_bits(text) -> []:
    bits = []
    for char in text:
        bits += char_to_bits(char, 8)
    return bits


def int_to_bits(x, bits):
    return list(map(int, list(format(x, 'b').zfill(bits))))


def char_to_bits(value, size) -> []:
    bits = (bin(value)[2:] if isinstance(value, int) else bin(ord(value))[2:]).zfill(size)
    return [int(bit) for bit in bits]


def bits_to_text(bits):
    text = ''.join([chr(int(y, 2)) for y in [''.join([str(x) for x in byte]) for byte in split(bits, 8)]])
    return text


def split(array, n) -> []:
    return [array[i:i + n] for i in range(0, len(array), n)]


def merge(arrays) -> []:
    result = []
    for array in arrays:
        result += array
    return result


def shift(array, n) -> []:
    return array[n:] + array[:n]


def xor(a1, a2) -> []:
    return [x ^ y for x, y in zip(a1, a2)]


def add(array1, array2) -> []:
    result = []
    extra = 0
    for a1, a2 in reversed(list(zip(array1, array2))):
        r = a1 + a2 + extra
        result.append(r % 2)
        extra = r // 2
    return list(reversed(result))


def to_int(array):
    return int(''.join([str(x) for x in array]), 2)


def shuffle(array, matrix) -> []:
    j = to_int(array)
    return [int(bit) for bit in bin(matrix[j])[2:].zfill(4)]


def apply(array, matrix):
    return [array[i - 1] for i in matrix]
