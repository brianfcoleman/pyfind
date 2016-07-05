from os.path import expanduser, expandvars
from os.path import join, normpath


def normalize_path(path):
    return normpath(expandvars(expanduser(path)))
