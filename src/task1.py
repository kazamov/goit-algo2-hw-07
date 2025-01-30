from LRUCache import LRUCache
from typing import List, Tuple
import random
import time

def range_sum_no_cache(array: List[int], L: int, R: int) -> int:
    return sum(array[L:R+1])

def update_no_cache(array: List[int], index: int, value: int) -> None:
    array[index] = value

def range_sum_with_cache(array: List[int], L: int, R: int, cache: LRUCache) -> int:
    key = ('range', L, R)
    result = cache.get(key)
    if result is None:
        result = sum(array[L:R+1])
        cache.put(key, result)
    return result

def update_with_cache(array: List[int], index: int, value: int, cache: LRUCache) -> None:
    array[index] = value
    # Invalidate all cache entries
    cache.cache.clear()

def generate_test_data(array_size: int, queries_count: int) -> Tuple[List[int], List[Tuple]]:
    array = [random.randint(1, 1000) for _ in range(array_size)]
    queries = []
    
    for _ in range(queries_count):
        if random.random() < 0.8:  # 80% Range queries
            L = random.randint(0, array_size-2)
            R = random.randint(L+1, array_size-1)
            queries.append(('Range', L, R))
        else:  # 20% Update queries
            index = random.randint(0, array_size-1)
            value = random.randint(1, 1000)
            queries.append(('Update', index, value))
            
    return array, queries

def run_task1():
    ARRAY_SIZE = 100_000
    QUERIES_COUNT = 50_000
    CACHE_SIZE = 1000
    
    # Generate test data
    array, queries = generate_test_data(ARRAY_SIZE, QUERIES_COUNT)
    array_with_cache = array.copy()
    cache = LRUCache(CACHE_SIZE)
    
    # Test without cache
    start_time = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_no_cache(array, query[1], query[2])
        else:  # Update
            update_no_cache(array, query[1], query[2])
    time_no_cache = time.time() - start_time
    
    # Test with cache
    start_time = time.time()
    for query in queries:
        if query[0] == 'Range':
            range_sum_with_cache(array_with_cache, query[1], query[2], cache)
        else:  # Update
            update_with_cache(array_with_cache, query[1], query[2], cache)
    time_with_cache = time.time() - start_time
    
    print(f"\nResults:")
    print(f"Time without cache: {time_no_cache:.4f} seconds")
    print(f"Time with cache: {time_with_cache:.4f} seconds")
    print(f"Performance improvement: {((time_no_cache - time_with_cache) / time_no_cache * 100):.2f}%")

if __name__ == "__main__":
    run_task1()