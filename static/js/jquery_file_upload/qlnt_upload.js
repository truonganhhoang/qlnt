/*
 * jQuery File Upload Plugin JS Example 5.0.2
 * https://github.com/blueimp/jQuery-File-Upload
 *
 * Copyright 2010, Sebastian Tschan
 * https://blueimp.net
 *
 * Licensed under the MIT license:
 * http://creativecommons.org/licenses/MIT/
 */



/*jslint nomen: true */
/*global $ */

$(function () {
    'use strict';
    function IsNumeric(input){
        return (input - 0) == input && input.length > 0;
    };

    var id = window.location.pathname.split('/');
    var i = 0;
    for ( i=0; i < id.length; i++){
        if (IsNumeric(id[i])){
            id = id[i];
            break;
        }
    };

    // Initialize the jQuery File Upload widget:
    $('#fileupload').fileupload({
        url: '/school/start_year/import/student/' + id,
        acceptFileTypes: /(\.|\/)(xls)$/i,
        maxNumberOfFiles: 10

    });

    $("#fileupload").bind('fileuploaddone', function(e, data){
            $("#notify").text("Đã lưu.");
            $("#notify").delay(1000).fadeOut('fast');

    });

    //$("#startUpload").attr('disabled', 'disabled');
    //$("#startUpload").addClass('ui-button-disabled ui-state-disabled');

    
    // Load existing files:
    /*$.getJSON($('#fileupload form').prop('action'), function (files) {
        var fu = $('#fileupload').data('fileupload');
        fu._adjustMaxNumberOfFiles(-files.length);
        fu._renderDownload(files)
            .appendTo($('#fileupload .files'))
            .fadeIn(function () {
                // Fix for IE7 and lower:
                $(this).show();
            });
    });
*/
    // Open download dialogs via iframes,
    // to prevent aborting current uploads:
    $('#fileupload .files a:not([target^=_blank])').live('click', function (e) {
        e.preventDefault();
        $('<iframe style="display:none;"></iframe>')
            .prop('src', this.href)
            .appendTo('body');
    });

});