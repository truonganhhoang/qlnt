/**
 * Created by PyCharm.
 * User: vutran
 * Date: 7/30/11
 * Time: 12:46 AM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function(){


    $("#sortableList").sortable({
        placeholder: 'ui-state-highlight'
    });
    $("#sortableList").disableSelection();

    $("li.sortable").each(function(){
        $(this).hover(function(){
            $(this).addClass('ui-state-hover');
        }, function(){
            $(this).removeClass('ui-state-hover');
        });
    });

    $("li.sortable").each(function(){
        $(this).click(function(){
            if (!$(this).hasClass('ui-state-focus')){
                $(".ui-state-focus").removeClass('ui-state-focus');
                $(this).addClass('ui-state-focus');
            }
        });
    });

    $("li.sortable").each(function(){
        $(this).dblclick(function(){
            if ($(".ui-state-active").length >0){
                var oldSelected = $(".ui-state-active");
                oldSelected.children('span').hide();
                oldSelected.removeClass('ui-state-active');
                $("#sortableList").append("<li id='tempNode'> </li>");
                var temp = $("#tempNode");
                oldSelected.before(temp);
                $(this).after(oldSelected);
                temp.before($(this));
                temp.remove();
            } else {
                $(this).children('span').show();
                $(this).addClass('ui-state-active');
            }
        });
    });

    var theFocus = $("#sortableList > li:first").addClass('ui-state-focus');
    var saveState = $("#sortableList").html();

    $("#cancel_list_sorting").click(function(){
        $("#sortableList").html(saveState);
        $("li.sortable").each(function(){
            $(this).hover(function(){
                $(this).addClass('ui-state-hover');
            }, function(){
                $(this).removeClass('ui-state-hover');
            });
        });

        $("li.sortable").each(function(){
            $(this).click(function(){
                if (!$(this).hasClass('ui-state-focus')){
                    $(".ui-state-focus").removeClass('ui-state-focus');
                    $(this).addClass('ui-state-focus');
                }
            });
        });

        $("li.sortable").each(function(){
            $(this).dblclick(function(){
                if ($(".ui-state-active").length >0){
                    var oldSelected = $(".ui-state-active");
                    oldSelected.children('span').hide();
                    oldSelected.removeClass('ui-state-active');
                    $("#sortableList").append("<li id='tempNode'> </li>");
                    var temp = $("#tempNode");
                    oldSelected.before(temp);
                    $(this).after(oldSelected);
                    temp.before($(this));
                    temp.remove();
                } else {
                    $(this).children('span').show();
                    $(this).addClass('ui-state-active');
                }
            });
        });

        return false;
    })


    $(document).keydown( function(event){
        var theSelected = $(".ui-state-active");
        if (theSelected.length >0){
            // selected an element => moving that element to organize elements.
            if ( event.which == 38){
                // up arrow key
                var prev = theSelected.prev('li.sortable');
                if (prev.length > 0){
                    prev.before(theSelected);
                }
            } else if ( event.which == 40){
                // down arrow key
                var next = theSelected.next('li.sortable');
                if (next.length >0) next.after(theSelected);
            } else if ( event.which == 13){
                theSelected.removeClass('ui-state-active');
                theSelected.children('span').hide();
            }
        } else {
            theFocus = $(".ui-state-focus");
            if ( event.which == 38){
                var prev = theFocus.prev('li.sortable');
                if ( prev.length > 0){
                    prev.addClass('ui-state-focus');
                    theFocus.removeClass('ui-state-focus');
                }
            } else if ( event.which == 40){
                var next = theFocus.next('li.sortable');
                if ( next.length > 0) {
                    next.addClass('ui-state-focus');
                    theFocus.removeClass('ui-state-focus');
                }
            } else if ( event.which == 13){
                theFocus.children('span').show();
                theFocus.addClass('ui-state-active');
            }
        }

        //return false;
    });

    // save button
    $("#save").click( function(){
        var data = "";
        $("#sortableList > li").each(function(){
            var id = $(this).attr('id');
            var index = $(this).parents().children().index($(this));
            data = data + id + '_' + index + '/';
        });

        var arg = { type:"POST",
            url: $("#ajax_to").text(),
            data:{data: data},
            datatype:"json",
            success: function(){
                // restore original state of table
                saveState = $("#sortableList").html();
            }
        };
        $.ajax(arg);
    })



});