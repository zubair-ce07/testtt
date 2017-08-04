function populate_blog(content) {

    var blog_post = "<div class=\"post-title\">" +
        "<h1>" + content.blog.title + "</h1>" +
        "</div>" +

        "<div class=\"post-info\">" +
        "<span>" + content.blog.created_on + " by <a href=\"#\" target=\"_blank\">" + content.blog.created_by + "</a></span>" +
        "</div>" +
        "<p>" + content.blog.text + "</p>";

    $(".blog-post").prepend(blog_post);

    content.comments.forEach(function (comment) {
        console.log(comment);
        var comment_template = "<div class=\"panel panel-white post panel-shadow\">" +
            "<div class=\"post-heading\">" +
            "<div class=\"pull-left image\">" +
            "<img src=\"http://bootdey.com/img/Content/user_1.jpg\" class=\"img-circle avatar\" alt=\"user profile image\">" +
            "</div>" +
            "<div class=\"pull-left meta\">" +
            "<div class=\"title h5\">" +
            "<a href=\"#\"><b>" + comment.created_by + "</b></a> made a comment." +
            "</div>" +
            "<h6 class=\"text-muted time\">" + comment.created_on + "</h6>" +
            "</div>" +
            "</div>" +
            "<div class=\"post-description\">" +
            "<p>" + comment.text + "</p>" +
            "</div>" +
            "</div>";

        $(".comments-list").prepend(comment_template);
    });


}


$(function () {

    var slug = window.location.pathname.split('/')[2];
    $.ajax({
        method: 'GET',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/blog/' + slug,
        success: function (result) {
            populate_blog(result);
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {
            console.log(XMLHttpRequest);
        }
    });

    $('.submit-comment').on('click', function (event) {
        var csrf = $(".comment-form").find("input[name=csrfmiddlewaretoken]").val();
        $.ajax({
            method: 'POST',
            dataType: 'json',
            url: 'http://127.0.0.1:8000/comment/',
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf);
            },
            data: JSON.stringify({
            created_by: "user_djangorest",
            comment_for: $('.post-title h1').text(),
            text: $(".comment-text").val(),
            created_on: "2017-08-04T09:47:47Z",
            user_ip: "127.0.0.1"}),
            success: function (result) {
                console.log(result);
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log(XMLHttpRequest);
            }

        });
    });

});
