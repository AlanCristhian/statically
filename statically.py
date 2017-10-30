import inspect
import sys
import warnings

import cython


__all__ = ["typed"]
__version__ = "1.0a1"


# async generators only present in Python 3.6+
has_async_gen_fun = (3, 6) <= sys.version_info[:2]


def _get_source_code(obj):
    if inspect.isclass(obj):
        lines = inspect.getsourcelines(obj)[0]
        extra_spaces = lines[0].find("class")
        return "".join(l[extra_spaces:] for l in lines)
    elif callable(obj):
        lines = inspect.getsourcelines(obj)[0]
        extra_spaces = lines[0].find("@")
        return "".join(l[extra_spaces:] for l in lines[1:])
    else:
        message = "Function or class expected, got {}.".format(type(obj).__name__)
        raise TypeError(message)


def _get_non_local_scopes(frame):
    while frame:
        yield frame.f_locals
        frame = frame.f_back


def _get_outer_variables(obj):
    frame = inspect.currentframe().f_back
    non_local_scopes = _get_non_local_scopes(frame)
    non_local_variables = list(obj.__code__.co_freevars)
    variables = {}
    for scope in non_local_scopes:
        for name in non_local_variables:
            if name in scope:
                variables[name] = scope[name]
                non_local_variables.remove(name)
        if not non_local_variables:
            break
    return variables


def typed(obj):
    """Compiles a function or class with cython.

    Use annotations for static type declarations. Example:

        import statically

        @statically.typed
        def add_two(x: int) -> int:
            two: int = 2
            return x + two
    """
    if has_async_gen_fun and inspect.isasyncgenfunction(obj):
        raise TypeError("Async generator funcions are not supported.")
    source = _get_source_code(obj)
    frame = inspect.currentframe().f_back
    if inspect.isclass(obj):
        locals_ = frame.f_locals
    else:
        locals_ = _get_outer_variables(obj)
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        compiled = cython.inline(source, locals=locals_,
                                 globals=frame.f_globals, quiet=True)
        return compiled[obj.__name__]
