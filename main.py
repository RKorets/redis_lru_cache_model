from collections import OrderedDict
import redis


class LRUCache:

    def __init__(self, capacity: int):
        self.cache = OrderedDict()
        self.capacity = capacity

    def get(self, key: str):
        if key not in self.cache:
            return -1
        else:
            self.cache.move_to_end(key)
            return self.cache[key]

    def put(self, key: str, value) -> None:
        self.cache[key] = value
        self.cache.move_to_end(key)
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)


r = redis.Redis(
    host='localhost',
    port=6379
)

cache_lru = LRUCache(3)  # cache field size


def put_value(key: str, value):
    cache_lru.put(key, value)
    r.delete('cache')
    r.hset('cache', mapping=cache_lru.cache)
    return print(f'Success put {key, value}')


def get_value(key: str):
    cache_lru.get(key)
    result = r.hget('cache', f'{key}')
    return print(result)


if __name__ == '__main__':
    put_value('Usr_1', 'Roma')
    put_value('Usr_2', 'Vova')
    put_value('Usr_3', 'Dima')

    get_value('Usr_1')

    put_value('Usr_4', 'Vadim')

    get_value('Usr_2')  # None

    print(cache_lru.cache)
