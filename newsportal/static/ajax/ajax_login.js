$(function ($) {
    $('#form_ajax').submit(function (e) {
        e.preventDefault()
        $.ajax({
            type: this.method,
            url: this.action,
            data: $(this).serialize(),
            dataType: 'json',
            success: function (response) {
                console.log('ok - ', response)
                if (response.status === 201) {
                    window.location.reload()
                } else if (response.status === 400) {
                    $('.alert-danger').text(response.error).removeClass('d-none')
                }
            }
        })
    })
})