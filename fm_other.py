import os

# Create a single directory
os.mkdir('path/to/new/directory')

# Create multiple directories (including intermediate directories)
os.makedirs('path/to/multiple/directories')



# Delete a file
os.remove('path/to/file')

# Delete an empty directory
os.rmdir('path/to/directory')

# Delete a non-empty directory
shutil.rmtree('path/to/non_empty_directory')



# Rename a file or directory
os.rename('path/to/source', 'path/to/new_name')



# Move a file or directory
shutil.move('path/to/source', 'path/to/destination')


import shutil

# Copy a file
shutil.copy('path/to/source/file', 'path/to/destination/file')

# Copy a directory recursively
shutil.copytree('path/to/source/directory', 'path/to/destination/directory')





{
    "bookmark1": "path/to/directory1",
    "bookmark2": "path/to/directory2",
    ...
}





import json
import os

class BookmarkManager:
    def __init__(self, bookmark_file='bookmarks.json'):
        self.bookmark_file = bookmark_file
        self.bookmarks = self.load_bookmarks()

    def load_bookmarks(self):
        if not os.path.exists(self.bookmark_file):
            return {}
        with open(self.bookmark_file, 'r') as file:
            return json.load(file)

    def save_bookmarks(self):
        with open(self.bookmark_file, 'w') as file:
            json.dump(self.bookmarks, file, indent=4)

    def add_bookmark(self, name, path):
        self.bookmarks[name] = path
        self.save_bookmarks()

    def remove_bookmark(self, name):
        if name in self.bookmarks:
            del self.bookmarks[name]
            self.save_bookmarks()
        else:
            print(f"Bookmark '{name}' not found.")

    def get_bookmark(self, name):
        return self.bookmarks.get(name, "Bookmark not found.")

    def list_bookmarks(self):
        for name, path in self.bookmarks.items():
            print(f"{name}: {path}")





# Example usage
manager = BookmarkManager()

# Adding bookmarks
manager.add_bookmark("project", "/path/to/project")
manager.add_bookmark("documents", "/path/to/documents")

# Listing bookmarks
manager.list_bookmarks()

# Retrieving a specific bookmark
print(manager.get_bookmark("project"))

# Removing a bookmark
manager.remove_bookmark("documents")





















