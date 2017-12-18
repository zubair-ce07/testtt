(function () {

    $(document).ready(function() {

        var updateBtn = $('#update_user'),
        deleteBtn = $('#delete'),
        errorsList = $('#error_list'),
        requestedUserId = window.location.pathname.split("/")[2],
        user = new User();

        if(localStorage.getItem('user_id') !== requestedUserId){
            deleteBtn.hide();
            updateBtn.hide();
        }

        user.load(requestedUserId, errorsList);

        deleteBtn.click(function () {
           user.deleteUser(requestedUserId, errorsList);
        });

        updateBtn.click(function () {

            var user = new User(
                $('#email').val(),
                '',
                '',
                $('#f_name').val(),
                $('#l_name').val(),
                $('#dob').val(),
                undefined,
                errorsList
            );

            user.updateUser(requestedUserId);
        });
    });

}());
