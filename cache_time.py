import time
cache = {}


def sum(a, b):
    time.sleep(.4)
    return a+b


def cache_sum(a, b):
    key = (a, b)
    if key in cache:
        return cache[key]
    else:
        cache[key] = sum(a, b)
        return cache[key]

start_time = time.time()
print(cache_sum(4, 5))
print("Time normal sum: %f" % (time.time()-start_time))

start_time = time.time()
print(cache_sum(4, 5))
print("Time cached sum: %f" % (time.time()-start_time))


