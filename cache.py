cache = {}


def set(key, value):
    cache[key] = value


def get(key):
    if key in cache:
        return cache[key]


def delete(key):
    if key in cache:
        cache.pop(key)


def flush():
    cache.clear()