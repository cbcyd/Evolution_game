from dataclasses import field

class CellMeta(type):
    """
    A metaclass that automatically adds 'x', 'y', and 'is_alive' attributes
    to any class that uses it. This is for use with the @dataclass decorator.
    """
    def __new__(cls, name, bases, namespace):
        if '__annotations__' not in namespace:
            namespace['__annotations__'] = {}

        # Add annotations for the dataclass
        namespace['__annotations__']['x'] = int
        namespace['__annotations__']['y'] = int
        namespace['__annotations__']['is_alive'] = bool

        # Add the fields themselves. These will be picked up by @dataclass.
        # We provide default values.
        namespace['x'] = 0
        namespace['y'] = 0
        namespace['is_alive'] = field(default=True, init=False)

        return super().__new__(cls, name, bases, namespace)
