(function(){
    $(document).ready(function() {
        $('#login').click(function (event) {
            event.preventDefault();

            var login = new Login($('#email').val(), $('#password').val(), $('#error_list'));
            login.signIn();
        });
    });
}());
