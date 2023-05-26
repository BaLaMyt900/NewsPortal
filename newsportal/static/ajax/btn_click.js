function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}



function subscribe(pk)
{
    $.ajax({
        url : "/post/subs/subscribe/" + pk,
        type : 'POST',
        data : { 'btn' : pk,
            csrfmiddlewaretoken: getCookie('csrftoken')},

        success : function (json) {
            if (json.status === 201) {window.location.reload()}
        }
    });

    return false;
}

function unsubscribe(pk)
{
    $.ajax({
        url : "/post/subs/unsubscribe/" + pk,
        type : 'POST',
        data : {'btn' : pk,
        csrfmiddlewaretoken: getCookie('csrftoken')},

        success : function (json) {
            if (json.status === 201) {window.location.reload()}
        }
    });

    return false;
}
