import unittest
import asyncio

import cython

import statically


ONE_HUNDRED = 100
execute = asyncio.get_event_loop().run_until_complete


def anext(agen):
    gen = agen.asend(None)
    try:
        gen.send(None)
    except StopIteration as error:
        return error.args[0]


class CompilationSuite(unittest.TestCase):
    def test_function(self):
        @statically.typed
        def identity(x: cython.int):
            return x
        self.assertEqual(identity(14), 14)

    def test_non_local_var_in_class(self):
        one = 1
        @statically.typed
        class Class:
            number = 100 + one
        self.assertEqual(Class.number, 101)

    def test_non_local_var_in_method(self):
        two = 2
        class Class:
            @statically.typed
            def add_two(self, x):
                return x + two
        obj = Class()
        self.assertEqual(obj.add_two(100), 102)

    def test_non_local_var_in_function(self):
        tree = 3
        @statically.typed
        def add_tree(x):
            return x + tree
        self.assertEqual(add_tree(100), 103)

    def test_non_local_var_in_generator_function(self):
        four = 4
        @statically.typed
        def add_four(x):
            yield x + four
        self.assertEqual(next(add_four(100)), 104)

    def test_non_local_var_in_coroutine_function(self):
        five = 5
        @statically.typed
        async def add_five(x):
            return x + five
        self.assertEqual(execute(add_five(100)), 105)

    def test_global_var_in_class(self):
        @statically.typed
        class Class_:
            number = 1 + ONE_HUNDRED
        self.assertEqual(Class_.number, 101)

    def test_global_var_in_method(self):
        class Class:
            @statically.typed
            def add_one_hundred(self, x):
                return ONE_HUNDRED + x
        obj = Class()
        self.assertEqual(obj.add_one_hundred(2), 102)

    def test_global_var_in_function(self):
        @statically.typed
        def add_one_hundred(x):
            return ONE_HUNDRED + x
        self.assertEqual(add_one_hundred(3), 103)

    def test_global_var_in_generator_function(self):
        @statically.typed
        def add_one_hundred(x):
            yield ONE_HUNDRED + x
        self.assertEqual(next(add_one_hundred(4)), 104)

    def test_global_var_in_coroutine_function(self):
        @statically.typed
        async def add_one_hundred(x):
            return ONE_HUNDRED + x
        self.assertEqual(execute(add_one_hundred(5)), 105)

    def test_async_generator(self):
        message = r"Async generator funcions are not supported."
        with self.assertRaisesRegex(TypeError, message):
            @statically.typed
            async def generator():
                yield


if __name__ == '__main__':
    unittest.main()
