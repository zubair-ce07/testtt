(function(){

    $(document).ready(function() {
        $('#create_user').click(function (event) {
            event.preventDefault();

            var user = new User(
                $('#email').val(),
                $('#password').val(),
                $('#c_password').val(),
                $('#f_name').val(),
                $('#l_name').val(),
                $('#dob').val(),
                $('#photo'),
                $('#error_list')
            );

            user.createUser();
        });
    });

}());
