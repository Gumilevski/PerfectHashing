# IMPLEMENTING OF FKS PERFECT HASHING

import numpy as np
import string


def normalize(c):  # make letter's Unicode code starting from 1
    return ord(c) - ord('a') + 1


# filling an auxiliary array of coefficients
# of size word_len for calculating hash of the string
def fill_coefficients(word_len: int, number: int, module: int):
    coefficients = [1]
    for j in range(1, word_len):
        coefficients.append((coefficients[-1] * number) % module)
    return coefficients


# string hash calculation
def string_hash(string, coefficients, word_len, module) -> int:
    result = 0
    for i in range(word_len):
        result += (normalize(string[i]) * coefficients[i]) % module
        result %= module
    return result


# if hash collisions appear we calculate second level parameters,
# then we use second level parameters to calculate second level hashes.
# In the function below we calculate the second level parameter for
# the set of words (hash_equal_words) in such a way that all second
# level hashes are different and we store them in second_hashes
def second_level_hashing(hash_equal_words, word_len, module):
    size = len(hash_equal_words)
    second_hashes = np.zeros(size)  # an array of second level hashes for hash_equal_words
    number = 1  # our second level parameter
    while len(second_hashes) != len(np.unique(second_hashes)):
        # difference check: if any second level collisions appear,
        # then while-loop runs one more time
        counter = 0
        for word in hash_equal_words:
            number = np.random.randint(1, 100)
            coefficients = fill_coefficients(word_len, number, module)
            second_hashes[counter] = string_hash(word, coefficients, word_len, module) \
                                     % (size * size)
            counter += 1
    return number, second_hashes


# generating num_words random words of length word_len
def words_generation(num_words, word_len):
    words = []
    for i in range(num_words):
        new_word = ''.join(np.random.choice(list(string.ascii_letters), word_len))
        words.append(new_word)
    return np.array(words)


# preparing empty table to store first level hashes
def prepare_empty_table(num_words):
    empty_table = []
    for i in range(num_words):
        empty_table.append([])
    return empty_table


np.random.seed(10)

PRIME = 37
MODULE = 1000000013
WORD_LENGTH = 8
NUM_WORDS = 10_000

first_level_coefficients = fill_coefficients(WORD_LENGTH, PRIME, MODULE)

words_to_hash = words_generation(NUM_WORDS, WORD_LENGTH)
second_level_parameters = np.zeros(NUM_WORDS, dtype=int)
first_level_table = prepare_empty_table(NUM_WORDS)  # in the i-th position words with first hash equals i

for word in words_to_hash:  # first level hashing
    first_level_table[string_hash(word, first_level_coefficients, WORD_LENGTH, MODULE) % NUM_WORDS].append(word)

for i in range(NUM_WORDS):
    if len(first_level_table[i]) > 1:  # if hash collision appears
        second_level_parameters[i], _ = second_level_hashing(first_level_table[i], WORD_LENGTH, MODULE)

print(f'first_level_table:\n {first_level_table}')
print(f'second_level_parameters:\n {second_level_parameters}')


