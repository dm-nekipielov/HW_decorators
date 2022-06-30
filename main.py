import functools
import tracemalloc

import requests


def memory_profile(msg: str = "Memory used by "):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            tracemalloc.start()
            result = f(*args, **kwargs)
            small_memory, peak_memory = tracemalloc.get_traced_memory()

            print(msg, f'{f.__name__}({args[0]}): {(peak_memory - small_memory) / 1024 ** 2} MiB')
            return result

        return deco

    return internal


def cache(max_limit: int = 64):
    def internal(f):
        @functools.wraps(f)
        def deco(*args, **kwargs):
            cache_key = (args, tuple(kwargs.items()))
            if cache_key in deco._cache:
                # збільшуємо лічильник запитів
                deco._call_count[cache_key] += 1
                return deco._cache[cache_key]
            result = f(*args, **kwargs)
            # видаляємо якшо досягли ліміта
            if len(deco._cache) >= max_limit:
                # видаляємо елемент з найменшою кількістю запитів
                min_reqs = min(deco._call_count, key=deco._call_count.get)
                deco._cache.pop(min_reqs)
                deco._call_count.pop(min_reqs)
            deco._cache[cache_key] = result
            deco._call_count[cache_key] = 1
            return result

        deco._cache = dict()
        deco._call_count = dict()
        return deco

    return internal


@memory_profile()
@cache(max_limit=30)
def fetch_url(url: str, first_n: int = 100):
    """Fetch a given url"""
    response = requests.get(url)
    return response.content[:first_n] if first_n else response.content


fetch_url("https://www.rozetka.ua/")
fetch_url("https://www.google.com/")
fetch_url("https://www.google.com/")
fetch_url("https://www.google.com/")
fetch_url('https://ithillel.ua')
fetch_url('https://dou.ua')
fetch_url('https://dou.ua')
fetch_url('https://ain.ua')
fetch_url('https://youtube.com')
fetch_url("https://www.rozetka.ua/")
fetch_url("https://www.rozetka.ua/")
fetch_url("https://www.rozetka.ua/")
