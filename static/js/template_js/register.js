$(document).ready(function(){
    // setting up layout
    var maxWidth=-1;
    $(".verticalLabel").each(function(){
        var width = parseInt($(this).css('width'));
        if (width > maxWidth) maxWidth = width;
    });
    $(".verticalLabel").each(function(){
        $(this).css('width', maxWidth);
    });

    $("#sendRegister").click(function(){
        var self = $(this);
        // check validity
        var registerName = $("#registerName").val().replace(/^\s+|\s+$/g,'');
        if (registerName == ""){
            $("#registerName").css('border-color','red');
            $("#notify").showNotification("Họ và tên còn trống", 2000);
            return false;
        } else $("#registerName").css('border-color','#999');
        var registerEmail = $("#registerEmail").val().replace(/^\s+|\s+$/g,'');
        if (!(registerEmail.split('@').length-1 == 1 && registerEmail.split('.').length-1>0)){
            $("#registerEmail").css('border-color','red');
            $("#notify").showNotification("Email không tồn tại", 2000);
            return false;
        } else $("#registerEmail").css('border-color','#999');
        var registerSchoolName = $("#registerSchoolName").val().replace(/^\s+|\s+$/g,'');
        if (registerSchoolName == ""){
            $("#registerSchoolName").css('border-color','red');
            $("#notify").showNotification("Tên trường còn trống", 2000);
            return false;
        } else $("#registerSchoolName").css('border-color','#999');
        var registerPhone = $("#registerPhone").val().replace(/^\s+|\s+$/g,'');
        var registerSchoolAddress = $("#registerSchoolAddress").val().replace(/^\s+|\s+$/g,'');
        var registerSchoolLevel = $("#registerSchoolLevel").val();
        var registerSchoolProvince = $("#registerSchoolProvince").val();
        // end checking
        if (self.text() == "Gửi"){
            $("#registerNotice").show();
            self.text("Đồng ý");
        } else if (self.text() == "Đồng ý"){
            var arg = { type:"POST",
                url:"",
                global: false,
                data: { register_name:registerName,
                        register_phone:registerPhone,
                        register_email:registerEmail,
                        school_name:registerSchoolName,
                        school_level:registerSchoolLevel,
                        school_address:registerSchoolAddress,
                        school_province:registerSchoolProvince},
                datatype:"json",
                success: function(json) {
                    if (json.success){
                        $("#notify").showNotification("Đã đăng ký thành công", 2000);
                        $("#registerNotice").hide();
                        self.text('Gửi');
                    } else {
                        $("#notify").showNotification(json.message, 2000);
                    }

                },
                error: function(){
                    $("#notify").showNotification("Gặp lỗi khi gửi đăng ký", 2000);
                }
            };
            $.ajax(arg);
        }
        return false;
    });
});