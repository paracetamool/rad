$('#id_username').addClass('form-control').attr('placeholder', 'Имя пользователя')
$('#id_password').addClass('form-control').attr('placeholder', 'Пароль').attr('autocomplete', 'new-password')
$('#id_otp_token').addClass('form-control').attr('placeholder', 'Код')

/*
$(document).on('submit', 'form', function(e) {
    e.preventDefault()
    var formData = new FormData(this),
        choice = e.originalEvent.submitter.value
    formData.append('action', choice)
    $.ajax({
        method: 'POST',
        url: window.location.pathname,
        data: formData,
        dataType: 'json',
        processData: false,
        contentType: false,
        success: (response) => {
            if (response.type == 'modal') { $('form').append(response.html); $('#agreement').modal() }
            else if (response.type == 'page') $('body').empty().html(response.html)
            else if (response.type == 'redirect') document.location.href = response.path
        },
    })
})
*/