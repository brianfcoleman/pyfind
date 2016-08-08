from index.trigram import find_contiguous_trigrams
from os.path import basename
from itertools import groupby
from utils.functional import make_nth, ungroupby


def first(elements):
    return elements[0]


def find_file_names_and_paths(file_paths):
    return ((basename(file_path), file_path) for file_path in file_paths)


def group_file_names_and_paths(file_paths):
    file_names_and_paths = sorted(find_file_names_and_paths(file_paths), key=first)
    return ((file_name, sorted(file_paths))
            for file_name, file_paths in groupby(file_names_and_paths, first))


def find_file_name_trigrams(file_names, make_trigrams):
    return (tuple(make_trigrams(file_name)) for file_name in file_names)


def is_empty(sequence):
    return len(sequence) == 0


def first(sequence):
    return sequence[0]


def rest(sequence):
    return sequence[1:]


def make_multilevel_map(elements, key_getters):
    def make_map(elements, get_key, key_getters):
        if is_empty(key_getters):
            return dict((
                (key, tuple(values))
                for key, values in groupby(
                    sorted(elements, key=get_key), get_key)))
        else:
            return dict((
                (key, make_map(values, first(key_getters), rest(key_getters)))
                for key, values in groupby(
                    sorted(elements, key=get_key), get_key)))

    return make_map(elements, first(key_getters), rest(key_getters))


def map_file_name_trigrams(file_name_trigrams):
    get_trigram = make_nth(3)
    get_trigram_start_index = make_nth(1)
    get_file_name = make_nth(0)

    key_getters = (get_trigram, get_trigram_start_index, get_file_name)

    return make_multilevel_map(file_name_trigrams, key_getters)


def make_trigram_index(file_names, trigrams):
    file_name_ids = range(len(file_names))
    file_name_trigrams = ungroupby(file_name_ids, trigrams)
    return map_file_name_trigrams(file_name_trigrams)


def make_index(file_paths):
    file_names_and_paths = tuple(group_file_names_and_paths(file_paths))
    file_names = [file_name for file_name, _ in file_names_and_paths]
    file_paths = [file_path for _, file_path in file_names_and_paths]
    contiguous_trigrams = tuple(find_file_name_trigrams(file_names,
            find_contiguous_trigrams))
    contiguous_trigrams = make_trigram_index(file_names,
            contiguous_trigrams)
    return (file_names, file_paths, contiguous_trigrams)


