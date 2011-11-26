

$(document).ready(function() {
    (function($) {
        $.widget("ui.combobox", {
            _create: function() {
                var self = this,
                        select = this.element.hide(),
                        selected = select.children(":selected"),
                        value = selected.val() ? selected.text() : "";
                var input = this.input = $("<input>")
                        .insertAfter(select)
                        .val(value)
                        .addClass("ui-widget ui-widget-content ui-corner-left")
                        .autocomplete({
                            delay: 0,
                            minLength: 0,
                            source: function(request, response) {
                                var matcher = new RegExp($.ui.autocomplete.escapeRegex(request.term), "i");
                                response(select.children("option").map(function() {
                                    var text = $(this).text();
                                    if ( !request.term || matcher.test(text) )
                                        return {
                                            label: text.replace(
                                                    new RegExp(
                                                            "(?![^&;]+;)(?!<[^<>]*)(" +
                                                                    $.ui.autocomplete.escapeRegex(request.term) +
                                                                    ")(?![^<>]*>)(?![^&;]+;)", "gi"
                                                    ), "<strong>$1</strong>"),
                                            value: text,
                                            option: this
                                        };
                                }));
                            },
                            select: function(event, ui) {
                                ui.item.option.selected = true;
                                self._trigger("selected", event, {
                                    item: ui.item.option
                                });
                                this.value = ui.item.option.text;
                                var attr = $(this).parents("tr").attr('id');
                                var teacher = ui.item.option.value;
                                $(this).parents("td").children("#id_teacher_id").val(teacher);
                                $(this).parents("td").children(".all_teacher").val(teacher);
                                $(this).parents("td").children(".major_teacher").val(teacher);

                                if (typeof attr !== 'undefined' && attr !== false && attr !== 'subject_form') {
                                    var id = $(this).parents("tr").attr('id').split(' ')[0];
                                    var data = { id: id, teacher: teacher, request_type:'teacher'};
                                    var arg = { type:"POST",
                                        url:"",
                                        data: data,
                                        datatype:"json",
                                        error: function() {
                                            $(".submitbutton").attr('disabled', false);
                                            $(".submitbutton").val('Lưu lại');
                                        }
                                    };
                                    $.ajax(arg);
                                    return false;
                                }

                            },
                            change: function(event, ui) {
                                if (!ui.item) {
                                    var matcher = new RegExp("^" + $.ui.autocomplete.escapeRegex($(this).val()) + "$", "i"),
                                            valid = false;
                                    select.children("option").each(function() {
                                        if ($(this).text().match(matcher)) {
                                            this.selected = valid = true;
                                            return false;
                                        }
                                    });
                                    if (!valid) {
                                        // remove invalid value, as it didn't match anything
                                        $(this).val("");
                                        select.val("");
                                        input.data("autocomplete").term = "";
                                        return false;
                                    }
                                }
                            }
                        });

                input.data("autocomplete")._renderItem = function(ul, item) {
                    return $("<li></li>")
                            .data("item.autocomplete", item)
                            .append("<a>" + item.label + "</a>")
                            .appendTo(ul);
                };

                this.button = $("<button type='button'>&nbsp;</button>")
                        .attr("tabIndex", -1)
                        .attr("title", "Danh sách giáo viên")
                        .insertAfter(input)
                        .button({
                            icons: {
                                primary: "ui-icon-triangle-1-s"
                            },
                            text: false
                        })
                        .removeClass("ui-corner-all")
                        .addClass("ui-corner-right ui-button-icon")
                        .click(function() {
                            // close if already visible
                            if (input.autocomplete("widget").is(":visible")) {
                                input.autocomplete("close");
                                return;
                            }

                            // work around a bug (likely same cause as #5265)
                            $(this).blur();

                            // pass empty string as value to search for, displaying all results
                            input.autocomplete("search", "");
                            input.focus();
                        });
            }
        });
    })(jQuery);

    $(function() {
        $(".combobox").each(function() {
            $(this).combobox();
        });
    });

    $("#notify").ajaxSuccess(function(event, request, settings, json) {
        if (json.message != null) {
            $(this).html("<ul>" + json.message + "</ul>");
            $(this).delay(1000).fadeOut(10000);
        }
        else {
            $(this).text("Đã lưu");
            $(this).delay(1000).fadeOut('fast');
        }
    });

    $(".submitbutton").attr("disabled", true);

    $("select[name=type]").each(function() {
        $(this).change(function() {
            var attr = $(this).parents("tr").attr('id');
            if (typeof attr !== 'undefined' && attr !== false && attr !== 'subject_form') {
                var id = $(this).parents("tr").attr('id').split(' ')[0];
                var type = $(this).val();
                var data = { id: id, type: type, request_type:'type'};
                var arg = { type:"POST",
                    url:"",
                    data: data,
                    datatype:"json",
                    error: function() {
                        $(".submitbutton").attr('disabled', false);
                        $(".submitbutton").val('Lưu lại');
                    }
                };
                $.ajax(arg);
                return false;
            }

        });
    });

    $("select[name=primary]").each(function() {
        $(this).change(function() {
            var attr = $(this).parents("tr").attr('id');
            if (typeof attr !== 'undefined' && attr !== false && attr !== 'subject_form') {
                var id = $(this).parents("tr").attr('id').split(' ')[0];
                var primary = $(this).val();
                var data = { id: id, primary: primary, request_type:'primary'};
                var arg = { type:"POST",
                    url:"",
                    data: data,
                    datatype:"json",
                    error: function() {
                        $(".submitbutton").attr('disabled', false);
                        $(".submitbutton").val('Lưu lại');
                    }
                };
                $.ajax(arg);
                return false;
            }
        });
    });

    $("select[name=teacher_id]").each(function() {
        //$(this).hide();
        $(this).addClass("combobox");
    });

    $("input[name=hs]").each(function() {
        $(this).change(function() {
            var attr = $(this).parents("tr").attr('id');
            if (typeof attr !== 'undefined' && attr !== false && attr !== 'subject_form') {
                var id = $(this).parents("tr").attr('id').split(' ')[0];
                var val = $(this).val();
                var data = { id: id, hs: val, request_type:'hs'};
                var arg = { type:"POST",
                    url:"",
                    data: data,
                    datatype:"json",
                    error: function() {
                        $(".submitbutton").attr('disabled', false);
                        $(".submitbutton").val('Lưu lại');
                    },
                    success: function() {
                    }
                };
                $.ajax(arg);
                return false;
            }
        });
    });

    $("input[name=nx]").each(function() {
        $(this).change(function() {
            var attr = $(this).parents("tr").attr('id');
            if (typeof attr !== 'undefined' && attr !== false && attr !== 'subject_form') {
                var id = $(this).parents("tr").attr('id').split(' ')[0];
                var val = $(this).is(':checked');
                var data = { id: id, nx: val, request_type:'nx'};
                var arg = { type:"POST",
                    url:"",
                    data: data,
                    datatype:"json",
                    error: function() {
                        $(".submitbutton").attr('disabled', false);
                        $(".submitbutton").val('Lưu lại');
                    },
                    success: function() {
                    }
                };
                $.ajax(arg);
                return false;
            }
        });
    });

    $(".major_teacher").each(function(){
        if ($(this).parents("td").children(".all_teacher").children("#id_teacher_id").val()==''){
            $(this).parents("td").children(".all_teacher").hide();
        }
        else if ($(this).children("select").val()==''){
            $(this).hide();
            $(this).parents("td").children(".range").val('1');
        }
        else{
            $(this).parents("td").children(".all_teacher").hide();
        }
    });

    $(".range").each(function(){
        $(this).change(function(){
            if ($(this).val() == '1'){
                $(this).parents("td").children(".all_teacher").show();
                $(this).parents("td").children(".major_teacher").hide();
            }
            else{
                $(this).parents("td").children(".all_teacher").hide();
                $(this).parents("td").children(".major_teacher").show();
            }
        });
    });
});