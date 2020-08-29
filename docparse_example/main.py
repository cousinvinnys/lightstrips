from inspect import getmembers, isfunction, getfullargspec
import module_name

functions = [o for o in getmembers(module_name) if isfunction(o[1])]

for function in functions:
    print(function)
    print(function[1].__name__)
    args = getfullargspec(function[1]).args
    print(f'\tARGS: {args}')
    print(f'\tDOCS: {function[1].__doc__}')
