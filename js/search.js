function checkAnyStringInArray(mainStr, arr) {
    mainStr = mainStr.toLowerCase();
    return arr.some(str => mainStr.includes(str));
}

function stringContainsAll(string, array) {
    string = string.toLowerCase();
    for (var i = 0; i < array.length; i++) {
        if (string.indexOf(array[i]) === -1) {
            return false;
        }
    }
    return true;
}

$("#tools-search").on("input", function(){
    var input = $(this).val().trim().toLowerCase();
    if(input !== ""){
        var search = input.split(" ");
        $(".accordion-item").each(function(){
            var $toolClasses = $(this).find(".accordion-body .tool-class");
            $toolClasses.each(function() {
                var bsContent = $(this).data("bs-content");
                if(!stringContainsAll(bsContent, search)){
                    $(this).hide();
                }else{
                    $(this).show();
                }
            });
            console.log($(this).find("h2:first").text().trim());
            console.log($toolClasses.filter(function() { return $(this).css('display') == 'none'; }).length);
            var allHidden = true;
            $toolClasses.each(function(){
                if($(this).css("display") !== "none"){
                    allHidden = false;
                    return false;
                }
            });
            if(allHidden){
                $(this).hide();
            }else{
                $(this).show();
            }
            // if ($toolClasses.filter(function() { console.log($(this)); return $(this).css('display') === 'none'; }).length === 0) {
            //     $(this).show();
            // } else {
            //     $(this).hide();
            // }
        });
    }else{
        $(".accordion-item").each(function(){
            var $toolClasses = $(this).find(".accordion-body .tool-class");
            $toolClasses.each(function() {
                $(this).show();
            });
            $(this).show();
        });
    }
});