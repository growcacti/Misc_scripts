class ImmutablePoint:
    def __new__(cls, x, y):
        # Create the instance
        instance = super(ImmutablePoint, cls).__new__(cls)
        # Set attributes (since __init__ can't modify an immutable instance)
        instance._x = x
        instance._y = y
        return instance

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

# Using the immutable class
point = ImmutablePoint(3, 4)
print(point.x)  # Output: 3
print(point.y)  # Output: 4
