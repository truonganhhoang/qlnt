$(document).ready(function(){
    $(".accountInfo").hide();
    $("#tableFunction").css('width', $("#registerTable").css('width'));
    var select = function() {
        if (!$(this).hasClass('thread') && !$(this).hasClass('form') && !$(this).hasClass('function')) {
            var id = $(this).attr('class').split(' ')[0];
            var checkboxid = '#checkbox_' + id;
            var checkboxall = '#checkbox_all';
            if ($(this).hasClass('selected')) {
                $(this).removeClass('selected');
                $(checkboxid).prop("checked", false);
                var n = $("input.registerCheckbox:checked").length;
                if (n == 1 || n==0) {
                    $(checkboxall).prop("checked", false);
                }
            } else {
                $(this).addClass('selected');
                $(checkboxid).prop("checked", true);
                $(checkboxall).prop("checked", true);
            }
        }
    };
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

    var delSelected = function() {
        if (!$("#checkbox_all").is(':checked')) {
            alert("Bạn chưa chọn đăng ký nào để xóa");
            return false;
        }
        var answer = confirm('Bạn có muốn xóa những đăng ký đã chọn');
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
            success: function(json) {
                if (json.success){
                    $("#notify").showNotification("Đã xóa xong");
                    location.reload('true');
                } else {
                    $("#notify").showNotification(json.message);
                }

            }
        };
        $.ajax(arg);
        return false;
    };
    $("#delSelected").click(delSelected);
    $("#createSelected").click(function(){
         if (!$("#checkbox_all").is(':checked')) {
            alert("Bạn chưa chọn đăng ký nào để tạo tài khoản");
            return false;
        }
        var data = '';
        $(".selected").each(function() {
            data = data + $(this).attr('class').split(' ')[0] + '-';
        });
        $("#notify").text("Đang tạo tài khoản...");
        $("#notify").show();
        var arg = { type:"POST",
            url:"",
            global: false,
            data: {data:data, request_type:'create_acc'},
            datatype:"json",
            success: function(json) {
                if (json.success){
                    $("#notify").showNotification(json.message);
                    var accounts = json.account_info;
                    accounts = accounts.split(',');
                    for ( var i=0; i< accounts.length; i++){
                        account = accounts[i];
                        console.log(account);
                        if ( account != ""){
                            var id = account.split('-')[0];
                            var username = account.split('-')[1];
                            console.log('->>', id, username);
                            var theTr = $("."+id);
                            theTr.append('<td style="padding-left: 4px;">'+username+'</td>');
                            theTr.append('<td style="padding-left: 4px;">'+username+'</td>');
                        }
                    }
                    $(".accountInfo").show();
                    $("#tableFunction").css('width', $("#registerTable").css('width'));
                } else {
                    $("#notify").showNotification(json.message);
                }
            }
        };
        $.ajax(arg);
        return false;
    });

});