/* Some Global Variables */

var published_comments = null;

function add_comment(comment) {

    var $comment_post = $('#content1 .comment:first:first-of-type').clone(true);
    $comment_post.find('.created-by').text(comment.created_by);
    $comment_post.find('.created-on').text((new Date(comment.created_on)).toUTCString());
    $comment_post.find('.text').text(comment.text);
    $('#' + comment.comment_for).find('.comment-list').append($comment_post);
    $comment_post.show();
}

function populate_comments() {
    published_comments.forEach(comment => {
        add_comment(comment);
    });
}


$(function () {

    $('.view-more').on('click', function (event) {
        event.preventDefault();

        if (TOKEN == null) {

            $('.alert-request').show().fadeTo(3000, 0).slideUp(200, function () {
                $(this).css({ opacity: 1 });
            });
            
            event.stopPropagation();
            return;
        }

        $.ajax({
            context: this,
            method: 'GET',
            dataType: 'json',
            headers: {
                'Authorization': 'Token ' + TOKEN
            },
            url: 'http://127.0.0.1:8000/api/blog/' + $(this).attr('href'),
            success: function (result) {
                published_comments = result.comments;
                populate_comments();
                $(this).removeAttr('href').off('click');
                if (!result.blog.comments_allowed) {
                    $('#' + result.blog.id).find('.card').remove();
                } else {
                    $('#' + result.blog.id).find('.comment-for').attr('value', result.blog.id);
                }
            }
        });
    });
});
