statically
==========

Compiles a function or class with `Cython <http://www.cython.org>`_. Use annotations for static type declarations.

Python 3.5+ is required.

To compile, you must decorate the function or class with ``typed``. Example: ::

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

Python 3.5 or less supports type hints in the parameters but not in the body
of the code. Read the next case: ::

    @statically.typed
    def sum_powers(x: cython.int):
        return sum([x**n for n in range(1, x + 1)])


Works, but provides just a 5% increase in speed over the Python equivalent
because the `n` variable is not annotated. In this case you can declare
the type of the variable in the parameter with a default value. ::

    @statically.typed
    def sum_powers(x: cython.int, n: cython.int = 0):
        return sum([x**n for n in range(1, x + 1)])

For this function I got more than 1,400% speed increase.

Installation
------------

    $ pip install git+https://github.com/AlanCristhian/statically.git

Caveats
-------

- Async generators are not supported.
- Won't work with IDLE or REPL. Instead it works with `IPython shell <http://ipython.readthedocs.io/en/stable/>`

Contribute
----------

I am not a native english speaker, so you can help me with the documentation.
Also I am not convinced about the module name. The `typed` decorator can
compile functions or classes without type declarations.

Feel free to send me a pull request or open an issue.
