"""
This module contains custom descriptors for the simulation.
"""

class NonNegative:
    """A descriptor that ensures a value is a non-negative number."""
    def __set_name__(self, owner, name):
        self.private_name = '_' + name

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return getattr(obj, self.private_name)

    def __set__(self, obj, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Value must be a number.")
        if value < 0:
            raise ValueError("Value cannot be negative.")
        setattr(obj, self.private_name, value)
