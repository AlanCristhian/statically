# statically

Compiles a function or class with [Cython](https://www.cython.org). Use annotations for static type
declarations.

Python 3.6+ is required.

To compile, you must decorate the function or class with `typed`. Example:

```python
import cython
import statically

@statically.typed
def func():
    # Cython types are evaluated as for cdef declarations
    x: cython.int               # cdef int x
    y: cython.double = 0.57721  # cdef double y = 0.57721
    z: cython.float  = 0.57721  # cdef float z  = 0.57721

    # Python types shadow Cython types for compatibility reasons
    a: float = 0.54321          # cdef double a = 0.54321
    b: int = 5                  # cdef object b = 5
    c: long = 6                 # cdef object c = 6

@statically.typed
class A:
    a: cython.int
    b: cython.int
    def __init__(self, b=0):
        self.a = 3
        self.b = b
```

## Installation

```shell
$ pip install git+https://github.com/AlanCristhian/statically.git
```

## Caveats

- Async generators are not supported.
- Won't work with IDLE, neither with REPL.

## Help me

I am not a native english speaker, so you can help me with the documentation.
Also I am not convinced about the module name. The `typed` decorator can
compile functions or classes without type declarations.

Feel free to send me a pull request or open an issue.
