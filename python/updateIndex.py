import os
from collections import OrderedDict
from rich import print
import json
import re

html_start = """<!DOCTYPE html>
<html lang="en">

<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>CTF Arsenal</title>
<link rel="stylesheet" href="css/prism.css">
<link rel="stylesheet" href="css/bootstrap.min.css">
<link rel="stylesheet" href="css/style.css">
</head>

<body class="bg-dark text-light">
<div class="container">
<nav class="navbar navbar-expand-lg navbar-dark border-bottom border-body">
<div class="container-fluid">
<span class="navbar-brand">
<div class="vr">&nbsp;</div>
CTF Arsenal
<div class="vr">&nbsp;</div>
</span>
</div>
</nav>
</div>
<div class="container mt-5">
<div class="row">
<div class="col-md-6 left-side border">
<div class="container p-4">
<div class="accordion accordion-flush" id="accordionFlush">
"""

html_end = """</div>
</div>
</div>
<div class="col-md-6 right-side border">
<div class="container p-4">
  <h4>Installation directory</h4>
  <div class="input-group mb-3">
    <span class="input-group-text" id="basic-addon1">$TOOLS = $HOME/</span>
    <input id="tools-path" type="text" class="form-control" placeholder="Username" aria-label="Username"
      aria-describedby="basic-addon1" value="Tools">
    <button class="btn btn-dark border-white" type="button" onclick="downloadScript()">Generate script</button>
  </div>
  <hr>
  <code id="script-output" style="color:white">
  </code>
</div>
</div>
</div>
</div>
<script src="js/jquery.js"></script>
<script src="js/prism.min.js"></script>
<script src="js/popper.min.js"></script>
<script src="js/bootstrap.bundle.min.js"></script>
<script src="js/buttonPress.js"></script>
<script src="js/search.js"></script>
<script src="js/popovers.js"></script>
</body>

</html>
"""


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


accordion_start = """
<div class="accordion-item bg-dark text-white">
<h2 class="accordion-header bg-dark text-white" id="flush-heading{ACCORDION_NAME}">
<button class="accordion-button collapsed bg-dark text-white border" type="button"
data-bs-toggle="collapse" data-bs-target="#flush-collapse{ACCORDION_NAME}" aria-expanded="false"
aria-controls="flush-collapse{ACCORDION_NAME}">
{ACCORDION_NAME}&nbsp;<span class="badge badge-light bg-light text-dark"><span id="{ACCORDION_CATEGORY}-counter">0</span>/{NUMBER_OF_TOOLS}</span>
</button>
</h2>
<div id="flush-collapse{ACCORDION_NAME}" class="accordion-collapse collapse" data-bs-parent="#accordionFlush" aria-labelledby="flush-heading{ACCORDION_NAME}">
<div class="accordion-body">
<button class="btn btn-success border-white m-1" type="button" onclick="allTools('{ACCORDION_CATEGORY}')">ALL</button>
<button class="btn btn-danger border-white m-1" type="button" onclick="noneTools('{ACCORDION_CATEGORY}')">None</button>
"""

accordion_end = """</div>
</div>
</div>
"""

accordion_data = ""

accordion_button = """<button class="btn btn-dark border-white m-1 tool-class" type="button" onclick="buttonPress(this)" data-name="{TOOL_NAME}" data-category="{ACCORDION_CATEGORY}" data-installation="{INSTALLATION_METHOD}" data-bs-title="{INSTALLATION_METHOD}" data-bs-container="body" data-bs-toggle="popover" data-bs-placement="top" data-bs-trigger="hover" data-bs-content="{TOOL_DESCRIPTION}">{TOOL_NAME}</button>"""

new_html = ""

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
            output = accordion_start.format(
                ACCORDION_NAME=ACCORDION_NAME,
                ACCORDION_CATEGORY=ACCORDION_CATEGORY,
                NUMBER_OF_TOOLS=NUMBER_OF_TOOLS,
            )
            for file in files:
                INSTALLATION_METHOD = file.split(".")[0]
                path = "/".join([root_directory, dirpath, file])
                data = read_json_file(path)
                for TOOL_NAME in data.keys():
                    if re.search(r"\b{}\b".format(re.escape(TOOL_NAME)), new_html):
                        print(f"{TOOL_NAME} already in document {file}")
                    TOOL_DESCRIPTION = descriptions[TOOL_NAME]
                    output += (
                        accordion_button.format(
                            TOOL_NAME=TOOL_NAME, ACCORDION_CATEGORY=ACCORDION_CATEGORY, TOOL_DESCRIPTION=TOOL_DESCRIPTION, INSTALLATION_METHOD=INSTALLATION_METHOD
                        )
                        + "\n"
                    )
            output += accordion_end
            new_html += output
    new_html += html_end
    with open("../index.html", "w") as f:
        f.write(html_start)
        f.write(new_html)
