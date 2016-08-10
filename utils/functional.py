from functools import partial, reduce
from itertools import chain


def all_of(iterable, predicate):
    def update_condition(condition, element):
        return condition and predicate(element)
    initial_condition = True
    return reduce(update_condition, iterable, initial_condition)


def cons(*elements):
    return tuple(elements)


def thread_values(key, values_of_key):
    for value in values_of_key:
        yield cons(key, value)


def thread_value_sequences(key, value_sequences_of_key):
    for value_sequence in value_sequences_of_key:
        yield cons(key, *value_sequence)


def ungroupby(keys, value_sequences_of_keys):
    return chain.from_iterable((
        thread_value_sequences(key, value_sequences_of_key)
        for key, value_sequences_of_key
        in zip(keys, value_sequences_of_keys)))


def make_nth(index):
    return lambda sequence: sequence[index]


def is_empty(sequence):
    return len(sequence) == 0


def first(sequence):
    return sequence[0]


def rest(sequence):
    return sequence[1:]


def last(sequence):
    return sequence[-1]


def empty():
    return tuple()


def at(sequence, index):
    return sequence[index]


