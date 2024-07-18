#!/usr/bin/env python3

"""Find all files in path, display number of the largest files.
Example: ./FindLargest.py home 50"""


import os
import sys

#ALL_CAPS global names are for constants, which these variables are not.

def main(path, number_of_items):
    file_list = find_files(path)
    sorted_list = sort_list(file_list)
    print_largest(sorted_list, number_of_items)


def size(num, suffix='B'):
#convert bytes to human
    for unit in ['', 'Ki', 'Mi', 'Gi', 'Ti', 'Pi', 'Ei', 'Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def check_user_number(number_of_items):
    '''make sure number_of_items is valid'''
    try:
        number_of_items = int(number_of_items)
        assert number_of_items > 0
        return number_of_items
    except ValueError:
        print('Please enter a positive integer.')
    except AssertionError:
        print('Please enter a number of items greater than 0')
    sys.exit(1) # same as 'quit()' but available in more places. A non-zero exit code is traditional for 'something went wrong'


def check_user_path(path):
    '''make sure path is valid'''
    try:
        assert os.path.isdir(path)
        return path
    except AssertionError:
        print('Please enter a valid path')
    sys.exit(1)


def find_files(path):
    '''find all files recursivly in a given path and save them in a list'''
    file_list = []
    for dirpath, dirnames, filenames in os.walk(path, topdown=False, followlinks=False):
        if not dirpath.startswith(('/proc', '/dev', '/sys', '/run')):
            for files in filenames:
                file_path = os.path.join(dirpath, files)
                if os.path.isfile(file_path):
                    file_list.append((os.path.getsize(file_path), file_path))
    return file_list


def sort_list(file_list):
    sorted_list = sorted(file_list, reverse=True)
    return sorted_list


def print_largest(sorted_list, number_of_items):
    '''print NUMBER_OF_ITEMS of files and their size.'''
    for size_in_bytes, name in sorted_list[:number_of_items]:
        print("File: '%s' \nSize: %s \n" % (name, size(size_in_bytes)))


if __name__ == '__main__':
    if len(sys.argv) < 3:
        #user did not supply enough arguments, print the useage directions.
        print(__doc__)
    else:
        path = check_user_path(sys.argv[1])
        number_of_items = check_user_number(sys.argv[2])
        main(path, number_of_items)
