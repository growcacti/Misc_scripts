class MyDict:
    def __init__(self):
        self.data = {}

    def __getitem__(self, key):
        return self.data[key]

    def __setitem__(self, key, value):
        self.data[key] = value

    def __delitem__(self, key):
        del self.data[key]

    def __repr__(self):
        return str(self.data)

# Using the class
d = MyDict()
d['key1'] = 'value1'
print(d['key1'])  # value1
del d['key1']
print(d)  # {}
