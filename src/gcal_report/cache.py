import json

from gcal_report import settings


_cache = {}


def has(key):
    return key in _cache


def get(key, default=None):
    return _cache.get(key, default)


def set(key, value):
    _cache[key] = value


def update():
    global _cache
    # TODO: move filename to config
    with open(settings.CACHE_FILE, 'w') as _file:
        _file.write(json.dumps(_cache))


def load():
    global _cache
    try:
        with open(settings.CACHE_FILE, 'r') as _file:
            _cache = json.load(_file)
            assert type(_cache) == dict
    except IOError as e:
        print e
