import re

phone_number = "123-456-7890"
pattern = r"^\d{3}-\d{3}-\d{4}$"
if re.match(pattern, phone_number):
    print("Valid phone number.")
else:
    print("Invalid phone number.")


import re

string = "Visit Microsoft!"
pattern = r"Microsoft"
newstring = re.sub(pattern, "OpenAI", string)
print(newstring)


string = "The rain in Spain"
pattern = r"\s"  # Split based on whitespace
result = re.split(pattern, string)
print(result)


pattern = r"Python"
string = "I love Python programming."
match = re.search(pattern, string)

if match:
    print("Pattern found!")
else:
    print("Pattern not found.")


string = "Python programming"
# Match at the beginning
if re.match(r"^Python", string):
    print("String starts with 'Python'")

# Match at the end
if re.search(r"programming$", string):
    print("String ends with 'programming'")



string = "Python3, PyCon, PyQt, PyLadies"
pattern = r"Py[a-zA-Z]+"
matches = re.findall(pattern, string)
print(matches)

listddd = ["Py[a-zA-Z]+",



dicterexg = {"validphone : r"^\d{3}-\d{3}-\d{4}$" ,
             "email": "[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,"}
}  
