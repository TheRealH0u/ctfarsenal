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

<body class="text-light">
  <a href="https://github.com/TheRealH0u/ctfarsenal" class="github-corner"
    aria-label="View source on GitHub"><svg width="80" height="80"
      style="fill:#fff;color:#151513;position:absolute;top:0;border:0;right:0" aria-hidden="true" viewBox="0 0 250 250">
      <path d="m0 0 115 115h15l12 27 108 108V0Z"></path>
      <path
        d="M128.3 109c-14.5-9.3-9.3-19.4-9.3-19.4 3-6.9 1.5-11 1.5-11-1.3-6.6 2.9-2.3 2.9-2.3 3.9 4.6 2.1 11 2.1 11-2.6 10.3 5.1 14.6 8.9 15.9"
        fill="currentColor" style="transform-origin:130px 106px" class="octo-arm"></path>
      <path
        d="M115 115c-.1.1 3.7 1.5 4.8.4l13.9-13.8c3.2-2.4 6.2-3.2 8.5-3-8.4-10.6-14.7-24.2 1.6-40.6 4.7-4.6 10.2-6.8 15.9-7 .6-1.6 3.5-7.4 11.7-10.9 0 0 4.7 2.4 7.4 16.1 4.3 2.4 8.4 5.6 12.1 9.2 3.6 3.6 6.8 7.8 9.2 12.2 13.7 2.6 16.2 7.3 16.2 7.3-3.6 8.2-9.4 11.1-10.9 11.7-.3 5.8-2.4 11.2-7.1 15.9-16.4 16.4-30 10-40.6 1.6.2 2.8-1 6.8-5 10.8L141 136.5c-1.2 1.2.6 5.4.8 5.3Z"
        fill="currentColor" class="octo-body"></path>
    </svg></a>
  <div class="container border-bottom border-body">
    <nav class="navbar navbar-expand-lg navbar-dark">
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
          <div class="input-group mb-3">
            <input id="tools-search" type="text" class="form-control" placeholder="Search tools description..."
              aria-label="Search tools description..." aria-describedby="basic-addon1">
          </div>
          <div class="container mb-3">
            <span class="badge git-badge">Git</span>
            <span class="badge apt-badge">Apt</span>
            <span class="badge pip3-badge">Pip3</span>
            <span class="badge wget-badge">Wget</span>
          </div>
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
            <button class="btn btn-light border-dark" type="button" onclick="downloadScript()">Generate script</button>
          </div>
          <code id="script-output">
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
{ACCORDION_NAME}&nbsp;<span class="badge badge-light bg-light text-dark"><span
    id="{ACCORDION_CATEGORY}-counter">0</span>/{NUMBER_OF_TOOLS}</span>
</button>
</h2>
<div id="flush-collapse{ACCORDION_NAME}" class="accordion-collapse collapse" data-bs-parent="#accordionFlush"
aria-labelledby="flush-heading{ACCORDION_NAME}">
<div class="accordion-body">
<button class="btn btn-success border-white m-1" type="button"
  onclick="allTools('{ACCORDION_CATEGORY}')">ALL</button>
<button class="btn btn-danger border-white m-1" type="button"
  onclick="noneTools('{ACCORDION_CATEGORY}')">None</button>
"""

accordion_end = """</div>
</div>
</div>
"""

accordion_data = ""

accordion_button = """<button class="btn btn-custom-dark border-white m-1 tool-class" type="button" onclick="buttonPress(this)" data-name="{TOOL_NAME}" data-category="{ACCORDION_CATEGORY}" data-installation="{INSTALLATION_METHOD}" data-bs-title="{INSTALLATION_METHOD}" data-bs-container="body" data-bs-toggle="popover" data-bs-placement="top" data-bs-trigger="hover" data-bs-content="{TOOL_DESCRIPTION}">{TOOL_NAME}</button>"""

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
