import xml.etree.ElementTree as ET

def execute_task(task):
    if task.get('name') == 'printMessage':
        message = task.find('message').text
        print(message)
    elif task.get('name') == 'calculate':
        operation = task.find('operation').text
        operand1 = int(task.find('operand1').text)
        operand2 = int(task.find('operand2').text)
        
        if operation == 'addition':
            print(f"Result: {operand1 + operand2}")
        # Extend this block for more operations

def main(filename):
    tree = ET.parse(filename)
    root = tree.getroot()

    for task in root.findall('task'):
        execute_task(task)

main('tasks.xml')

import xml.etree.ElementTree as ET

def print_xml_element(element, indent=''):
    """
    Recursively prints the XML elements, attributes, and text content in a human-readable format.
    """
    # Construct a string with the element's tag name and its attributes (if any)
    attributes = ", ".join([f'{k}="{v}"' for k, v in element.attrib.items()])
    tag_info = f'{element.tag} ({attributes})' if attributes else element.tag
    
    # Print the current element with indentation to show its level in the tree
    print(f"{indent}{tag_info}")
    
    # If the element contains text, print it with additional indentation
    if element.text and element.text.strip():
        print(f"{indent}  Text: {element.text.strip()}")
    
    # Recursively process each child of the current element
    for child in element:
        print_xml_element(child, indent + '  ')

def read_and_print_xml(filename):
    """
    Loads an XML file, parses it, and prints its content in a human-readable format.
    """
    # Parse the XML file
    tree = ET.parse(filename)
    root = tree.getroot()

    # Start the recursive printing from the root element
    print_xml_element(root)

# Example usage
filename = 'example.xml'  # Replace with the path to your XML file
read_and_print_xml(filename)
import xml.etree.ElementTree as ET

def print_xml_element(element, indent=''):
    """
    Recursively prints the XML elements, attributes, and text content in a human-readable format.
    """
    # Construct a string with the element's tag name and its attributes (if any)
    attributes = ", ".join([f'{k}="{v}"' for k, v in element.attrib.items()])
    tag_info = f'{element.tag} ({attributes})' if attributes else element.tag
    
    # Print the current element with indentation to show its level in the tree
    print(f"{indent}{tag_info}")
    
    # If the element contains text, print it with additional indentation
    if element.text and element.text.strip():
        print(f"{indent}  Text: {element.text.strip()}")
    
    # Recursively process each child of the current element
    for child in element:
        print_xml_element(child, indent + '  ')

def read_and_print_xml(filename):
    """
    Loads an XML file, parses it, and prints its content in a human-readable format.
    """
    # Parse the XML file
    tree = ET.parse(filename)
    root = tree.getroot()

    # Start the recursive printing from the root element
    print_xml_element(root)

# Example usage
filename = 'example.xml'  # Replace with the path to your XML file
read_and_print_xml(filename)
