/**
 * Created by PyCharm.
 * User: vutran
 * Date: 8/4/11
 * Time: 6:05 AM
 *
 */

var applyListener = function(){

    $("input.datepicker").datepicker({
        changeMonth: true,
        changeYear: true,
        yearRange: 'c-60:c'
    });

    $("input:text").each(function(){
        $(this).focusout(function(){
            var origin = $(this).val();
            if ($(this).is_harmful(origin)){
                $(this).focus();
                $(this).showNotification("Thông tin bạn vừa nhập có chứa mã độc.");
            }
        });
    });

    $("input:text").live('focus',function(){
        if (!$(this).hasClass('tiptipfocus')){
            $(this).select();
            return false;
        }
    });

    $('*[class~="tiptipclick"]').tipTip({
        activation: "click",
        delay: 100
    });
    $('*[class~="tiptiphover"]').tipTip({
        activation: "hover",
        delay: 100
    });
    $('*[class~="tiptiphover_delay"]').tipTip({
        activation: "hover",
        delay: 1500
    });
    $('*[class~="tiptipfocus"]').tipTip({
        activation: "focus",
        delay: 100
    });
};


$(document).ready(function(){
    // setting up css to render page in the right way

//{#    if ($.browser.msie ){#}
//{#        alert("Bạn đang dùng trình duyệt MS Internet Explorer, hãy dùng trình duyệt Firefox hoặc Chrome để hiển thị " +#}
//{#            "trang web này tốt hơn.");#}
//{#    }#}

//    $("footer").css('width',$(document).width());

//    $(document).resize(function(){
//        if ($('#place_keeper').offset().top + $("footer").outerHeight() <= $(window).height()){
//            $("footer").css('position', 'fixed');
//            $("footer").css('bottom', '0');
//        } else {
//            $("footer").css('position', 'relative');
//            $("footer").css('bottom', '');
//        }
//    });


//
//    var maxHeight = 0;
//    $(".thumb > ul").each(function(){
//        if ($(this).height() > maxHeight){
//            maxHeight = $(this).height();
//        }
//    });
//    $(".thumb > ul").each(function(){
//        $(this).css('height', maxHeight);
//    });

    // end setting up
    // xss prevention

    function toAscii(str) {
        str = str.replace(/^\s+|\s+$/g, ''); // trim
        str = str.toLowerCase();

        // remove accents, swap ñ for n, etc
        var from = "àáäâèéëêìíïîòóöôùúüûñçảãạăắằẳẵặâầấẩẫậoóòỏõọuúùủũụêềếểễệeèéẻẽẹôồốổỗộơờớởỡợìỉĩíịyỳýỷỹỵ";
        var to   = "aaaaeeeeiiiioooouuuuncaaaaaaaaaaaaaaaoooooouuuuuueeeeeeeeeeeeooooooooooooiiiiiyyyyyy";
        for (var i=0, l=from.length ; i<l ; i++) {
            str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
        }

        return str;
    }


    $.fn.is_harmful = function(origin){
        origin = toAscii(origin);
        origin = origin.replace(/\//g,' ').replace(/-/g,' ')
                .replace('@',' ').replace('Nhanh:','')
                .replace('nhanh:','');
        if ($.encoder.encodeForHTML($.encoder.canonicalize(origin)) != origin ) return true;
        return $.encoder.encodeForJavascript($.encoder.canonicalize(origin)) != origin;

    };

    $("form").each(function(){
        $(this).bind('submit',function(){
            var ok = true;
            $('input:text').each(function(){
                var origin = $(this).val();
                if ($(this).is_harmful(origin)){
                    $(this).focus();
                    $(this).showNotification("Thông tin bạn vừa nhập có chứa mã độc.");
                    ok = false;
                }
            });
            if (!ok) return false;

        });
    });



    // end xss prevention
    // jquery global function
    $.fn.disableNotification = function(){
        $(".notify-widget-pane").hide();
    };
    $.fn.enabelNotification = function(){
        $(".notify-widget-pane").show();
    };
    $.fn.showNotification = function(msg, duration){
        $("#notify").enabelNotification();
        $("#notify").text(msg);
        $("#notify").fadeIn('fast');
        if ( !duration || typeof duration != 'number') duration = 1000;
        $("#notify").data('delay', setTimeout(function(){
            $("#notify").stop(true, true).fadeOut('fast');
        }, duration));
    };
    // end jquery global function

    $.datepicker.setDefaults(
            $.extend(
                    $.datepicker.regional['vi']
            )
    );



    // local functions.

    $("#notify").ajaxStart( function(){
        $(this).text("Đang gửi dữ liệu lên máy chủ...");
        $(this).fadeIn('fast');
    });

    $("#notify").ajaxSuccess( function(event, request, settings){
        $(this).text("Đã lưu.");
        $(this).data('delay', setTimeout(function(){
            $("#notify").stop(true, true).fadeOut('fast');
        }, 1000));
    });

    $("#notify").ajaxError( function(event, request, settings){
        $(this).text("Gặp lỗi khi gửi dữ liệu tới máy chủ");
        $(this).data('delay', setTimeout(function(){
            $("#notify").stop(true, true).fadeOut('fast');
        }, 1000));
    });

    // every listener that wants to apply to DOM elements.
    applyListener();



    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }

            var ok = true;
            $('input:text').each(function(){
                var origin = $(this).val();
                if ($(this).is_harmful(origin)){
                    $(this).focus();
                    $("#notify").showNotification("Thông tin bạn vừa nhập có chứa mã độc.");
                    ok = false;
                }
            });
            if (!ok) return false;
        }
    });

    $("#feedback").click(function(){
        if ($("#feedbackWindow").css('display') == 'none'){
            var buttonOffsetTop = $(this).offset().top;
            var contentWidth = parseInt($("#content").css('width'));
            var feedbackWindow = $("#feedbackWindow");
            var feedbackWindowWidth = parseInt(feedbackWindow.css('width'));
            feedbackWindow.css('position', 'absolute');
            feedbackWindow.css('top', buttonOffsetTop + 35);
            feedbackWindow.css('left', contentWidth - feedbackWindowWidth + 30);
            feedbackWindow.slideDown(350);
        } else $("#feedbackWindow").slideUp(350);
        return false;
    });

    $("#feedbackClose").click(function(){
        $("#feedbackWindow").fadeOut(400);
    });

    $("#sendFeedback").click(function(){
        var content = $("#feedbackContent").val();
        console.log(content);
        if (content.replace(/ /g,'') == ''){
            $("#notify").showNotification("Nội dung còn trống", 3000);
        } else {
            var feedbackUrl = window.location.href;
            var arg = {
                type:"POST",
                global: false,
                url:"/app/feedback/",
                data:{content: content,
                    feedback_url: feedbackUrl},
                datatype:"json",
                success: function(json){
                    if (json.success){
                        $("#feedbackWindow").fadeOut(400);
                        $("#notify").showNotification("Đã gửi góp ý", 3000);
                    } else {
                        $("#notify").showNotification("Không gửi được góp ý lên máy chủ", 2000);
                    }
                }
            };
            $.ajax(arg);
        }

        return false;
    });


});

