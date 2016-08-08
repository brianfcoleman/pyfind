from index.trigram import find_nonoverlapping_trigrams
from utils.functional import all_of, make_nth, thread_values
from utils.functional import cons, first, rest, empty
from functools import partial
from itertools import chain, tee


def find_search_trigram_sequences(search_string):
    get_trigram = make_nth(2)
    return [list(map(get_trigram, group_of_trigrams))
        for group_of_trigrams in find_nonoverlapping_trigrams(search_string)]


def find_sequential_sequences(groups_of_elements, is_sequential_pair):
    def next_group_of_elements(groups_of_elements):
        try:
            return (False, next(groups_of_elements))
        except StopIteration:
            return (True, tuple())

    def do_generate_sequences(sequence, groups_of_elements):
        is_last, group_of_elements = next_group_of_elements(groups_of_elements)
        if is_last:
            yield tuple(reversed(sequence))
        for element, other_groups_of_elements in zip(group_of_elements,
                tee(groups_of_elements, len(group_of_elements))):
            if is_sequential_pair(first(sequence), element):
                yield from do_generate_sequences(cons(element, *sequence),
                        groups_of_elements)

    def generate_sequences(groups_of_elements):
        is_last, first_group_of_elements = next_group_of_elements(
                groups_of_elements)
        for element, other_groups_of_elements in zip(first_group_of_elements,
                tee(groups_of_elements, len(first_group_of_elements))):
            yield from do_generate_sequences((element,),
                    other_groups_of_elements)

    return generate_sequences(iter(groups_of_elements))


def find_sequences(groups_of_elements):
    return find_sequential_sequences(groups_of_elements, lambda a, b: True)


def find_ngram_start_index_sequences(groups_of_ngrams_and_start_indices,
        ngram_length):

    get_start_index = make_nth(1)

    def is_sequential_start_index_pair(ngram_and_start_index,
            next_ngram_and_start_index):
        return get_start_index(next_ngram_and_start_index) >= (
                get_start_index(ngram_and_start_index) + ngram_length)

    return find_sequential_sequences(groups_of_ngrams_and_start_indices,
            is_sequential_start_index_pair)


def find_trigram_start_index_sequences(groups_of_trigrams_and_start_indices):
    return find_ngram_start_index_sequences(
            groups_of_trigrams_and_start_indices, 3)


def find_trigrams_by_file_name_index_sequence(trigrams_and_start_indices,
        indexed_trigrams):
    return (indexed_trigrams[search_trigram][start_index]
            for search_trigram, start_index in trigrams_and_start_indices)


def find_trigram_sequence_by_file_name_index(
        trigrams_by_file_name_index_sequence, file_name_index):
    return tuple((trigrams_by_file_name_index[file_name_index]
            for trigrams_by_file_name_index
            in trigrams_by_file_name_index_sequence))


def find_matching_file_name_indices(trigrams_by_file_name_index_sequence):

    def make_file_name_matcher(file_name_index):
        def matches_file_name(trigrams_by_file_name_index):
            return file_name_index in trigrams_by_file_name_index
        return matches_file_name

    trigrams_by_file_name_index = first(trigrams_by_file_name_index_sequence)
    file_name_indices = trigrams_by_file_name_index.keys()
    return (find_trigram_sequence_by_file_name_index(
        trigrams_by_file_name_index_sequence, file_name_index)
            for file_name_index in file_name_indices
            if all_of(rest(trigrams_by_file_name_index_sequence),
                make_file_name_matcher(file_name_index)))


def expand_matching_file_name_indices(
        sequence_of_groups_of_matching_file_name_indices):
    for groups_of_matching_file_name_indices \
            in sequence_of_groups_of_matching_file_name_indices:
        yield from find_sequences(groups_of_matching_file_name_indices)


def search_indexed_trigrams(indexed_trigrams, search_trigrams):
    if not all_of(search_trigrams,
            lambda search_trigram: search_trigram in indexed_trigrams):
        return empty()
    groups_of_trigrams_by_start_indices = (
            (search_trigram, indexed_trigrams[search_trigram])
            for search_trigram in search_trigrams)
    groups_of_trigrams_and_start_indices = tuple((
            tuple(thread_values(search_trigram,
                trigrams_by_start_indices.keys()))
            for search_trigram, trigrams_by_start_indices
            in groups_of_trigrams_by_start_indices))
    trigrams_and_start_index_sequences = find_trigram_start_index_sequences(
            groups_of_trigrams_and_start_indices)
    trigrams_by_file_name_index_sequences = (
            find_trigrams_by_file_name_index_sequence(
                trigrams_and_start_indices, indexed_trigrams)
            for trigrams_and_start_indices
            in trigrams_and_start_index_sequences)
    for trigrams_by_file_name_index_sequence \
            in trigrams_by_file_name_index_sequences:
        yield from expand_matching_file_name_indices(
                find_matching_file_name_indices(
                        tuple(trigrams_by_file_name_index_sequence)))


def search(index, search_string):
    search_trigram_sequences = find_search_trigram_sequences(search_string)
    file_names, file_paths, contiguous_trigrams = index
    matching_trigrams = chain.from_iterable(
            map(partial(search_indexed_trigrams, contiguous_trigrams),
                search_trigram_sequences))
    return matching_trigrams


