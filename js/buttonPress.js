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

    btn.toggleClass('btn-dark btn-light');
    var category = btn.data("category");
    var scriptParagraph = $(`#${id}`);
    var scriptCategory = $(`#${category}`);
    var counter = $(`#${category}-counter`);
    if (scriptParagraph.length > 0) {
        scriptParagraph.remove();
        if (scriptCategory.children().length == 0) {
            scriptCategory.remove();
        }
        var c = parseInt(counter.text());
        c = c - 1;
        counter.text(c.toString());
    } else {
        var installation = loadJSONSync(`tools/${category.replace("-", "/")}.json` ,id);
        const categoryBlacklist = ["apt", "gem", "pip3", "go"];
        const noCategoryNoSpan = ["gospider", "sns"];
        var type = "<p>";
        if (scriptCategory.length == 0) {
            var text = "";
            if (!categoryBlacklist.includes(category)) {
                text = `mkdir -p $TOOLS/${category.replace("-", "/")} && export TPATH=$TOOLS/${category.replace("-", "/")}`;
            } else {
                switch (category) {
                    case "apt":
                        text = "sudo apt install -y ";
                        break;
                    case "pip3":
                        text = "pip3 install ";
                        break;
                    case "gem":
                        text = "sudo gem install ";
                        break;
                }
            }
            var addCategory = $('<div>', {
                id: category,
                text: text
            });
            script.append(addCategory);
            scriptCategory = $(`#${category}`);
        }
        if (categoryBlacklist.includes(category) && !noCategoryNoSpan.includes(id)) type = "<span>";
        var addParagraph = $(type, {
            id: id,
            text: installation + " "
        });
        scriptCategory.append(addParagraph);
        var c = parseInt(counter.text());
        c = c + 1;
        counter.text(c.toString());
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
        scriptText += "# "+$(this).attr("id");
        divContents.each(function () {
            if (this.nodeType === 3) {
                scriptText += "\n";
                scriptText += $(this).text().trim();
            } else if (this.nodeType === 1) {
                if ($(this).is('p')) {
                    scriptText += "\n" + $(this).text().trim();
                }else if($(this).is('span')){
                    scriptText += " " + $(this).text().trim();
                }
            }
        });
        scriptText += "\n";
    });
    // console.log(scriptText);
    download(scriptText, "output.sh", "text/plain");
}

// function allTools(category){
//     var buttons = $('[data-category="apt"]');
//     buttons.each(function() {
//         var $element = $(this);
//         handleClick().then(function() {
//             $element.click();
//         });
//     });
// }
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

function allTools(category) {
    console.log(category);
    const buttons = document.querySelectorAll(`button[data-category="${category}"]`);
    console.log(buttons);
    for(let i = 0; i < buttons.length; i++){
        console.log(buttons[i]);
        if(buttons[i].classList.contains('btn-dark')){
            buttonPress(buttons[i]);
        }
    }
}

function noneTools(category) {
    console.log(category);
    const buttons = document.querySelectorAll(`button[data-category="${category}"]`);
    console.log(buttons);
    for(let i = 0; i < buttons.length; i++){
        console.log(buttons[i]);
        if(buttons[i].classList.contains('btn-light')){
            buttonPress(buttons[i]);
        }
    }
}