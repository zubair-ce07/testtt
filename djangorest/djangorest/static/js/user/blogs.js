/* Some Global Variables */

var user_blogs = null;

function add_user_blog(blog) {

    var $blog_post = $('#content3 .blog-post:first:first-of-type').clone(true);
    $blog_post.attr('id', blog.id);
    $blog_post.find('.author').text(blog.created_by);
    $blog_post.find('.blog-post-time').text('Posted on ' + (new Date(blog.published_date)).toUTCString());
    $blog_post.find('.blog-summary').text(blog.summary);
    $blog_post.find('.blog-title').text(blog.title);
    $blog_post.find('.blog-text').text(blog.text);
    $blog_post.find('.created-by').attr('value', blog.created_by);
    $blog_post.find('.slug').attr('value', blog.slug);
    $blog_post.find('.title').attr('value', blog.title);
    $blog_post.find('.edit-blog-form').attr('name', blog.slug);
    $blog_post.find('.delete-blog .blog-slug').attr('value', blog.slug);
    $blog_post.find('.view-more').attr('href', blog.slug);
    
    if(blog.is_published) {
        $blog_post.find('.is-published').addClass('active');
    }
    if(blog.is_public) {
        $blog_post.find('.is-public').addClass('active');
    }
    if(blog.comments_allowed) {
        $blog_post.find('.comments-allowed').addClass('active');
    }
    $('#content3 .blog-list').append($blog_post);
    $blog_post.show();
    
}

function populate_user_blogs() {
    user_blogs.forEach(blog => {
        add_user_blog(blog);
    });
}

$(function () {

    $('.all-blogs').on('show', function () {
        $.ajax({
            method: 'GET',
            dataType: 'json',
            headers: {
                'Authorization': 'Token ' + TOKEN
            },
            url: 'http://127.0.0.1:8000/api/blog/' + USERNAME,
            success: function (result) {
                user_blogs = result;
                populate_user_blogs();
            }
        });
    });

});
