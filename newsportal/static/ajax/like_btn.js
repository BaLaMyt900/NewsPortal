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


function postlike(pk)
{
    $.ajax({
        url : "/post/like/" + pk,
        type : 'POST',
        data : { 'btn' : pk,
            csrfmiddlewaretoken: getCookie('csrftoken')},

        success : function (json) {
            if (json.status === 201) {window.location.reload()}
            else if (json.status === 400) {console.log('err - ', json)}
        }
    });

    return false;
}

function postdislike(pk)
{
    $.ajax({
        url : "/post/dislike/" + pk,
        type : 'POST',
        data : { 'btn' : pk,
            csrfmiddlewaretoken: getCookie('csrftoken')},

        success : function (json) {
            if (json.status === 201) {window.location.reload()}
            else if (json.status === 400) {console.log('err - ', json)}
        }
    });

    return false;
}

function commlike(pk)
{
    $.ajax({
        url : "/post/comm/like/" + pk,
        type : 'POST',
        data : { 'btn' : pk,
            csrfmiddlewaretoken: getCookie('csrftoken')},

        success : function (json) {
            if (json.status === 201) {window.location.reload()}
            else if (json.status === 400) {console.log('err - ', json)}
        }
    });

    return false;
}

function commdislike(pk)
{
    $.ajax({
        url : "/post/comm/dislike/" + pk,
        type : 'POST',
        data : { 'btn' : pk,
            csrfmiddlewaretoken: getCookie('csrftoken')},

        success : function (json) {
            if (json.status === 201) {window.location.reload()}
            else if (json.status === 400) {console.log('err - ', json)}
        }
    });

    return false;
}