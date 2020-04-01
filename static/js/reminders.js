$("document").ready(function(){
    $(".icon-book").click(function(){
        $("aside").toggleClass("toggle");
        $(this).toggleClass("toggle_book");
    });
    page=window.location.pathname.substring(1, window.location.pathname.length-1);
    if (page!='/' && page!='tasks/') {        
        $(`.${page}-nav`).css('background-color', '#d6d6d6');
        $(`.${page}-nav`).css('opacity', '1');   
    }


    // Tasks done handling
    $(".task-done").click(function(){
        var task_id = $(this).next().text();
        var old_this = $(this);
        $.ajax({
            url: `/tasks/${task_id}/done`,
            success: function(answer){
                if (old_this.parent().parent().parent().attr('class') == 'task-undones') {
                    var clone = old_this.parent().parent().clone(true,true).appendTo('.task-dones');
                    old_this.parent().parent().remove();

                    dones = parseInt($('.dones-length').text()) + 1;
                    undones = parseInt($('.undones-length').text()) - 1;
                    $('.dones-length').html(dones);
                    $('.undones-length').html(undones);


                }else if(old_this.parent().parent().parent().attr('class') == 'task-dones'){
                    var clone = old_this.parent().parent().clone(true,true).appendTo('.task-undones');
                    old_this.parent().parent().remove();     

                    dones = parseInt($('.dones-length').text()) - 1;
                    undones = parseInt($('.undones-length').text()) + 1;
                    $('.dones-length').html(dones);
                    $('.undones-length').html(undones);
                    
                }
            },
            error: function(){
                alert("Ha ocurrido un error.");
            }
        });
    });

});
