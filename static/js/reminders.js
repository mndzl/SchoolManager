$("document").ready(function(){
    $(".icon-book").click(function(){
        $("aside").toggleClass("toggle");
        $(this).toggleClass("toggle_book");
    });
    page=window.location.pathname.substring(1, window.location.pathname.length-1);
    try{
        if (page!='/' && page!='tasks/') {        
            $(`.${page}-nav`).css('background-color', '#d6d6d6');
            $(`.${page}-nav`).css('opacity', '1');   
        }
    }catch(error){
        console.error(error);
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

    $("input[name='file_field']").change(function(){
        $('.files').html('');
        files = [];
        for(var i=0; i<$(this).get(0).files.length; i++){
            files.push($(this).get(0).files[i].name);
            $(".files").append(`<div class='file'><div class='filename'>${$(this).get(0).files[i].name}</div></div>`);
        }
    });
});
