class Singleton:
    _instance = None  # This is a class attribute to hold the single instance

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            # Create the single instance if it does not exist
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self, value):
        # Initialize the instance
        self.value = value

# Testing the Singleton pattern
singleton1 = Singleton(10)
singleton2 = Singleton(20)

print(singleton1.value)  # Output: 20
print(singleton2.value)  # Output: 20
print(singleton1 is singleton2)  # Output: True (both variables point to the same instance)
