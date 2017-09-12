$(function () {

    $('.button-logout').on('click', function () {
        $.ajax({
            method: 'GET',
            dataType: 'json',
            headers: {
                'Authorization': 'Token ' + TOKEN
            },
            url: 'http://127.0.0.1:8000/api/user/logout',
            success: function (result) {

                window.location.replace('http://127.0.0.1:8000');
            }
        });
    });

});
