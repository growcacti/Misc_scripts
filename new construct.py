class Singleton:
    _instance = None  # Keep instance reference

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(Singleton, cls).__new__(cls, *args, **kwargs)
        return cls._instance

# Usage
singleton1 = Singleton()
singleton2 = Singleton()

assert singleton1 is singleton2  # This will pass, as both are the same instance
