from itertools import combinations, islice
from functools import partial
from re import finditer
from utils.functional import all_of, first, last, at


def slide_window(sequence, window_length):
    return ((index, (index+window_length), sequence[index:index+window_length])
            for index in range(0, (len(sequence)+1)-window_length))


def find_contiguous_ngrams(string, ngram_length):
    return ((start, end, ngram.lower())
        for start, end, ngram in slide_window(string, ngram_length))


def find_contiguous_trigrams(string):
    return find_contiguous_ngrams(string, 3)


def find_nonoverlapping_ngrams(string, ngram_length):
    ngrams = tuple(find_contiguous_ngrams(string, ngram_length))
    ngram_groups = ((ngrams[index]
        for index in range(group_index, len(ngrams), ngram_length))
        for group_index in range(ngram_length))
    return ngram_groups


def find_nonoverlapping_trigrams(string):
    return find_nonoverlapping_ngrams(string, 3)


