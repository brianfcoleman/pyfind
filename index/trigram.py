from itertools import combinations, islice
from functools import partial
from re import finditer
from utils.functional import all_of


def is_empty(sequence):
    return len(sequence) == 0


def first(sequence):
    return sequence[0]


def last(sequence):
    return sequence[-1]


def at(sequence, index):
    return sequence[index]


def make_subsequence(sequence, indices):
    return map(partial(at, sequence), indices)


def to_string(characters):
    return ''.join(characters)


def slide_window(sequence, window_length):
    return (sequence[index:index+window_length]
            for index in range(0, (len(sequence)+1)-window_length))


def make_indices(sequence):
    return tuple(range(len(sequence)))


def find_contiguous_ngrams(string, string_indices, ngram_length):
    return ((first(ngram_indices), last(ngram_indices),
        to_string(make_subsequence(string, ngram_indices)).lower())
        for ngram_indices in slide_window(string_indices, ngram_length))


def find_contiguous_trigrams(string):
    return find_contiguous_ngrams(string, make_indices(string), 3)


def find_nonoverlapping_ngrams(string, ngram_length):
    ngrams = tuple(find_contiguous_ngrams(string, make_indices(string),
        ngram_length))
    ngram_groups = ((ngrams[index]
        for index in range(group_index, len(ngrams), ngram_length))
        for group_index in range(ngram_length))
    return ngram_groups


def find_nonoverlapping_trigrams(string):
    return find_nonoverlapping_ngrams(string, 3)


