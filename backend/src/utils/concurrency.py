from multiprocessing.pool import ThreadPool
from tqdm import tqdm
from typing import List, Callable


def tqdm_thread_pool_map(threads: int, func: Callable, items: List) -> List:
    """Consume a number of desired threads, a function, and a list of items to call the given function on. Return a list of results."""
    with ThreadPool(threads) as pool:
        results = []
        for result in tqdm(pool.imap(func, items), total=len(items)):
            results.append(result)

        return results
