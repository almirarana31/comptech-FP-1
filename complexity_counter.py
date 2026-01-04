"""Simple empirical time & memory complexity estimator

Usage:
  - Use `@measure_complexity(input_gen=...)` on functions that accept a single integer-size parameter
  - `input_gen(n)` should return `(args, kwargs)` to call the function

The decorator will run the function for increasing sizes, measure time and memory,
and attempt to match runtime growth to common complexity classes.
"""
from typing import Callable, Iterable, Tuple, Any, Dict
import time
import tracemalloc
import math
import statistics


def _median(xs):
    return statistics.median(xs) if xs else 0.0


def _linear_least_squares(y, x):
    # Fit y ~ a * x  (a scalar)
    num = sum(yi * xi for yi, xi in zip(y, x))
    den = sum(xi * xi for xi in x)
    if den == 0:
        return 0.0
    return num / den


def _rmse(y, y_pred):
    n = len(y)
    if n == 0:
        return float('inf')
    return math.sqrt(sum((yi - ypi) ** 2 for yi, ypi in zip(y, y_pred)) / n)


def _guess_complexity(sizes, times):
    # Candidate basis functions (on sizes)
    funcs = {
        'O(1)': lambda n: 1.0,
        'O(log n)': lambda n: math.log(n + 1),
        'O(n)': lambda n: n,
        'O(n log n)': lambda n: n * math.log(n + 1),
        'O(n^2)': lambda n: n * n,
        'O(n^3)': lambda n: n ** 3,
        'O(2^n)': lambda n: 2 ** n if n < 60 else float('inf'),
    }

    y = times
    best = None
    best_score = float('inf')
    best_pred = None

    for name, f in funcs.items():
        x = [f(n) for n in sizes]
        # normalize x to avoid overflow when possible
        max_x = max(x) if x else 1.0
        if max_x == 0:
            continue
        x_scaled = [xi / max_x for xi in x]
        a = _linear_least_squares(y, x_scaled)
        pred = [a * xi for xi in x_scaled]
        score = _rmse(y, pred)
        if score < best_score:
            best_score = score
            best = name
            best_pred = pred

    return best, best_score


def measure_complexity(input_gen: Callable[[int], Tuple[Tuple[Any, ...], Dict[str, Any]]],
                       sizes: Iterable[int] = (10, 100, 1000, 5000, 10000),
                       repeats: int = 3):
    """Decorator factory.

    input_gen: function that given n returns (args_tuple, kwargs_dict)
    sizes: iterable of sizes to test
    repeats: number of repeats per size (take median)
    """

    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            # If called normally, just execute the function
            return func(*args, **kwargs)

        # attach an analyze method
        def analyze():
            sizes_list = list(sizes)
            results = []

            for n in sizes_list:
                run_times = []
                mem_peaks = []
                for _ in range(repeats):
                    call_args, call_kwargs = input_gen(n)
                    # merge wrapper args (if used) - but we favor generator-provided args
                    # Measure time and memory
                    tracemalloc.start()
                    t0 = time.perf_counter()
                    try:
                        func(*call_args, **call_kwargs)
                    except Exception:
                        # if the function raises for too large N, record as inf
                        t0 = None
                    t1 = time.perf_counter()
                    current, peak = tracemalloc.get_traced_memory()
                    tracemalloc.stop()

                    if t0 is None:
                        run_times.append(float('inf'))
                    else:
                        run_times.append(t1 - t0)
                    mem_peaks.append(peak / 1024.0)  # KB

                median_time = _median(run_times)
                median_mem = _median(mem_peaks)
                results.append((n, median_time, median_mem))

            sizes_vals = [r[0] for r in results]
            times_vals = [r[1] for r in results]

            guess, score = _guess_complexity(sizes_vals, times_vals)

            out = {
                'results': results,
                'estimated_complexity': guess,
                'fit_score': score,
            }
            return out

        wrapper.analyze = analyze
        return wrapper

    return decorator
