$.fn.dialog=function(option){
    if(option=="show"){
        $(this).fadeIn(100);
    }else if(option=="hide"){
        $(this).fadeOut(1000);
        $(this).trigger("dialog.hiden");
    }
}

$(function(){
    $(".sdialog-footer>button").click(function () {
        $(this).parents(".sdialog").dialog("hide");
    });
});