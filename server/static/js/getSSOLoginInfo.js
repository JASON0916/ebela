jQuery(document).ready(function ($) {

    $('#cookies_h').click(function () {
        if ($('#cookies').text() === '') {
            $.ajax({
                url: '/api/v1.0/cookies',
                type: 'GET',
            })
            .success(function (data) {
                $('#cookies').text(data);
            })
        } else {
            $('#cookies').slideToggle();
        }
    })

    $('#user_info_h').click(function () {
        if ($('#user_info').text() === '') {
            $.ajax({
                url: '/api/v1.0/user/info',
                type: 'GET',
            })
            .success(function (data) {
                if (data['code'] === '0-000-000') {
                    $('#user_info').text(
                        'user_id: ' + data['user']['id'] + '    ' +
                        'ip: ' + data['user']['ipAddress'] + '    ' +
                        'name: ' + data['user']['name']
                    )
                } else {
                        window.location = data['redirectUrl'] + window.location.href
                }
            })
        } else {
            $('#user_info').slideToggle();
        }
    })

    $('#data_auth_h').click(function () {
        if ($('#data_auth').text() === '') {
            $.ajax({
                url: '/api/v1.0/user/dataAuth',
                type: 'GET',
            })
            .success(function (data) {
                if (data['code'] === '0-000-000') {
                    $('#data_auth').text(
                        'user_id: ' + data['userId'] + '    ' +
                        'data_level: [' + data['dataLevel'] + ']' +
                        data['dataLevelInfo']
                    )
                } else {
                        window.location = data['redirectUrl'] + window.location.href
                }
            })
        } else {
            $('#data_auth').slideToggle();
        }
    })

});
