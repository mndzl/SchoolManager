$("document").ready(function(){
    $(".icon-book").click(function(){
        $("aside").toggleClass("toggle");
        $(this).toggleClass("toggle_book");
    });
    page=window.location.pathname.substring(1, window.location.pathname.length-1);
    $('.'+page+'-nav').css('background-color', '#d6d6d6');
    $('.'+page+'-nav').css('opacity', '1');
});