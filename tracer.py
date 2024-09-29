"""A decorator that traces calls/returns of a recursive function.

Usage:
  from tracer import trace

  @trace()
  def my_recursive_function(m, n):
      ...

Calls and returns of my_recursive_function will be written to the standard error stream.

Limitations:  Not suitable for multi-threaded programs or anything else without a simple
call-return structure on a single stack.  For example, may be a mess with generators.
"""

import sys
from functools import wraps


def trace(log_to=sys.stderr, call_stack = []):
    """Use as @trace() or @trace(SEPARATE_STACK).
    Returns a decorator that shows call-stack at entry
    and just before return.
    Note call_stack will be aliased in traces of different functions
    (intentionally!) unless a different output stream is specified.
    """
    def trace_wrapper(func):
        # FIXME: Should we associate a different call-stack with each output destination?
        @wraps(func)
        def trace_guts(*args, **kwargs):
            nonlocal call_stack
            nonlocal log_to
            level = len(call_stack)
            arg_vals = ", ".join(str(arg) for arg in args)
            called_like = f"{func.__name__}({arg_vals})"
            if level > 0:
                print("|   " * (level - 1) + "|---", file=log_to, end="")
            print(f"{called_like}", file=log_to)
            call_stack.append(called_like)  # On entry
            retval = func(*args, **kwargs)
            call_stack.pop() # On exit
            if level > 0:
                print("|   " * level, file=log_to, end="")
            print(f"{retval}", file=log_to)
            return retval
        return trace_guts
    return trace_wrapper


@trace()
def fact(n: int) -> int:
    if n > 1:
        return n * fact(n-1)
    else:
        return 1

@trace()
def gcd(m: int, n: int) -> int:
    if n > 0:
        return gcd(n, m % n)
    return m

@trace()
def fib(m: int) -> int:
    if m > 1:
        return fib(m-1) + fib(m-2)
    else:
        return m

# print(fact(4))
# print()
# print(gcd(18,24))
# print()
if __name__ == "__main__":
    print("Tracing recursive fibonacci(4)")
    print(fib(4))
