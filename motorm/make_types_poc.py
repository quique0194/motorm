class Int():
    pass

def make_type(base_type, invalid_vals: set):
    # see https://www.geeksforgeeks.org/create-classes-dynamically-in-python/
    class TypeClass():
        def __init__(self, val) -> None:
            if type(val) != base_type:
                raise ValueError('Invalid type')
            if val in invalid_vals:
                raise ValueError('Is zero!')
            self.inner = val
    return TypeClass


NonZeroInt = make_type(int, invalid_vals={0})

print(type(1))
print(type(NonZeroInt(1)))

try:
    print(type(NonZeroInt(0)))
except Exception as e:
    print(e)
try:
    print(type(NonZeroInt('a')))
except Exception as e:
    print(e)
