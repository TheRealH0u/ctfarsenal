import os
from collections import OrderedDict
from rich import print
import json
import re


def traverse_directory(root_dir):
    file_structure = {}

    for dirpath, dirnames, filenames in os.walk(root_dir):
        relative_path = os.path.relpath(dirpath, root_dir)

        sorted_filenames = sorted(filenames)
        if relative_path not in file_structure:
            file_structure[relative_path] = []
        file_structure[relative_path].extend(sorted_filenames)

        for filename in sorted_filenames:
            file_path = os.path.join(dirpath, filename)

    ordered_file_structure = OrderedDict(sorted(file_structure.items()))
    return ordered_file_structure


def read_json_file(filepath):
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
            return data
    except FileNotFoundError:
        print(f"File not found: {filepath}")
    except json.JSONDecodeError:
        print(f"Error decoding JSON from the file: {filepath}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def getNumberOfTools(path):
    files = traverse_directory(path).values()
    length = 0
    for values in files:
        for file in values:
            data = read_json_file(f"{path}/{file}")
            length += len(data)
    return length

if __name__ == "__main__":
    descriptions = read_json_file("descriptions.json")
    root_directory = "../tools"
    structure = traverse_directory(root_directory)
    for dirpath, files in structure.items():
        if len(files) > 0:
            ACCORDION_CATEGORY = dirpath
            ACCORDION_NAME = ACCORDION_CATEGORY.capitalize()
            NUMBER_OF_TOOLS = getNumberOfTools(f"{root_directory}/{dirpath}")
            for file in files:
                INSTALLATION_METHOD = file.split(".")[0]
                path = "/".join([root_directory, dirpath, file])
                data = read_json_file(path)
                for TOOL_NAME, INSTALLATION in data.items():                    
                    # Find the SSH URL part in the string
                    start = INSTALLATION.find("https://github.com")
                    end = INSTALLATION.find(".git", start)

                    # Extract the SSH URL
                    URL = INSTALLATION[start:end]
                    print(f"|{TOOL_NAME}|{URL}|")