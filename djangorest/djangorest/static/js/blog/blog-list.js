/* Some Global Variables */

var published_blogs = null;

function add_published_blog(blog) {
    var $blog_post = $('#content1 .blog-post:first:first-of-type').clone(true);
    $blog_post.attr('id', blog.id);
    $blog_post.find('.author').text(blog.created_by);
    $blog_post.find('.blog-post-time').text('Posted on ' + (new Date(blog.published_date)).toUTCString());
    $blog_post.find('.blog-summary').text(blog.summary);
    $blog_post.find('.blog-title').text(blog.title);
    $blog_post.find('.blog-text').text(blog.text);
    $blog_post.find('.view-more').attr('href', blog.slug);
    $('#content1 .blog-list').append($blog_post);
    $blog_post.show();
}

function populate_published_blogs() {
    published_blogs.forEach(blog => {
        add_published_blog(blog);
    });
}


$(function () {

    $.ajax({
        method: 'GET',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/api/blog/',
        success: function (result) {
            published_blogs = result;
            populate_published_blogs();
        }
    });

});
