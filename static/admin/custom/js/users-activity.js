if (!$) $ = django.jQuery

function getUsersData() {
    $('.ajax-loader.users-activity').show();
    $.ajax({
        method: "GET",
        url: '/get_users_data/',
        data: {
            'select_org': $('#id_select_org_1').val(),
        },
        dataType: 'json',
        success: (response) => {
            var bodyHtml = '',
                yes_no = b => {
                    var icon = ['icon-yes', 'icon-no'][+b], alt = ['True', 'False'][+b], title = ['В сети', 'Вне сети'][+b];
                    return `<img src="/static/admin/img/${icon}.svg" alt=${alt} title=${title}>`
                }
            $('p').html('').append('<b>Всего пользователей:</b> ' + Object.keys(response).length + '</p>')
            $('table tbody').children().remove();
            for (var key in response) bodyHtml += `
            <tr>
                <td><a href="/admin/auth/user/${response[key][0]}/change/">${key}</a></td>
                <td>${response[key][1]}</td>
                <td>${response[key][2]}</td>
                <td>${response[key][3]}</td>
                <td>${yes_no(response[key][4])}</td>
            </tr>`;
            $('table tbody').append(bodyHtml);
            $('.ajax-loader.users-activity').hide();
        },
    });
};

$(document).ready(() => { getUsersData() });
$(document).on('change', '#id_select_org_1', () => { getUsersData() });
$(document).on('click', '#id_button_refresh_1', () => { getUsersData() });
