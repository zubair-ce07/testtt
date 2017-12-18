(function () {
    $(document).ready(function() {
        $('#loader').click(function () {
            var users = new Users($('#users'), $('#error_list'));
            users.load()
        });
    });

    function Users(usersUl, errors){
        this.users = [];
        this.usersUl = usersUl;
        this.errors = errors;
    }

    Users.prototype.load = function () {
        this.usersUl.empty();
        this.errors.empty();

        var usersUl = this.usersUl;
        var errors = this.errors;
        var users = this.users;

        $.ajax({
            method: 'GET',
            url: '/api/users/',
            success: function (data) {
                users = data;
                for(var user in users){
                    var link = '<a href="' + users[user].id + '/">' + users[user].email + '</a>';
                    usersUl.append($('<li></li>').html(link));
                }
            },
             error: function (xhr) {
                if(xhr.status === 0)
                    errors.append($('<li></li>').text('Error Occurred: Check your internet connectivity.'));
                else if(xhr.status === 403 || xhr.status === 401 || xhr.status === 400)
                errors.append($('<li></li>').text(xhr.responseJSON.detail))
             }
        });
    };
}());
