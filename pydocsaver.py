import io
import contextlib
import pkg_resources
import os
liblist = ['__future__', '__main__', '_thread', '_tkinter', 'abc', 'aifc', 'argparse', 'array', 'ast', 'asyncio', 'atexit', 'audioop', 'base64', 'bdb', 'binascii', 'bisect', 'builtins', 'bz2', 'calendar', 'cgi', 'cgitb', 'chunk', 'cmath', 'cmd', 'code', 'codecs', 'codeop', 'collections', 'colorsys', 'compileall', 'concurrent', 'configparser', 'contextlib', 'contextvars', 'copy', 'copyreg', 'cProfile', 'crypt (Unix)', 'csv', 'ctypes', 'curses (Unix)', 'dataclasses', 'datetime', 'dbm', 'decimal', 'difflib', 'dis', 'doctest', 'email', 'encodings', 'ensurepip', 'enum', 'errno', 'faulthandler', 'fcntl (Unix)', 'filecmp', 'fileinput', 'fnmatch', 'fractions', 'ftplib', 'functools', 'gc', 'getopt', 'getpass', 'gettext', 'glob', 'graphlib', 'grp (Unix)', 'gzip', 'hashlib', 'heapq', 'hmac', 'html', 'http', 'idlelib', 'imaplib', 'imghdr', 'importlib', 'inspect', 'io', 'ipaddress', 'itertools', 'json', 'keyword', 'lib2to3', 'linecache', 'locale', 'logging', 'lzma', 'mailbox', 'mailcap', 'marshal', 'math', 'mimetypes', 'mmap', 'modulefinder', 'msilib (Windows)', 'msvcrt (Windows)', 'multiprocessing', 'netrc', 'nis (Unix)', 'nntplib', 'numbers', 'operator', 'optparse', 'os'," 'ossaudiodev (Linux, FreeBSD)'", 'pathlib', 'pdb', 'pickle', 'pickletools', 'pipes (Unix)', 'pkgutil', 'platform', 'plistlib', 'poplib', 'posix (Unix)', 'pprint', 'profile', 'pstats', 'pty (Unix)', 'pwd (Unix)', 'py_compile', 'pyclbr', 'pydoc', 'queue', 'quopri', 'random', 're', 'readline (Unix)', 'reprlib', 'resource (Unix)', 'rlcompleter', 'runpy', 'sched', 'secrets', 'select', 'selectors', 'shelve', 'shlex', 'shutil', 'signal', 'site', 'sitecustomize', 'smtplib', 'sndhdr', 'socket', 'socketserver', 'spwd (Unix)', 'sqlite3', 'ssl', 'stat', 'statistics', 'string', 'stringprep', 'struct', 'subprocess', 'sunau', 'symtable', 'sys', 'sysconfig', 'syslog (Unix)', 'tabnanny', 'tarfile', 'telnetlib', 'tempfile', 'termios (Unix)', 'test', 'textwrap', 'threading', 'time', 'timeit', 'tkinter', 'token', 'tokenize', 'tomllib', 'trace', 'traceback', 'tracemalloc', 'tty (Unix)', 'turtle', 'turtledemo', 'types', 'typing', 'unicodedata', 'unittest', 'urllib', 'usercustomize', 'uu', 'uuid', 'venv', 'warnings', 'wave', 'weakref', 'webbrowser', 'winreg (Windows)', 'winsound (Windows)', 'wsgiref', 'xdrlib', 'xml', 'xmlrpc', 'zipapp', 'zipfile', 'zipimport', 'zlib', 'zoneinfo'
]

 

def save_module_docs(directory="module_docs"):
    if not os.path.exists(directory):
        os.makedirs(directory)

    for lib in liblist:
        module_name = lib
        try:
            # Attempt to import the module
            __import__(module_name)
        except ImportError:
           
            print(f"Could not import {module_name}, skipping.")
            continue

        with io.StringIO() as buf, contextlib.redirect_stdout(buf):
            try:
                for lib in liblist:
                    help(lib)
                    doc = buf.getvalue()
            except:
                print(f"Could not get help for {module_name}, skipping.")
                continue
        
        # Save the documentation to a file
        filepath = os.path.join(directory, f"{module_name}.txt")
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(doc)
        print(f"Saved documentation for {module_name}")

if __name__ == "__main__":
    save_module_docs()
