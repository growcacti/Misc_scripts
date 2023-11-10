from collections import Counter
from string import ascii_lowercase


def closeStrings(self, word1: str, word2: str) -> bool:
    """
    Operation 1 allows us to swap any two symbols, so what matters in the end is not the order of them, but how many of each symbol we have. 
    Imagine we have (6, 3, 3, 5, 6, 6) frequencies of symbols, than we need to have the same frequencies for the second string as well. 
    So, we need to check if we have the same elements, but in different order (that is one is anagramm of another). We can do it in 2 ways. 
    We can sort both of them and compare, or we can use Counter again to check if these two lists have the same elements.
    
    Operation 2 allows us to rename our letters, but we need to use the same letters: it means, that set of letters in first and second strings should be the same.
    """
    if len(word1) != len(word2):
        return False

    counts_1 = Counter(word1)
    counts_2 = Counter(word2)

    return set(word1) == set(word2) and Counter(counts_1.values()) == Counter(counts_2.values())


def closeStrings2(self, word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False
    alpha = ascii_lowercase
    counts1 = []
    counts2 = []
    for char in alpha:
        in1, in2 = char in word1, char in word2
        if in1 and in2:
            counts1.append(word1.count(char))
            counts2.append(word2.count(char))
        elif (in2 and not in1) or (in1 and not in2):
            return False
    counts2.sort()
    counts1.sort()
    return counts1 == counts2

def common_ground(s1, s2):
    lst = []
    for w in s2.split():
        if w in s1.split() and w not in lst:
            lst.append(w)
    return ' '.join(lst) if lst else "death"

from typing import Union


def calculate_partial_result(prev_char: str, count: int) -> str:
    return prev_char + (str(count) if count > 1 else '')


def compress(s: str) -> Union[None, str]:
    if not s or s is None:
        return s

    prev_char = s[0]
    count = 0
    result = ''

    for char in s:
        if char == prev_char:
            count += 1
        else:
            result += calculate_partial_result(prev_char, count)
            prev_char = char
            count = 1

    result += calculate_partial_result(prev_char, count)
    return result if len(result) < len(s) else s
def accum(s):
    c, res = 0, []
    for x in [x for x in s]:
        res.append(x * (c +def accum(s):
    c, res = 0, []
    for x in [x for x in s]:
        res.append(x * (c + 1))
        c += 1
    return "-".join([x[0].upper() + x[1:].lower() for x in res])

 1))
        c += 1
    return "-".join([x[0].upper() + x[1:].lower() for x in res])

import re
from functools import reduce

ACRONYMS = {
    'KPI': "key performance indicators",
    'EOD': "the end of the day",
    'TBD': "to be decided",
    'WAH': "work at home",
    'IAM': "in a meeting",
    'OOO': "out of office",
    'NRN': "no reply necessary",
    'CTA': "call to action",
    'SWOT': "strengths, weaknesses, opportunities and threats",
}

ACRONYM_PATTERN = re.compile(r"\b[A-Z]{3,}\b")
CAPITAL_PATTERN = re.compile(r"(?:\. |^)([a-z])")
CAPITAL_FIX = lambda match: "{}".format(match.group(0).upper())


def acronym_buster(message):
    """
    Find the first group of words that is in all caps
    check if it is in the ACRONYMS dict
    if it is, return the first occurrence of the acronym
    else return [acronym] is an acronym. I do not like acronyms. Please remove them from your email.
    :param message: The message to check
    :return: new string with the acronyms replaced with full words
    :rtype:str
    """
    message = reduce(lambda msg, item: msg.replace(*item), ACRONYMS.items(), message)

    try:
        # find all matching groups with .finditer using next and get the first acronym that is not allows
        acronym = next(ACRONYM_PATTERN.finditer(message)).group(0)
        return "{} is an acronym. I do not like acronyms. Please remove them from your email.".format(acronym)
    except StopIteration:
        return CAPITAL_PATTERN.sub(CAPITAL_FIX, message)

    from string import ascii_lowercase


def print_rangoli(size):
    """
    prints alphabet rangoli based on the size given
    :param size the size of the rangoli pattern to print
    :return alphabet rangoli pattern
    :rtype: str
    """
    result = []
    for x in range(size):
        alpha = "-".join(ascii_lowercase[x:size])
        result.append((alpha[::-1] + alpha[1:]).center(4 * size - 3, "-"))
    return "\n".join(result[:0:-1] + result)

def to_alternating_case(string):
    return string.swapcase()
# *-coding:utf8-*
from functools import reduce
from string import ascii_letters

from pymath.primes.is_prime import is_prime_with_re


class Anagrams(object):
    """
    Anagram class to detect anagrams for letters
    """

    def __init__(self):
        pass

    def detect_anagrams(self, word, word_list):
        """
        check to see that each character in the first string actually occurs in the second. If it is possible to
        “checkoff” each character, then the two strings must be anagrams.
        Checking off a character will be accomplished by replacing it with the special Python value None.
        However, since strings in Python are immutable, the first step in
        the process will be to convert the second string to a list.
        Each character from the first string can be checked against the characters in the list and if found,
        checked off by replacement. """
        res, word = [], word.lower()
        for x in word_list:
            if len(word) == len(x.lower()) and word != x.lower():
                if self.is_anagram(word, x.lower()):
                    res.append(x)
        return res

    @staticmethod
    def is_anagram(s1, s2):
        """
        Check if s1 is an anagram of s2
        :param s1: String to check
        :param s2: string to compare to
        :return: Whether the strings are anagrams
        :rtype: bool
        """
        a_list = list(s2)
        pos1 = 0
        flag = True

        while pos1 < len(s1) and flag:
            pos2 = 0
            found = False
            while pos2 < len(a_list) and not found:
                if s1[pos1] == a_list[pos2]:
                    found = True
                else:
                    pos2 += 1

            if found:
                a_list[pos2] = None
            else:
                flag = False

            pos1 += 1

        return flag

    def anagram_count(self, parent, child):
        """
        Counts the number of times the anagram of a child string appears in a parent string
        Obtains the length of the child string and slices the parent string by that length,
        checks if the slices are anagrams and increases the count variable.
        If the child string is longer than parent, string, it returns a 0 automatically
        :return:  Number of times a child anagram string appears in a parent string
        :rtype int
        """
        count = 0
        child_slice = len(child)
        anagram = self.hash_string(child)

        # if the child is longer than the parent, return 0, it does not make sense for child to be > than parent
        if len(child) > len(parent):
            return 0

        # if the child and the parent are exactly the same, return 1
        if child == parent:
            return 1

        # if the child's length is the same as the parent length AND the child and parent are not the same
        # check if it is an anagram
        if len(child) == len(parent) and child != parent:
            if self.is_anagram(child, parent):
                return 1
            else:
                return 0
        for i in range(0, len(parent) - child_slice):
            if self.hash_string(parent[i: i + child_slice]) == anagram:
                count += 1
        return count

    def hash_string(self, word):
        """
        Map ascii letters to prime numbers, then hashes the string
        This is used to check if a parent string has an anagram of a child string.
        Used because hashes will remain unique and will be easier to check against
        :return: The character map for each letter to corresponding prime number
        :rtype int
        """
        # prime number length will depend on ascii_letters length
        char_map = {}
        char_map_zip = zip(ascii_letters, self.generate_primes(len(ascii_letters)))
        for let, prime in char_map_zip:
            char_map[let] = prime
        return reduce(lambda memo, char: memo * char_map[char], word, 1)

    @staticmethod
    def generate_primes(length):
        """
        Generates the prime numbers based on the length of the ascii characters
        :param length, Length of the ascii letters list, which is the length of the prime numbers wanted
        :return: list of prime numbers
        :rtype: list
        """
        # upper bound of search space
        upper_bound = 100
        # result list
        primes = list()

        while len(primes) < length:
            primes += filter(is_prime_with_re, range(upper_bound - 100, upper_bound))
            upper_bound += 100

        return primes[:length]


class AntiVowel(object):
    def __init__(self, text):
        self.text = text

    def anti_vowel(self):
        vowels = {'a', 'e', 'i', 'o', 'u', 'A', 'E', 'I', 'O', 'U'}
        vtext = ''.join(letter for letter in self.text if letter not in vowels)
        return vtext

import binascii


def to_ascii(h):
    encoded = str.encode(h)
    return bytearray.fromhex(bytes.decode(encoded)).decode()


def to_hex(s):
    return str(binascii.hexlify(str.encode(s)))

def autocomplete(input_, dictionary):
    """
    Check if all the letters in the input are alphabetic, remove all letters in input that are not alphabetic
    :param input_: word 'user' is typing
    :param dictionary: dictionary to evaluate
    :return: list of possible matches based on first characters of word, restrict result to 5 matches
    :rtype list
    """
    res = []
    new_input = "".join([let for let in input_ if let.isalpha()])

    for word in dictionary:
        if word.startswith(new_input) or word.startswith(new_input.title()):
            res.append(word)
    return res[0:5]

def clean_string(s):
    if len(s) == 0:
        return s

    q = []

    for idx in range(len(s)):

        if s[idx] != "#":
            q.append(s[idx])
        elif len(q) != 0:
            q.pop()

    return "".join(q)
from typing import List, Generator


def balanced_parens(n: int) -> List[str]:
    """
    Returns a list of parenthesis
    :param n
    :returns list
    """
    return [x for x in generate_all_parens(n)]


def generate_all_parens(n: int) -> Generator:
    def compute_parens(left: int, right: int, s: str):
        if right == n:
            yield s
            return
        if left < n:
            yield from compute_parens(left + 1, right, s + "(")
        if right < left:
            yield from compute_parens(left, right + 1, s + ")")

    yield from compute_parens(0, 0, "")


import re


def hey(what):
    what = what.strip()
    # silence
    if len(what) == 0:
        return "Fine. Be that way!"
    que = r'(\w|\W)+\?$'
    # shouting
    if what.isupper() and not what.islower():
        return 'Whoa, chill out!'
    # question
    if re.match(que, what):
        return 'Sure.'
    # everything else
    else:
        return 'Whatever.'


import re


def caps_counter(word):
    result = {"UPPER CASE": 0, "LOWER CASE": 0}
    for x in word:
        if re.match(r"[A-Z]", x):
            result["UPPER CASE"] += 1
        elif re.match(r'[a-z]', x):
            result['LOWER CASE'] += 1
    return result

class Censor(object):
    def __init__(self, text, word):
        self.word = word
        self.text = text

    def censor(self):
        string_list = self.text.split()
        new_list = []
        new_sent = ""
        for w in string_list:
            if w == self.word:
                new_list.append("*" * len(self.word))
            else:
                new_list.append(w)

            new_sent = " ".join(new_list)
        return new_sent

try:
    from functools import reduce
except ImportError:
    print("No Module named reduce")


def total_characters(word_list):
    """
    Counts the total number of characters in a word list. Accepts a word list where each element
    is a word. Throws an Exception whenever an invalid parameter is used.
    :param word_list: string word list
    :return: total number of characters
    :raises: TypeError
    :rtype: int
    """
    # check for valid parameters
    if word_list is None or not isinstance(word_list, list):
        raise Exception("ParameterError", "Expect input to be a list")

    # create a variable to hold current total
    total_chars = 0

    # perform a loop to check if each element in word list is a string
    for x in range(len(word_list)):
        if isinstance(word_list[x], str):
            total_chars += len(word_list[x])
        else:
            total_chars += 0
    return total_chars


from collections import Counter
from string import ascii_lowercase


def closeStrings(self, word1: str, word2: str) -> bool:
    """
    Operation 1 allows us to swap any two symbols, so what matters in the end is not the order of them, but how many of each symbol we have. 
    Imagine we have (6, 3, 3, 5, 6, 6) frequencies of symbols, than we need to have the same frequencies for the second string as well. 
    So, we need to check if we have the same elements, but in different order (that is one is anagramm of another). We can do it in 2 ways. 
    We can sort both of them and compare, or we can use Counter again to check if these two lists have the same elements.
    
    Operation 2 allows us to rename our letters, but we need to use the same letters: it means, that set of letters in first and second strings should be the same.
    """
    if len(word1) != len(word2):
        return False

    counts_1 = Counter(word1)
    counts_2 = Counter(word2)

    return set(word1) == set(word2) and Counter(counts_1.values()) == Counter(counts_2.values())


def closeStrings2(self, word1: str, word2: str) -> bool:
    if len(word1) != len(word2):
        return False
    alpha = ascii_lowercase
    counts1 = []
    counts2 = []
    for char in alpha:
        in1, in2 = char in word1, char in word2
        if in1 and in2:
            counts1.append(word1.count(char))
            counts2.append(word2.count(char))
        elif (in2 and not in1) or (in1 and not in2):
            return False
    counts2.sort()
    counts1.sort()
    return counts1 == counts2
class ConsecutiveString(object):
    def __init__(self, starr, k):
        self.starr = starr
        self.k = k

    def longest_consec(self):
        result = ""

        if 0 < self.k <= len(self.starr):
            for index in range(len(self.starr) - self.k + 1):
                s = ''.join(self.starr[index:index + self.k])
                if len(s) > len(result):
                    result = s

        return result


def longest_consec(starr, k):
    result = ""
    if 0 < k <= len(starr):
        for index in range(len(starr) - k + 1):
            s = ''.join(starr[index:index + k])
            if len(s) > len(result):
                result = s

    return result

def contain_all_rots(word, word_list):
    """
    Checks if the word_list contains all the rotations of the word
    Returns true if all rotations are found, false otherwise
    If the word is an empty string the function will return True early
    First, gets all possible rotations of the word and checks if all the possible rotations are in the
    word_list
    :param word: The word to check for
    :param word_list: The list of possible rotations for the word
    :return: True if the word_list contains all rotations of the word
    :rtype: bool
    """

    # return early if the string is empty
    if word == "":
        return True
    # get all the rotations of the word
    rotations = word_rotations(word)

    # check if all these rotations are in the word_list
    return set(word_list).issuperset(rotations)


def word_rotations(word):
    """
    Gets all possible rotations of a word and stores them in a list
    checks if a given rotation has already appeared. If so -- the sequence is periodic and you have already discovered
     all distinguishable rotations, so just return the result:
    :param word: The word to check for
    :return: A list of all possible rotations of the word
    :rtype: list
    """
    result = set()
    for mid in range(len(word)):
        rot = word[mid:] + word[:mid]
        if rot in result:
            return result
        else:
            result.add(rot)

    return list(result)

def denumerate(enum_list):
    """
    denumerates a list of tuples into a word
    :param enum_list: list of tuples with the 1st index in the tuple being the position of the letter
    (the 2nd elem)
    :return: a word formed from the 'denumeration' or False if it does not start from 0
    :rtype: str or bool
    """
    try:
        # create a key-value pairing formt the list provided.
        numbers = dict(enum_list)

        # returns the largest key and adds 1 to it
        maximum = max(numbers) + 1

        # creates the string result from the dictionary and a range which will get the keys and return their values
        result = "".join(numbers[x] for x in range(maximum))

        # if the result is alphanumeric and the length is equal to the maximum, return it
        if result.isalnum() and len(result) == maximum:
            return result
    except (KeyError, ValueError, TypeError):
        return False
    return False

def design_door_mat(n, m):
    """
    Designs a door mat given parameters n and m with constrains 5<n<101 and 15<m<303
    >>> design_door_mat(7, 21)
    ---------.|.---------
    ------.|..|..|.------
    ---.|..|..|..|..|.---
    -------WELCOME-------
    ---.|..|..|..|..|.---
    ------.|..|..|.------
    ---------.|.---------
    :param n: height of the mat
    :param m: length of the mat which is always 3 times the length
    :return: a designed door mat as a string with WELCOME at the center
    :rtype: str
    """
    # that each line has a set number of repetitions of '.|.', which are centered, and the rest is filled by '-'.
    # the flag is symmetrical, so if you have the top, you have the bottom by reversing it.
    # You only need to work on n // 2 (n is odd and you need the integer div because the remaining line is the "WELCOME" line).
    # generate 2*i + 1 '.|.', center it, and fill the rest with '-'.
    pattern = [(".|." * (2 * i + 1)).center(m, "-") for i in range(n // 2)]

    # join the pattern with the middle WELCOME line and the pattern reversed
    return "\n".join(pattern + ["WELCOME".center(m, "-")] + pattern[::-1])

# print(design_door_mat(7, 21))
def make_diamond(letter):
    """
    makes a diamond from the given letter
    :return: a diamond
    :rtype: list
    """
    diamond = None

    # count how far the letter is from A and use that as counter
    size = ord(letter.upper()) - ord('A')

    for i in range(size, -1, -1):
        # gets 1 half of the top of the diamond
        half_row = ' ' * i + chr(i + ord('A')) + ' ' * (size - i)

        # gets the bottom half of the diamond
        row = ''.join(half_row[:0:-1]) + half_row

        if diamond:
            diamond = [row] + diamond + [row]
        else:
            diamond = [row]

    return "\n".join(diamond) + "\n"


import re


def extract_hostname(url: str) -> str:
    regex = r'^(?P<scheme>[a-z]+:\/\/)*(?P<www>(www.)*)?(?P<hostname>[a-z\d][a-z\d-]*)?(\.[a-z\d][a-z\d-]*(\/)*[\w]*(\/)*)+?$'
    m = re.match(regex, url)
    return m.group("hostname")
def duplicate_chars(word_one: str, word_two: str): bool:


if len(word_one) != len(word_two):
    return False
return set(word_one) == set(word_two)

class DuplicateEncoder(object):
    def __init__(self, encode):
        self.encode = encode

    def duplicate_encode(self):
        encode = self.encode.lower()
        out = ""
        for x in encode:
            if encode.count(x) == 1:
                out += "("
            else:
                out += ")"
        return out

    def duplicate_encode_v2(self):
        return "".join(["(" if self.encode.lower().count(c) == 1 else ")" for c in self.encode.lower()])


def sc(s):
    ret = []
    for c in s:
        if c.isupper():
            if chr(ord(c) + 32) in s:
                ret.append(c)
        elif c.islower():
            if chr(ord(c) - 32) in s:
                ret.append(c)
    return ''.join(ret)
try:
    from urllib import quote
except ImportError:
    from urllib.parse import quote


def generate_link(user):
    """
    Generates user links based on the user's name
    appends this to base_url
    :param user: the user name
    :return: a user generated link
    :rtype: str
    """
    return "http://www.codewars.com/users/" + quote(user)
greek_alphabet = ('alpha', 'beta', 'gamma', 'delta', 'epsilon', 'zeta', 'eta', 'theta', 'iota', 'kappa', 'lambda',
                  'mu', 'nu', 'xi', 'omicron', 'pi', 'rho', 'sigma', 'tau', 'upsilon', 'phi', 'chi', 'psi', 'omega'
                  )


def greek_comparator(lhs, rhs):
    GREEK_ALPHABET = {alpha: indx for indx, alpha in enumerate(greek_alphabet)}

    return GREEK_ALPHABET[lhs] - GREEK_ALPHABET[rhs]

from functools import reduce
from string import hexdigits


class Hexadecimal(object):
    """
    Class for conversion of hexadecimal characters
    initialized with the hexadecimal string
    """

    def __init__(self):
        pass

    @staticmethod
    def hexa_first_principles(hexadecimal):
        """
        Converts a hexadecimal number represented as a string to its decimal equivalent using first principles
        Checks if the input hexadecimal is not in the hexdigits, raises a value error
        :param hexadecimal: string representation of a hexadecimal
        :return: decimal equivalent of hexadecimal
        :rtype: int
        :raises: ValueError
        """
        hexa = hexadecimal.lower()
        if set(hexa) - set(hexdigits[:len(hexdigits) - 6]):
            raise ValueError("Invalid hexadecimal string")

        # if c in hexdigits[10: len(hexdigits) - 6] is equivalent to abcdef
        # converts each character in hexa to digit
        hex_list = [ord(c) - ord('a') + 10 if c in hexdigits[10: len(hexdigits) - 6] else ord(c) - ord('0')
                    for c in hexa]

        # converts each number in the hex_list to base 16
        return reduce(lambda x, y: x * 16 + y, hex_list, 0)

    @staticmethod
    def hex_built_in(hexadecimal):
        """
        Ordinary conversion using built ins
        :return: decimal equivalent of hexadecimal
        """
        return int(hexadecimal, base=16)

"""
if the number of petals is greater than the length of the list, reduce the number of petals by the length

loop though list, checking if the number of petals is greater than the length of the list
reduce the number of petals by the length of the list after every iteration until the number is less than or equal to
length of the list, in this case: it is either 1-6
return the value at that index
"""


def how_much_i_love_you(nb_petals):
    love = ["I love you", "a little", "a lot", "passionately", "madly", "not at all"]
    while nb_petals > len(love):
        nb_petals -= len(love)
        if nb_petals in range(0, len(love)):
            break
        else:
            continue

    return love[nb_petals - 1]


def how_much_i_love_you_2(nb_petals):
    return ["I love you", "a little", "a lot", "passionately", "madly", "not at all"][nb_petals % 6 - 1]


def is_isogram(word):
    s = word.lower()
    return len(set(s)) == len(s)
def is_isogram(word):
    if word is None or not isinstance(word, (int, float)):
        return False
    s = [c for c in word.lower() if c.isalpha()]
    return len(set(s)) == len(s)


MAX_CHARS = 256


def is_isomorphic(s: str, t: str) -> bool:
    if not s or not t:
        return False

    if len(s) != len(t):
        return False

    marked = [False] * MAX_CHARS
    mapping = [None] * MAX_CHARS

    for x in range(len(t)):
        if not mapping[ord(s[x])]:

            if marked[ord(t[x])]:
                return False

            marked[ord(t[x])] = True

            mapping[ord(s[x])] = t[x]

        elif mapping[ord(s[x])] != t[x]:
            return False

    return True


def is_isomorphic_v2(s: str, t: str) -> bool:
    if not s or not t:
        return False

    if len(s) != len(t):
        return False

    mapping = {}

    for x in range(len(s)):
        if s[x] in mapping:
            if mapping[s[x]] != t[x]:
                return False
        else:
            if t[x] in mapping.values():
                return False
            else:
                mapping[s[x]] = t[x]

    return True


import string


def is_pangram(s):
    return not set(string.lowercase) - set(s.lower())

def length_of_longest_substring(s: str) -> int:
    """
    The most obvious way to do this would be to go through all possible substrings of the string which would result in
    an algorithm with an overall O(n^2) complexity.

    But we can solve this problem using a more subtle method that does it with one linear traversal( O(n)complexity ).

    First,we go through the string one by one until we reach a repeated character. For example if the string is
    “abcdcedf”, what happens when you reach the second appearance of "c"?

    When a repeated character is found(let’s say at index j), it means that the current substring (excluding the
    repeated character of course) is a potential maximum, so we update the maximum if necessary. It also means that the
    repeated character must have appeared before at an index i, where i<j

    Since all substrings that start before or at index i would be less than the current maximum, we can safely start
    to look for the next substring with head which starts exactly at index i+1.
    """
    # creating set to store last positions of occurrence
    seen = {}
    max_length = 0
    # staring the initial window at 0
    start = 0

    for end in range(len(s)):

        # have we seen this element already?
        if s[end] in seen:
            # move the start pointer to position after last occurrence
            start = max(start, seen[s[end]] + 1)

        # update last seen value of character
        seen[s[end]] = end
        max_length = max(max_length, end - start + 1)

    return max_length


class LetterDigitCount(object):
    def __init__(self, sentence):
        self.sentence = sentence

    def counter(self):
        d = {"DIGITS": 0, "LETTERS": 0}
        for x in self.sentence:
            if x.isdigit():
                d["DIGITS"] += 1
            elif x.isalpha():
                d["LETTERS"] += 1
            else:
                pass

        return d
"""
Find the lexicographic permutations of a given list of characters
"""
from itertools import permutations


def lexicographic_permutations(input_, index):
    """
    Finds the lexicographic permutations of a given array of characters
    :param input_: string input
    :type input_ str
    :param index: the index of the lexicographic permutation to return
    :type: int
    :return: List of permutations for the given input
    :rtype: list
    """
    count = 0
    result = ""
    for permutation in permutations(input_, len(input_)):
        count += 1
        if count == index:
            result = permutation
            break

    return "".join(result)


if __name__ == "__main__":
    chars = "".join(map(str, range(0, 10)))
    index = 1000000
    lexi_perms = lexicographic_permutations(chars, index)
    p = lexi_perms[index]
    print(f"The {index}th lexicographic permutation of {chars} is {p}")
def lineup_students(string):
    return sorted(string.split(), key=lambda x: (len(x), x), reverse=True)

# lineup_students = lambda s: sorted(s.split(), key=lambda x: (len(x), x), reverse=True)


def print_logo(thickness, c):
    """
    Prints a given logo given its thickness and the character itself
    :param thickness: an integer representing the thickness
    :param c: the character to print a logo with
    :return: a string with the logo printed out
    :rtype: str
    """
    # Top Cone
    for i in range(thickness):
        print((c * i).rjust(thickness - 1) + c + (c * i).ljust(thickness - 1))

    # Top Pillars
    for i in range(thickness + 1):
        print((c * thickness).center(thickness * 2) + (c * thickness).center(thickness * 6))

    # Middle Belt
    for i in range((thickness + 1) // 2):
        print((c * thickness * 5).center(thickness * 6))

        # Bottom Pillars
    for i in range(thickness + 1):
        print((c * thickness).center(thickness * 2) + (c * thickness).center(thickness * 6))

        # Bottom Cone
    for i in range(thickness):
        print(((c * (thickness - i - 1)).rjust(thickness) + c + (c * (thickness - i - 1)).ljust(thickness)).rjust(
            thickness * 6))


print_logo(5, "H")

def longest_substring_util(s: str, start: int, end: int, k: int) -> int:
    if end < k:
        return 0

    # will hold the occurrences of each character in the string
    # counter = Counter(s)
    count_map = [0] * 26

    # build the count map which will contain the occurrences of each character in the string
    for i in range(start, end):
        count_map[ord(s[i]) - ord('a')] += 1

    # iterate through the string
    for mid in range(start, end):

        # if we find a character that is 'invalid' i.e. the frequency of the character is less than k
        # if counter.get(s[mid]) >= k:
        if count_map[ord(s[mid]) - ord('a')] >= k:
            continue

        # we now have a mid point
        mid_next = mid + 1

        # while mid_next < end and counter.get(s[mid_next]) < k:
        while mid_next < end and count_map[ord(s[mid_next]) - ord('a')] < k:
            mid_next += 1

        left_sub = longest_substring_util(s, start, mid, k)
        right_sub = longest_substring_util(s, mid_next, end, k)

        return max(left_sub, right_sub)

    return end - start


def longest_substring(s: str, k: int) -> int:
    """
    Divide and Conquer is one of the popular strategies that work in 2 phases.

    Divide the problem into subproblems. (Divide Phase).
    Repeatedly solve each subproblem independently and combine the result to solve the original problem. (Conquer Phase)
    We could apply this strategy by recursively splitting the string into substrings and combine the result to find the
    longest substring that satisfies the given condition. The longest substring for a string starting at index start and
     ending at index end can be given by,

    longestSustring(start, end) = max(longestSubstring(start, mid), longestSubstring(mid+1, end))
    Finding the split position (mid)

    The string would be split only when we find an invalid character. An invalid character is the one with a frequency
    of less than k. As we know, the invalid character cannot be part of the result, we split the string at the index
    where we find the invalid character, recursively check for each split, and combine the result.

    Algorithm

    Build the countMap with the frequency of each character in the string s.
    Find the position for mid index by iterating over the string. The mid index would be the first invalid character in
    the string.
    Split the string into 2 substrings at the mid index and recursively find the result.
    To make it more efficient, we ignore all the invalid characters after the mid index as well, thereby reducing the
    number of recursive calls.

    Complexity Analysis

    Time Complexity: O(N^2), where N is the length of string ss. Though the algorithm performs better in most cases,
    the worst case time complexity is still (N ^ 2).

    In cases where we perform split at every index, the maximum depth of recursive call could be O(N). For each
    recursive call it takes O(N) time to build the countMap resulting in O(n ^ 2) time complexity.

    Space Complexity: O(N) This is the space used to store the recursive call stack. The maximum depth of recursive
    call stack would be O(N).

    @param s: String to evaluate for
    @param k: length of the longest substring
    @return: length of longest substring with at most repeating characters of length k
    @rtype int
    """
    return longest_substring_util(s, 0, len(s), k)

def mean(lst):
    nums = [float(i) for i in lst if i.isdigit()]
    strings = "".join([x for x in lst if not x.isdigit()])
    return [sum(nums) / len(nums), strings]

from re import search

receiver = {
    "it": "Roma",
    "design": "Danik",
    "chemistry": "Maxim",
}

letters = {
    "bug": "it",
    "boom": "chemistry",
    "edits": "design"
}


def memesorting(meme):
    full_pattern = r"bug|boom|edits"
    match = search(full_pattern, meme)

    if match:
        group = match.group(0)
        if group == "bug":
            return receiver[letters[group]]
        if group == "boom":
            return receiver[letters[group]]
        if group == "edits":
            return receiver[letters[group]]
    else:
        spelled_word = ""
        words = meme.lower().split(" ")
        for word in words:
            if 'b' in word or 'u' in word or 'g' in word:
                spelled_word += letter

    return receiver.get(letters[spelled_word], "Vlad")


Test.assert_equals(memesorting('This is programmer meme ecause it has bug'), 'Roma')
Test.assert_equals(memesorting('This is also programbur meme gecause it has needed key word'), 'Roma')
Test.assert_equals(memesorting('This is edsigner meme cause it has key word'), 'Danik')
Test.assert_equals(memesorting('This could be chemistry meme but our gey word boom is too late'), 'Roma')
Test.assert_equals(memesorting('This is meme'), 'Vlad')



from collections import Counter


def minimum_deletions(word: str) -> int:
    counter = Counter(word)
    deletions = 0

    counts = [x for x in counter.values()]

    for x in range(len(counts)):
        for y in range(x + 1, len(counts)):
            if counts[x] > 0 and counts[x] == counts[y]:
                count = counts[y]
                counts[y] = count - 1
                deletions += 1
            else:
                break

    return deletions


def min_deletions(s: str) -> int:
    count, result, used = Counter(s), 0, set()

    for character, frequency in count.items():

        while frequency > 0 and frequency in used:
            frequency -= 1
            result += 1

        used.add(frequency)

    return result


"""
Calculates the name scores of each name in the names.txt file
"""
from collections import Iterable, OrderedDict
from string import ascii_lowercase, ascii_uppercase

ALPHABET_UPPER_POSITIONS = {letter: index for index, letter in enumerate(ascii_uppercase, start=1)}
ALPHABET_LOWER_POSITIONS = {letter: index for index, letter in enumerate(ascii_lowercase, start=1)}


def name_scores(names):
    """
    Calculates the scores of each name in the names array/list. This is obtained by first sorting the array of names in
    the list and obtaining the value of each name, an example is COLIN =  3 + 15 + 12 + 9 + 14 = 53, with the example
    provided, this would end up being 1 * 53 = 53. As it is the only name in the list.
    An example:

    >>> name_scores(["COLIN"])
    53

    :param names:
    :type names list
    :return: total of all name scores
    :rtype: int
    """
    # sanity checks, ensure this is an iterable
    if not isinstance(names, Iterable):
        raise ValueError(f"Expected names to be an iterable, instead got {names}")

    # sort the list of names in alphabetical order in place
    names.sort()
    score_board = OrderedDict()

    # check the alphabetical score for each name and the position in the list
    for name in names:
        alphabetical_score = find_alphabetical_score(name)
        position = names.index(name) + 1
        score_board[name] = alphabetical_score * position

    return sum(score_board.values())


def find_alphabetical_score(name):
    """
    Finds the alphabetical score of a name. An example:

    >>> find_alphabetical_score("COLIN")
    53

    Assumption made here is that the name will be uppercase

    :param name: Name of the alphabet
    :type name str
    :return: Alphabetical score of the name
    :rtype: int
    """
    # ascertain that this will get a string
    if name is None or not isinstance(name, str):
        raise ValueError(f"Name should be a string, instead got {name}")

    # if any of the letters in the name is upper
    if any(x for x in name if x.isupper()):
        name = name.upper()
        numbers = [ALPHABET_UPPER_POSITIONS[letter] for letter in name if letter in ALPHABET_UPPER_POSITIONS]
        return sum(numbers)
    else:
        # use lower case
        name = name.lower()
        numbers = [ALPHABET_LOWER_POSITIONS[letter] for letter in name if letter in ALPHABET_LOWER_POSITIONS]
        return sum(numbers)


if __name__ == "__main__":
    file_name = "names.txt"
    with open(file_name) as name_file:
        names_list = name_file.readline().split(",")
    print(f"Name scores for {names_list} is \n {name_scores(names_list)}")
"""
Create a dictionary of the numbers and their names
create a list for the tens, such as 20, 30, 40, 50, 60...
if the number is between 0 and 19, get the dictionary value of that number
For numbers of 20 or larger, use divmod() to get both the number of tens and the remainder:

tens, below_ten = divmod(Number, 10)
Demo:

>>> divmod(42, 10)
(4, 2)

"""

NAMES = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen",
         17: "seventeen", 18: "eighteen", 19: "nineteen"}
NAMES_TWO = ["twenty", "thirty", "forty", "fifty", "sixty", "seventy", "eighty", "ninety"]


def name_that_number(x):
    """
    Names the given number, returns a string version of the number, ie. number in words

    >>> name_that_number(40)
    'forty'

    :param x: Number passed in
    :return: string version of the number, ie. number in words
    :rtype: str
    """
    if x in range(0, 20):
        return NAMES.get(x)
    elif 20 <= x <= 99:
        tens, ones = divmod(x, 10)
        return NAMES_TWO[tens - 2] + " " + NAMES.get(ones) if ones != 0 else NAMES_TWO[tens - 2]
    else:
        return "Number out of range"


"""
Converts a number to octal, decimal and binary equivalents from 1 up to the number(inclusive)
"""


def print_formatted(number):
    """
    formats the given number, returning its decimal equivalent, octal, hexadecimal and binary
    :param number: number to convert to octal, decimal, binary
    :return: String
    :rtype: str
    """
    # define the width
    width = len(bin(number)[2:])
    result = []
    # create a range from 1 up to the number (inclusive)
    for num in range(1, number + 1):
        # for each number convert the number to octal, binary and hexadecimal and add it to a list
        result.append(
            "{} {} {} {}".format(str(num).rjust(width), oct(num)[2:].rjust(width), hex(num)[2:].upper().rjust(width),
                                 bin(num)[2:].rjust(width)))
    # return each output on a new line
    return "\n".join(result)


def print_formatted_2(n):
    results = []

    for i in range(1, n + 1):
        decimal = str(i)
        octal = str(oct(i)[2:])
        hex_ = str(hex(i)[2:]).upper()
        binary = str(bin(i)[2:])

        results.append([decimal, octal, hex_, binary])

    width = len(results[-1][3])  # largest binary number

    for i in results:
        print(*(rep.rjust(width) for rep in i))
import collections
import re


def order(sentence):
    """
    Split the string into a list,
    Loop through it checking if the number in the string is greater than the number in the next string
    if the current string has a number that is less than the next, add it to a result string
    """
    # split the string
    sent_li = sentence.split(" ")
    # stores the words as keys and the digits within words as keys
    word_dict = {}

    for word in sent_li:
        # check for the digit in the word
        for let in word:
            if re.match("[0-9]", let):
                word_dict[let] = word
    # sort the dict by keys and return the values
    result = collections.OrderedDict(sorted(word_dict.items()))
    return " ".join([v for k, v in result.items()])


def order_2(words):
    return ' '.join(sorted(words.split(), key=lambda w: sorted(w)))

class Palindrome(object):
    """
    Palindrome class to handle Palindrome problems
    Notes regarding the implementation of smallest_palindrome and
    largest_palindrome:

    Both functions must take two keyword arguments:
        max_factor -- int
        min_factor -- int, default 0

    Their return value must be a tuple (value, factors) where value is the
    palindrome itself, and factors is an iterable containing both factors of the
    palindrome in arbitrary order.
    """

    def __init__(self):
        pass

    @staticmethod
    def is_palindrome(a):
        return str(a) == str(a)[::-1]

    @staticmethod
    def longest_palindrome(s):
        s, final_str = s.lower(), ""
        if s == "":
            return 0
        else:
            for y, item in enumerate(s):
                for x, _ in enumerate(s):
                    tr = s[y: x + 1]
                    if Palindrome.is_palindrome(tr) and (len(tr) > len(final_str)):
                        final_str = tr

        return len(final_str)

    def palindrome_pairs(self, word_list):
        """
        Loops through the word_list and checks if the current word is a palindrome of any of the preceding words
        or if the preceding words are a palindrome of the current
        :param word_list: list of words to evaluate for palindrome pairs
        :return: list of lists with each list containing the word indices which form a palindrome
        """
        words = [str(word) for word in word_list]

        return [
            [i, j]
            for i, word_i in enumerate(words)
            for j, word_j in enumerate(words)
            if i != j and self.is_palindrome(word_i + word_j)
        ]

    def smallest_palindrome(self, max_factor, min_factor=0):
        """
        Gets the smallest palindrome from the generator and returns the value from the operation
        :param max_factor:Largest factor to evaluate
        :param min_factor: Smallest factor to evaluate
        :return: Smallest palindrome pair product,
        :rtype:int
        """
        return min(self.generate_palindromes(max_factor, min_factor), key=lambda tup: tup[0])

    def largest_palindrome(self, max_factor, min_factor=0):
        """
        Gets the maximum palindromr product from the generator function
        using the key to only fetch the value from the operation
        :param max_factor: The maximum factor or number to use
        :param min_factor: the minimum number to use, which defaults to 0 if there is no input
        :return: Maximum palindrome product from the generator
        :rtype:int
        """
        return max(self.generate_palindromes(max_factor, min_factor), key=lambda tup: tup[0])

    def generate_palindromes(self, max_factor, min_factor):
        """
        Creates 2 ranges one for the minimum factor and another for the maximum factor
        The results for the first one are used to generate a range for the second one
        Then checks if the product from the result of the 2 operations is a palindrome
        Returns only if the product results to a palindrome
        :return: Tuple with the first element as the product(value) and the 2nd element as the palindrome pair that
        make the product(factors)
        :rtype: tuple
        """
        return ((a * b, (a, b))
                for a in range(min_factor, max_factor + 1)
                for b in range(min_factor, a + 1)
                if self.is_palindrome(a * b)
                )

def palindrome_pairs(words):
    words = [str(word) for word in words]

    return [
        [i, j]
        for i, word_i in enumerate(words)
        for j, word_j in enumerate(words)
        if i != j and is_palindrome(word_i + word_j)
    ]


def is_palindrome(a):
    return str(a) == str(a)[::-1]
from string import ascii_lowercase


class Pangram:
    def __init__(self, s):
        self.s = s

    def is_pangram(self):
        return not set(ascii_lowercase) - set(self.s.lower())
def closing_paren(sentence, open_paren_index):
    """

    :param: sentence the sentence to search through
    :param: open_paren_index, index of the opening parenthesis
    """
    open_nested_count = 0
    position = open_paren_index + 1

    while position <= len(sentence):
        char = sentence[position]
        if char == "(":
            open_nested_count += 1
        elif char == ")":
            if open_nested_count == 0:
                return position
            else:
                open_nested_count -= 1
        position += 1

    raise Exception("No closing parenthesis :(")

def pattern(n):
    """
    Perform checks on the number, if 0, return an empty string,
    if 1, return a string literal of 1,
    else,find the range of the numbers and convert each to a string and repeat the string x times will adding to
     another list
    join this list with \n
    """
    return '\n'.join(['1'] + ['1' + '*' * (i - 1) + str(i)
                              for i in range(2, n + 1)]
                     )


from collections import Counter


def replacer(counter: Counter, word: str) -> str:
    for char, count in counter.items():
        for _ in range(count):
            if char.lower() in word.lower():
                i = word.lower().find(char.lower())
                letter = word[i]
                swapped = letter.swapcase()
                word = word.replace(letter, swapped)

    return word


# TODO: still failing tests
def work_on_strings(a: str, b: str) -> str:
    count_a = Counter(a.lower())
    count_b = Counter(b.lower())

    a = replacer(count_b, a)
    b = replacer(count_a, b)

    return a + b

import re


def rake_garden(garden):
    garden_list = garden.split(" ")
    raked = []
    for item in garden_list:
        if not re.match("gravel|rock", item):
            item = "gravel"
            raked.append(item)
        else:
            raked.append(item)
    return " ".join(raked)


VALID = {'gravel', 'rock'}


def rake_garden_2(garden):
    return ' '.join(a if a in VALID else 'gravel' for a in garden.split())

from random import choice


def random_case(sentence):
    """
    Randomly changes the case of the input sentence
    :param sentence: the sentence to randomly change case
    :return: a new string with the cases randomly swapped
    :rtype: str
    """
    return "".join(choice([let.upper(), let.lower()]) for let in sentence)

class RemoveDuplicate(object):
    def __init__(self, strin):
        self.strin = strin

    def remove_duplicate(self):
        """
        split the string to obtain individual word elements, remove duplicate words
        for each word
        loop through characters in string and check if it is not in output string
        if not, add to output string, return the string.
        """
        out = []
        for x in self.strin.lower():
            if x not in out:
                out.append(x)
        return "".join(out)


class RemoveDupSort(object):
    def __init__(self, sentence):
        self.sentence = sentence

    def remover(self):
        words = self.sentence.split(" ")
        return " ".join(sorted(set(words)))


def re_ordering(s):
    """
    Split the string into a list,
    loop through the list, then loop through each word checking if any letter is capital
    if so, obtain the index of the word insert it at the beginning and remove it from old position
    """
    k, reorder = s.split(), ""
    for x in k:
        for y in x:
            if y.isupper():
                ind = k.index(x)
                k.insert(0, k.pop(ind))
    return " ".join(k)
def reverse_words(message):
    message_list = list(message)

    # first we reverse all the characters in the entire message_list
    reverse_characters(message_list, 0, len(message_list) - 1)
    # this gives us the right word order
    # but with each word backwards

    # now we'll make the words forward again
    # by reversing each word's characters

    # we hold the index of the /start/ of the current word
    # as we look for the /end/ of the current word
    current_word_start_index = 0

    for i in range(len(message_list) + 1):

        # found the end of the current word!
        if (i == len(message_list)) or (message_list[i] == ' '):
            reverse_characters(message_list, current_word_start_index, i - 1)

            # if we haven't exhausted the string our
            # next word's start is one character ahead
            current_word_start_index = i + 1

    return ''.join(message_list)


def reverse_characters(message_list, front_index, back_index):
    # walk towards the middle, from both sides
    while front_index < back_index:
        # swap the front char and back char
        message_list[front_index], message_list[back_index] = \
            message_list[back_index], message_list[front_index]

        front_index += 1
        back_index -= 1

    return message_list


def rgb_to_hex(r: int, g: int, b: int) -> str:
    rounder = lambda x: min(255, max(x, 0))
    return ("{:02X}" * 3).format(rounder(r), rounder(g), rounder(b))
import re


def seven_ate9(sevens):
    return re.sub(r"7+9(?=7)", "7", sevens)
from string import ascii_lowercase


def destroyer(input_sets):
    """
    takes in a tuple with 1 or more sets of characters and replaces the alphabet with letters that are in the sets
    First gets the candidates of the alphabets and gets the letters to knock out into a list

    :param input_sets:
    :return: string of letters with the letters in the input sets having been replaced with _
    :rtype: str
    """
    letters_to_knock = []
    candidates = " ".join([let for let in ascii_lowercase])
    result = ""
    for sets in input_sets:
        for char in sets:
            letters_to_knock.append(char)

    for let in candidates:
        if let in letters_to_knock:
            result += "_"
        else:
            result += let

    return result


# alternative
def destroyer_2(input_sets):
    from string import ascii_lowercase as alphabet
    return " ".join(c if c not in set.union(*input_sets) else "_" for c in alphabet)


import re


def order(sentence):
    result, word_list, c = [], sentence.split(), 0
    for word in word_list:
        if re.match(r"[a-zA-Z]+[1-9][a-zA-Z]+|^[1-9][a-zA-Z]+$|[a-zA-Z]+[1-9]$", word):
            for char in word:
                if char.isdigit():
                    digit = int(char)
                    print("Before:", word_list)
                    removed = word_list.pop(c)
                    print("After:", word_list)
                    word_list.insert(digit - 1, word)
                    c += 1

    return " ".join(word_list)

class Swap(object):
    def __init__(self, str_input):
        self.str_input = str_input

    # simple solution
    def swappie(self):
        print("Using for loop")
        out = ""
        for x in self.str_input:
            if x.islower():
                out += x.upper()
            else:
                out += x.lower()
        return out

    # alternative solution using inbuilt
    def swappie_two(self):
        print("Using inbuilt function swapcase()")
        return self.str_input.swapcase()

    # using map
    def swappie_three(self):
        print("Using map function and inbuilt function")
        return "".join(map(str.swapcase, self.str_input))

    # using lambda
    def swappie_four(self):
        print("using lambda function")
        m = lambda x: x.lower() if x.isupper() else x.upper()
        return m(self.str_input)

def tail_swap(word_list):
    """
    Creates a format for the final replacement
    Picks the head and tail for each string in the list via tuple unpacking
    Swaps the tails using the format created.
    :param word_list: The word list with 2 strings which contain exactly 1 colon
    :return: a list with the tails of each string swapped
    :rtype: list
    """
    # create a format for final replacement
    fmt = '{}:{}'.format

    # pick the head and tail for each word in the list
    (head, tail), (head_2, tail_2) = (a.split(':') for a in word_list)

    # return the formatted list
    return [fmt(head, tail_2), fmt(head_2, tail)]

def title_case(title, minor_words=''):
    title = title.capitalize().split()
    minor_words = minor_words.lower().split()
    return ' '.join(word if word in minor_words else word.capitalize() for word in title)
def tower_builder(n_floors):
    return [("*" * (i * 2 - 1)).center(n_floors * 2 - 1)
            for i in range(1, n_floors + 1)]
def truncate_string(sentence, n):
    if n <= 3:
        return sentence[0: n] + "..."
    if len(sentence) > n:
        return sentence[0:n - 3] + "..."
    else:
        return sentence
GIFTS = ['twelve Drummers Drumming',
         'eleven Pipers Piping',
         'ten Lords-a-Leaping',
         'nine Ladies Dancing',
         'eight Maids-a-Milking',
         'seven Swans-a-Swimming',
         'six Geese-a-Laying',
         'five Gold Rings',
         'four Calling Birds',
         'three French Hens',
         'two Turtle Doves',
         'a Partridge in a Pear Tree']

ORDINAL = [None, 'first', 'second', 'third', 'fourth', 'fifth', 'sixth',
           'seventh', 'eighth', 'ninth', 'tenth', 'eleventh', 'twelfth']


def sing():
    return verses(1, 12)


def verse(num):
    # last gift
    gifts = GIFTS[-num:]
    if len(gifts) > 1:
        gifts[:-1] = [", ".join(gifts[:-1])]
    gifts = ", and ".join(gifts)
    return "On the {} day of Christmas my true love gave to me, {}.\n".format(ORDINAL[num], gifts)


def verses(start, stop):
    return "".join(verse(n) + "\n" for n in range(start, stop + 1))



def two_fer(name="you"):
    return f"One for {name}, one for me."
def two_fer(name="you"):
    return f"One for {name}, one for me."

from typing import List


def valid_word(seq: List[str], word: str) -> bool:
    for s in sorted(seq):
        word = word.replace(s, "")

    return len(word) == 0



    words_to_counts = {}


class WordCloudData:
    def __init__(self, input_string):
        self.words_to_counts = {}
        self.populate_words_to_counts(input_string)

    def populate_words_to_counts(self, input_string):
        """
        Iterates over each character in the input string, splitting
        words and passing them to add_word_to_dictionary
        :param: input_string
        """
        current_word_start_index = 0
        current_word_length = 0

        for i, character in enumerate(input_string):

            # if we reacched the end of the string, we check if the last
            # character is a letter and add the last word to our dictionary
            if i == len(input_string) - 1:
                if character.isalpha():
                    current_word_length += 1
                if current_word_length > 0:
                    current_word = input_string[current_word_start_index:
                                                current_word_start_index + current_word_length]
                    self.add_word_to_dictionary(current_word)

            # if we reach a space or emdash, we know we are at the end of a word
            # so we add it to our dictionary and reset our current word
            elif character == " " or character == u'\u2014':
                if current_word_length > 0:
                    current_word = input_string[current_word_start_index:
                                                current_word_start_index + current_word_length]
                    self.add_word_to_dictionary(current_word)
                    current_word_length = 0

            # we want to make sure we split an ellipses so it we get 2 periods in
            # a row we add the current word to our dictionary and reset our current word
            elif character == ".":
                if i < len(input_string) - 1 and input_string[i + 1] == ".":
                    if current_word_length > 0:
                        current_wrd = input_string[current_word_start_index:
                                                   current_word_start_index + current_word_length]
                        self.add_word_to_dictionary[current_word]
                        current_word_length = 0

            # if the character is a letter of an apostrophe, we add it to our current word
            elif character.isalpha() or character == '\'':
                if current_word_length == 0:
                    current_word_start_index = i
                current_word_length += 1

            # if the character is a hyphen, we want to check if it's surrounded by letters
            # if it is we add it to our current word
            elif character == "-":
                if i > 0 and input_string[i - 1].isalpha() and input_string[i + 1].isalpha():
                    if current_word_length == 0:
                        current_word_start_index = i
                    current_word_length += 1

                else:
                    if current_word_length > 0:
                        current_word = input_string[current_word_start_index:
                                                    current_word_start_index + current_word_length]
                        self.add_word_to_dictionary(current_word)
                        current_word_length = 0

    def add_word_to_dictionary(self, word):
        if word in self.words_to_counts:
            self.words_to_counts[word] += 1

        # if a lowercase version is in the dictionary, we know our input word must be uppercase
        # but we only include uppercase words if they are always uppercase, so we just increment
        # the lowercase version count
        elif word.lower() in self.words_to_counts:
            self.words_to_counts[word.lower()] += 1

        # if an uppercase version is in the dictionary, we know our input word must be lowercase
        # since we only include uppercase words if they're always uppercase, we add the lowercase
        # version and give it the uppercase version's count
        elif word.capitalize() in self.words_to_counts:
            self.words_to_counts[word] = 1
            self.words_to_counts[word] += self.words_to_counts[word.capitalize()]
            del self.words_to_counts[word.capitalize()]

        # otherwise, the word is not in the dictionary at all, lowercase or uppercase
        # so, we add it to the dictionary
        else:
            self.words_to_counts[word] = 1



def word_search(query, seq):
    return [x for x in seq if query.lower() in x.lower()] or [str(None)]
def fix_the_meerkat(arr):
    return list(reversed(arr))
import re


def xoxo(stringer):
    """
    check whether the string x or the string o is present, if so, check the count
    else, return false
    """
    stringer = stringer.lower()
    if stringer.find("x") != -1 and stringer.find("o") != -1:
        return stringer.count("x") == stringer.count("o")
    return False


def xoxo_reg(stringer):
    X = re.findall(r'(o)(x)(o)|\s+(X|x)\s+', stringer, re.IGNORECASE)
    O = re.findall(r"(x)(o|O)(x)|\s+(O|o)\s+", stringer, re.IGNORECASE)
    return len(X) == len(O)

def zebulans_nightmare(functionName):
    # replace the underscore with a space to create separate words and split them into a list
    fn = functionName.replace("_", " ").split()
    f_let = ""
    # add first element to a new list
    out = [fn[0]]
    # take only the 2nd and consecutive elements
    for i in fn[1:]:
        # capitalize the first letter only of each word
        f_let = i.title()
        # add each new word to the list
        out.append(f_let)
    # return this new list
    return "".join(out)


print(zebulans_nightmare("goto_next_kata"))





