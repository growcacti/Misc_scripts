def is_text_file(filepath):
    try:
        # Open the file in text mode and read a portion to check
        with open(filepath, 'r', encoding='utf-8') as file:
            file.read(1024)  # Read the first 1024 bytes
        return True
    except UnicodeDecodeError:
        # If a UnicodeDecodeError occurs, it's likely not a text file
        return False
    except Exception as e:
        # Other exceptions can be handled differently if needed
        print(f"An error occurred: {e}")
        return False

# Example usage
filepath = 'example_file'
if is_text_file(filepath):
    print(f"{filepath} is a text file.")
else:
    print(f"{filepath} is not a text file.")
