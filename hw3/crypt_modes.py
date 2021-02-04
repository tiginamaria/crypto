from crypt_utils import *


def CBC(text, block_size, initial_vector, is_encode):
    text = text_to_bits(text)
    text_blocks = split(text, block_size)
    initial_vector = text_to_bits(initial_vector)[:block_size]
    bits = []
    if is_encode:
        for text_block in text_blocks:
            initial_vector = xor(text_block, initial_vector)
            bits += initial_vector
    else:
        for text_block in text_blocks:
            bits += xor(text_block, initial_vector)
            initial_vector = text_block
    return bits_to_text(bits)


