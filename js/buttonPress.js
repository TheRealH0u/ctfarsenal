var script = $("#script-output");

var commandStatus = false;

function loadJSONSync(filePath, id) {
    var xhr = new XMLHttpRequest();
    xhr.open('GET', filePath, false); // 'false' makes the request synchronous
    xhr.send(null);

    if (xhr.status === 200) {
        var json = JSON.parse(xhr.responseText);
        return json[id];
    } else {
        throw new Error('Failed to load JSON file: ' + xhr.status);
    }
}

function buttonPress(src) {
    var btn = $(src);
    var id = btn.data("name");

    btn.toggleClass('btn-custom-dark btn-custom-light');
    var category = btn.data("category");
    var installationMethod = btn.data("installation");
    var installationCategory = $(`#${installationMethod}`);
    var scriptParagraph = $(`#${id}`);
    var scriptCategory = $(`#${category}`);
    var categoryCounter = $(`#${category}-counter`);
    var installation = loadJSONSync(`tools/${category.replace("-", "/")}/${installationMethod}.json`, id);

    const spanInstallationList = ["apt", "gem", "pip3"];
    const spanInstallationDict = {
        "apt": "sudo apt install -y ",
        "gem": "sudo gem install ",
        "pip3": "pip3 install "
    };

    if (spanInstallationList.includes(installationMethod)) {
        if (scriptParagraph.length > 0) {
            scriptParagraph.remove();
            if (installationCategory.children().length == 0) {
                installationCategory.remove();
            }
            var c = parseInt(categoryCounter.text());
            c = c - 1;
            categoryCounter.text(c.toString());
        }
        else {
            if (installationCategory.length == 0) {
                text = spanInstallationDict[installationMethod];
                var addCategory = $('<div>', {
                    id: installationMethod,
                    text: text
                });
                script.append(addCategory);
                installationCategory = $(`#${installationMethod}`); // scriptCategory
            }
            var addParagraph = $("<span>", {
                id: id,
                text: installation + " "
            });
            installationCategory.append(addParagraph);
            var c = parseInt(categoryCounter.text());
            c = c + 1;
            categoryCounter.text(c.toString());
        }
    }
    else {
        if (scriptParagraph.length > 0) {
            scriptParagraph.remove();
            if (scriptCategory.children().length == 0) {
                scriptCategory.remove();
            }
            var c = parseInt(categoryCounter.text());
            c = c - 1;
            categoryCounter.text(c.toString());
        } else {
            if (scriptCategory.length == 0) {
                text = `mkdir -p $TOOLS/${category.replace("-", "/")} && export TPATH=$TOOLS/${category.replace("-", "/")}`;
                var addCategory = $('<div>', {
                    id: category,
                    text: text
                });
                script.append(addCategory);
                scriptCategory = $(`#${category}`);
            }
            var addParagraph = $("<p>", {
                id: id,
                text: installation + " "
            });
            scriptCategory.append(addParagraph);
            var c = parseInt(categoryCounter.text());
            c = c + 1;
            categoryCounter.text(c.toString());
        }
    }
}

function download(content, filename, contentType) {
    var a = document.createElement('a');
    var blob = new Blob([content], { type: contentType });
    a.href = window.URL.createObjectURL(blob);
    a.download = filename;
    a.click();
}

function downloadScript() {
    var scriptText = "#! /bin/bash\n\n";
    var toolsPath = `export TOOLS="$HOME/${$("#tools-path").val()}"`;
    scriptText += toolsPath + "\n\n";
    var divContents = $('#script-output').contents();
    $("#script-output").children("div").each(function () {
        var divContents = $(this).contents();
        scriptText += "# " + $(this).attr("id");
        divContents.each(function () {
            if (this.nodeType === 3) {
                scriptText += "\n";
                scriptText += $(this).text().trim();
            } else if (this.nodeType === 1) {
                if ($(this).is('p')) {
                    scriptText += "\n" + $(this).text().trim();
                } else if ($(this).is('span')) {
                    scriptText += " " + $(this).text().trim();
                }
            }
        });
        scriptText += "\n";
    });
    // console.log(scriptText);
    download(scriptText, "output.sh", "text/plain");
}

function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}
// TODO: Will add a function to just select all the tools od unselect all the tools
// function allTools(){
//     const buttons = document.querySelectorAll('button[class="tool-class"');
//     console.log(buttons);
// }

function allTools(category) {
    //console.log(category);
    const buttons = document.querySelectorAll(`button[data-category="${category}"]`);
    //console.log(buttons);
    for (let i = 0; i < buttons.length; i++) {
        //console.log(buttons[i]);
        if (buttons[i].classList.contains('btn-custom-dark')) {
            buttonPress(buttons[i]);
        }
    }
}

function noneTools(category) {
    //console.log(category);
    const buttons = document.querySelectorAll(`button[data-category="${category}"]`);
    //console.log(buttons);
    for (let i = 0; i < buttons.length; i++) {
        //console.log(buttons[i]);
        if (buttons[i].classList.contains('btn-custom-light')) {
            buttonPress(buttons[i]);
        }
    }
}

const activeFilters = {};

function filterTools(src, category) {
    var btn = $(src);
    btn.toggleClass(`${category}-badge ${category}-badge-active`);
    
    // Toggle filter in the global state
    if (activeFilters[category]) {
        delete activeFilters[category];
    } else {
        activeFilters[category] = true;
    }

    applyFilters();
}

function applyFilters() {
    showAllItems();

    // Dynamically build the selector for buttons that should remain visible
    let selector = 'button.tool-class';
    if (Object.keys(activeFilters).length > 0) {
        // Create a comma-separated list of selectors
        const filterSelectors = Object.keys(activeFilters)
            .map(category => `[data-installation="${category}"]`)
            .join(', ');
        
        selector += filterSelectors;
    }

    // Get all buttons
    const buttonsToHide = document.querySelectorAll('button.tool-class');

    // Hide buttons that do not match all active filters
    buttonsToHide.forEach(button => {
        // Check if the button matches the dynamic selector for active filters
        if (!button.matches(selector)) {
            button.style.display = 'none';
        }
    });

    // Check each .accordion-item and hide it if it has no visible .tool-class buttons
    const accordionItems = document.querySelectorAll('.accordion-item');
    accordionItems.forEach(item => {
        const visibleButtons = item.querySelectorAll('button.tool-class:not([style*="display: none"])');
        if (visibleButtons.length === 0) {
            item.style.display = 'none';
        } else {
            item.style.display = '';
        }
    });
}



function showAllItems() {
    // Show all tool-class buttons
    const allButtons = document.querySelectorAll('button.tool-class');
    allButtons.forEach(button => button.style.display = 'inline-block');

    // Show all accordion-item classes
    const accordionItems = document.querySelectorAll('.accordion-item');
    accordionItems.forEach(item => item.style.display = 'block');
}

function filterRemove() {
    // Select all badges
    const allBadges = document.querySelectorAll('.badge');

    // Iterate through each badge
    allBadges.forEach(badge => {
        // Get the list of classes for the badge
        const classes = badge.classList;

        // Check if the badge has an active class
        classes.forEach(className => {
            if (className.endsWith('-badge-active')) {
                // Replace '-badge-active' with '-badge'
                const newClass = className.replace('-badge-active', '-badge');
                
                // Remove the '-badge-active' class and add the '-badge' class
                badge.classList.remove(className);
                badge.classList.add(newClass);
            }
        });
    });

    showAllItems();
}
