

$(document).ready(function() {
    var note = '';
    $("#notify").ajaxSuccess(function(event, request, settings, json) {
        if (json.message != null && json.message != '' && json.message != 'OK') {
            $(this).html("<ul>" + json.message + "</ul>");
            $(this).delay(1000).fadeOut(10000);
        }
        else if (json.message == 'OK') {
            $(this).text('Đã lưu');
            $(this).delay(1000).fadeOut('fast');
            location.reload('true');
        }

    });

    $("#submitform").bind('submit', function() {
        var d = $(this).serialize();
        d = d + '&request_type=add';
        var self = $(this);
        var theLast = self.prev();
        var arg = {data: d,
            type: $(this).attr('method'),
            url: $(this).attr('action'),
            success:function(json) {
                if (!json.success) {
                    $("#notify").showNotification(json.message, 3000);
                } else {
                    $.ajaxSetup({
                        global: false
                    });
                    $("#student_placeholder").load("/school/getStudent/" + json.student_id + "/",
                        function() {
                            $.ajaxSetup({
                                global: true
                            });
                            var newStudent = $("#student_placeholder").find("tr");
                            newStudent.insertBefore(self).click(select);
                            var stt = parseInt(theLast.find('td:eq(1)').text());
                            if (stt) newStudent.find('td:eq(1)').text(stt + 1);
                            else newStudent.find('td:eq(1)').text(1);
                            $(".form").find('input:text').val('');
                            $(".form").find('input#id_dan_toc').val('Kinh');
                            $("#notify").showNotification(json.message);
                                                        
                        })

                }
            }
        };
        $.ajax(arg);
        return false;
    });

    $("#import").click(function() {
        $("#fileupload").dialog('open');
    });

    $("#fileupload").dialog({
        modal : true,
        buttons: {
            Đóng: function() {
                location.reload('true');
                $(this).dialog('close');
            }
        },
        autoOpen: false,
        width: 700,
        height: 400,
        maxWidth: 700,
        maxHeight: 400,
        title: "Nhập học sinh từ file Excel"
    });

    function isNumeric(input) {
        return (input - 0) == input && input.length > 0;
    }

    var select = function() {
        if (!$(this).hasClass('thread') && !$(this).hasClass('form') && !$(this).hasClass('function')) {
            var id = $(this).attr('class').split(' ')[0];
            var checkboxid = '#checkbox_' + id;
            var checkboxall = '#checkbox_all';
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
                $(checkboxid).prop("checked", false);
                var n = $("input.studentCheckbox:checked").length;
                if (n == 1 || n==0) {
                    $(checkboxall).prop("checked", false);
                    $("#showChosenStudent").html("Chưa chọn học sinh nào");
                    $("#send").attr('disabled', 'disabled');
                } else {
                    $("#showChosenStudent").html( (n-1).toString() + " học sinh");
                }
            } else {
                $(this).addClass('selected');
                $(checkboxid).prop("checked", true);
                $(checkboxall).prop("checked", true);
                var n = $("input.studentCheckbox:checked").length;
                $("#showChosenStudent").html( (n-1).toString() + " học sinh");
                $("#send").removeAttr('disabled');
            }
        }
    };
    var delSelected = function() {
        if (!$("#checkbox_all").is(':checked')) {
            alert("Bạn chưa chọn học sinh nào để xóa");
            return false;
        }
        var answer = confirm('Bạn có muốn xóa những học sinh đã chọn');
        if (!answer) return false;
        var data = '';
        $(".selected").each(function() {
            data = data + $(this).attr('class').split(' ')[0] + '-';
        });
        $("#notify").text("Đang xóa...");
        $("#notify").show();
        var arg = { type:"POST",
            url:"",
            global: false,
            data: {data:data, request_type:'del'},
            datatype:"json",
            success: function() {
                $("#notify").showNotification("Đã xóa xong");
                location.reload('true');
            }
        };
        $.ajax(arg);
        return false;
    };
    $("#delSelected").click(delSelected);

    // individual listener
    $("tr").each(function() {
        $(this).click(select);
    });

    $("#checkbox_all").click(function() {
        var checkboxall = '#checkbox_all';
        if ($(checkboxall).is(':checked')) {
            $("tr").each(function() {
                var id = $(this).attr('class').split(' ')[0];
                var checkboxid = '#checkbox_' + id;
                if (!$(this).hasClass('selected'))
                    $(this).trigger('click');
            });
        }
        else {
            $("tr").each(function() {
                var id = $(this).attr('class').split(' ')[0];
                var checkboxid = '#checkbox_' + id;
                if ($(this).hasClass('selected'))
                    $(this).trigger('click');
            });
        }
    });
    $("#selectAll").click(function() {
        $("tr").each(select);
        return false;
    });

    $("#textSms").click(function(){
        if ($("#smsWindow").css('display') == 'none'){
            var buttonOffsetTop = $(this).offset().top;
            var contentWidth = parseInt($("#content").css('width'));
            var smsWindow = $("#smsWindow");
            var smsWindowWidth = parseInt(smsWindow.css('width'));
            smsWindow.css('position', 'absolute');
            smsWindow.css('top', buttonOffsetTop + 30);
            smsWindow.css('left', contentWidth - smsWindowWidth + 30);
            smsWindow.slideDown(400);
        } else $("#smsWindow").slideUp(400);
    });
    $("#smsClose").click(function(){
        $("#smsWindow").fadeOut(400);
    });
    $("#send").click(function(){
        var content = $("#smsContent").val();
        console.log(content);
        var studentList = "";
        $("tr.selected").each(function(){
            studentList += $(this).attr('class').split(" ")[0] + "-";
        });
        if (content.replace(/ /g,'') == ''){
            $("#notify").showNotification("Nội dung còn trống");
        } else {
            var arg = { type:"POST",
                url:"",
                global: false,
                data: { content:content,
                    request_type:'send_sms',
                    include_name: $("#includeStudentName").is(':checked'),
                    student_list:studentList},
                datatype:"json",
                success: function(json) {
                    $("#notify").showNotification("Đã gửi "+ json.number_of_sent +" tin nhắn");
                    $("#smsProgressbar").hide();
                    if (json.number_of_blank != '0' || json.number_of_failed != '0'){
                        var html = "<ul>";
                        if (parseInt(json.number_of_blank) > 0)
                            html += "<li>" + json.number_of_blank + " học sinh không có số điện thoại.</li>";
                        if (parseInt(json.number_of_failed) > 0)
                            html += "<li>"+json.number_of_failed + " học sinh không gửi được tin nhắn</li>";
                        html += "</ul>";
                        $("#smsErrorDetail").css('width', $("#smsContent").css('width'));
                        $("#smsErrorDetail").html(html).show();
                    }
                },
                error: function(){
                    $("#notify").showNotification("Gặp lỗi khi gửi tin nhắn");
                    $("#smsProgressbar").hide();
                }
            };
            $("#smsProgressbar").css('width', $("#smsContent").css('width'));
            $("#smsProgressbar").show();
            $.ajax(arg);
        }

        return false;
    });
    $("input.datepicker").datepicker("option", "yearRange", '{{ year_range }}');
    $("input.datepicker").datepicker("option", "defaultDate", '{{ default_date }}');

});