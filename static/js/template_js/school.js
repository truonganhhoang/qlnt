/**
 * Created by PyCharm.
 * User: root
 * Date: 10/25/11
 * Time: 2:04 PM
 * To change this template use File | Settings | File Templates.
 */
$(document).ready(function(){
    var max = -1;
    $(".classDiv").each(function(){
        console.log($(this).css('width'));
        var width = parseInt($(this).css('width'));
        if (width > max)
            max = width;
    });
    $(".classDiv").each(function(){
        $(this).css('width', max);
    });
    console.log(max);
});