import os
import time

def list_files(directory):
    files_info = []
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            file_info = {
                'name': filename,
                'size': os.path.getsize(filepath),
                'date': time.ctime(os.path.getmtime(filepath)),
                'type': 'File'
            }
        elif os.path.isdir(filepath):
            file_info = {
                'name': filename,
                'size': '-',
                'date': time.ctime(os.path.getmtime(filepath)),
                'type': 'Directory'
            }
        files_info.append(file_info)
    return files_info

def print_files_info(files_info):
    print(f"{'Name':<30} {'Size (bytes)':<15} {'Date Modified':<25} {'Type':<10}")
    print("="*80)
    for file_info in files_info:
        print(f"{file_info['name']:<30} {file_info['size']:<15} {file_info['date']:<25} {file_info['type']:<10}")

directory = '.'  # Change to the directory you want to list
files_info = list_files(directory)
print_files_info(files_info)
