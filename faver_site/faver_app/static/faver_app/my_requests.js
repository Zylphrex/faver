$(document).ready(function() {
    $('.award').click(function() {
        $.ajax({
            url : "/complete-request/",
            type: "POST",
            data : {
                csrfmiddlewaretoken: document.getElementsByName('csrfmiddlewaretoken')[0].value,
                'title': $(this).siblings(".title").html(),
            },
            dataType : "json",
            success: function( data ){
                location.reload(true);
            },
        });
    });
});
