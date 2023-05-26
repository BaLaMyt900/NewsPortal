function btn_click(pk)
{
    $.ajax({
        url : "/api/click_btn/" + pk + "/" ,
        type : 'POST',
        data : { 'btn' : pk },

        success : function (json) {
            window.location.reload()
        }
    });

    return false;
}