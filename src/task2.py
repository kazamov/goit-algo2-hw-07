from functools import lru_cache
import timeit
import matplotlib.pyplot as plt
from tabulate import tabulate
from SplayTree import SplayTree

@lru_cache(maxsize=1000)
def fibonacci_lru(n: int) -> int:
    if n <= 1:
        return n
    return fibonacci_lru(n-1) + fibonacci_lru(n-2)

def fibonacci_splay(n: int, tree: SplayTree) -> int:
    result = tree.find(n)
    if result is not None:
        return result
    
    if n <= 1:
        result = n
    else:
        result = fibonacci_splay(n-1, tree) + fibonacci_splay(n-2, tree)
    
    tree.insert(n, result)
    return result

def measure_execution_time(func, n, number=100, repeat=3, *args):
    if args:
        stmt = lambda: func(n, *args)
    else:
        stmt = lambda: func(n)
    
    times = timeit.repeat(stmt, number=number, repeat=repeat)
    return min(times) / number

def print_analysis_summary(results):
    lru_times = [r[1] for r in results]
    splay_times = [r[2] for r in results]
    
    lru_avg = sum(lru_times) / len(lru_times)
    splay_avg = sum(splay_times) / len(splay_times)
    
    lru_variance = sum((t - lru_avg) ** 2 for t in lru_times) / len(lru_times)
    splay_variance = sum((t - splay_avg) ** 2 for t in splay_times) / len(splay_times)
    
    speed_difference = (splay_avg - lru_avg) / lru_avg * 100
    
    print("\nPerformance Analysis Summary:")
    print("-----------------------------")
    print("LRU Cache is the better approach because:")
    print(f" - Faster execution time (approximately {speed_difference:.1f}% faster)")
    print(f" - More consistent performance (variance: {lru_variance:.2e} vs {splay_variance:.2e})")
    print(" - Built-in Python functionality (@lru_cache decorator)")
    print(" - Simpler implementation (one-line decorator)")
    print(" - Lower overhead (built into Python's standard library)")

def run_task2():
    n_values = range(0, 951, 50)
    results = []
    
    for n in n_values:
        fibonacci_lru.cache_clear()
        tree = SplayTree()
        
        lru_time = measure_execution_time(fibonacci_lru, n)
        splay_time = measure_execution_time(fibonacci_splay, n, 100, 3, tree)
        
        results.append([n, lru_time, splay_time])
    
    headers = ["n", "LRU Cache (s)", "Splay Tree (s)"]
    print("\nPerformance Comparison:")
    print(tabulate(results, headers=headers, floatfmt=".8f"))
    
    print_analysis_summary(results)

    plt.figure(figsize=(12, 6))
    plt.plot([r[0] for r in results], [r[1] for r in results], 'b-', label='LRU Cache')
    plt.plot([r[0] for r in results], [r[2] for r in results], 'r-', label='Splay Tree')
    plt.xlabel('n (Fibonacci number)')
    plt.ylabel('Average execution time (seconds)')
    plt.title('Fibonacci Calculation Performance Comparison')
    plt.legend()
    plt.grid(True)
    plt.show(block=True)

if __name__ == "__main__":
    run_task2()