import os
import shutil
from pathlib import Path
import glob

# Create a new directory
os.mkdir('new_directory')

# Move into the new directory
os.chdir('new_directory')

# Create a new file
Path('test_file.txt').touch()

# List all txt files in the current directory
print(glob.glob('*.txt'))

# Move the file to a new location
shutil.move('test_file.txt', '../test_file_moved.txt')

# Change back to the parent directory and remove the newly created directory and file
os.chdir('..')
os.remove('test_file_moved.txt')
shutil.rmtree('new_directory')
