$(document).ready(function () {
    $('.messages').delay(2000).fadeOut();

    fetch('http://127.0.0.1:8000/api/tasks/')
        .then(function (response) {
            return response.json();
        })
        .then(function (TasksJson) {
            $.each(TasksJson, function (index, value) {
                let html = "<div class=\"col-md-4\">\n" +
                    "                    <div class=\"card mb-2 \">\n" +
                    "                        <div class=\"card-body\">\n" +
                    "                            <h3 class=\"card-title\" id=\"title\"> " + value.title + "</h3>\n" +
                    "                            <p class=\"card-title\">\n" +
                    "                                <strong>Assignee: </strong>" + value.assignee.username + "</p>\n" +
                    "                            <p class=\"card-title\">\n" +
                    "                                <strong>Assigned By: </strong>" + value.assigned_by.username + "</p>\n" +
                    "                            <p class=\"card-title\">\n" +
                    "                                <strong>Due: </strong> " + value.due_date + "\n" +
                    "                            </p>\n" +
                    "                            <p class=\"card-text\">" + value.description + "</p>\n" +
                    "                            <p class=\"card-title\">\n" +
                    "                                <strong>Status: </strong> " + value.status + "\n" +
                    "                            </p>\n" +
                    "                        </div>\n" +
                    "                    </div>\n" +
                    "                            <hr>" +
                    "                </div>";

                $('.row').append(html)
            });
        })
});
