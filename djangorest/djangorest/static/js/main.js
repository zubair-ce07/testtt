function populate_comment(comment) {

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

}

function populate_blog(blog) {

    var blog_post = "<div class=\"post-title\">" +
        "<h1>" + blog.title + "</h1>" +
        "</div>" +

        "<div class=\"post-info\">" +
        "<span>" + blog.created_on + " by <a href=\"#\" target=\"_blank\">" + blog.created_by + "</a></span>" +
        "</div>" +
        "<p>" + blog.text + "</p>";

    $(".blog-post").prepend(blog_post);

}

function add_blog_post(blog) {

    var $blog_post = $("<div class=\"col-md-12 blog-post\" style=\"display: block\";>" +
        "<div class=\"post-title\">" +
        "<a href=\"#\">" +
        "<h1 class='blog-title'>" + blog.title + "</h1>" +
        "</a>" +
        "</div>" +
        "<div class=\"post-info\">" +
        "<span>" + blog.created_on + " by <a href=\"#\" target=\"_blank\">" + blog.created_by + "</a></span>" +
        "</div>" +
        "<p>" + blog.summary + "</p>" +
        "<a href=blogs/" + blog.slug + " class=\"slug button button-style button-anim fa fa-long-arrow-right\"><span>Read More</span></a>" +
        "</div>");
    $(".list-blog").append($blog_post);

}

function populate_blog_page() {

    $.ajax({
        method: 'GET',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/blog/',
        success: function (result) {
            result.forEach(function (blog) {
                add_blog_post(blog);
            });
        }
    });
}

$(function () {

    'use strict';

    /* Preloader */
    $(window).load(function () {
        $('.preloader').delay(800).fadeOut('slow');
    });
    /* Smooth Scroll */
    $('a.smoth-scroll').on("click", function (e) {
        var anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: $(anchor.attr('href')).offset().top - 50
        }, 1000);
        e.preventDefault();
    });
    /* Scroll To Top */
    $(window).scroll(function () {
        if ($(this).scrollTop() >= 500) {
            $('.scroll-to-top').fadeIn();
        } else {
            $('.scroll-to-top').fadeOut();
        }
    });
    $('.scroll-to-top').click(function () {
        $('html, body').animate({
            scrollTop: 0
        }, 800);
        return false;
    });
    /* Tooltip */
    $('[data-toggle="tooltip"]').tooltip();
    /* Popover */
    $('[data-toggle="popover"]').popover();
    /* Ajaxchimp for Subscribe Form */
    $('#mc-form').ajaxChimp();
    /* Video and Google Map Popup */
    $('.video-popup').magnificPopup({
        disableOn: 700,
        type: 'iframe',
        removalDelay: 160,
        preloader: false,
        fixedContentPos: false
    });
    /* Magnific Popup */
    $('.image-popup').magnificPopup({
        type: 'image',
        gallery: {
            enabled: true
        },
        zoom: {
            enabled: true,
            duration: 500
        },
        image: {
            markup: '<div class="mfp-figure portfolio-pop-up">' +
                '<div class="mfp-close"></div>' +
                '<div class="mfp-img"></div>' +
                '<div class="mfp-bottom-bar portfolio_title">' +
                '<div class="mfp-title"></div>' +
                '<div class="mfp-counter"></div>' +
                '</div>' +
                '</div>',
            titleSrc: function (item) {
                return item.el.attr('title');
            }
        }
    });
    /* Image Carousel/Slider */
    $(".image-carousel").owlCarousel({
        items: 1,
        autoPlay: true,
        stopOnHover: false,
        navigation: true,
        navigationText: ["<i class='fa fa-long-arrow-left fa-2x owl-navi'></i>", "<i class='fa fa-long-arrow-right fa-2x owl-navi'></i>"],
        itemsDesktop: [1199, 1],
        itemsDesktopSmall: [980, 1],
        itemsTablet: [768, 1],
        itemsTabletSmall: false,
        itemsMobile: [479, 1],
        autoHeight: false,
        pagination: false,
        loop: true,
        transitionStyle: "fadeUp"
    });
    /* Load More Post */
    $("div.blog-post").slice(0, 4).show();
    $("#load-more-post").on('click', function (e) {
        e.preventDefault();
        $("div.blog-post:hidden").slice(0, 1).slideDown(300);
        if ($("div.blog-post:hidden").length == 0) {
            $('#post-end-message').html('<div class="end">End</div>').fadeIn(800);
            $("#load-more-post").fadeOut(100);
        }
    });
    /* Load More Portfolio */
    $("div.portfolio").slice(0, 2).show();
    $("#load-more-portfolio").on('click', function (e) {
        e.preventDefault();
        $("div.portfolio:hidden").slice(0, 1).slideDown(300);
        if ($("div.portfolio:hidden").length == 0) {
            $('#portfolio-end-message').html('<div class="end">End</div>').fadeIn(800);
            $("#load-more-portfolio").fadeOut(100);
        }
    });


    $('.login-form').validate({
        rules: {
            username: {
                required: true,
            },
            password: {
                required: true,
            }
        },
        messages: {
            username: "Please enter your username",
            password: "Please enter your password"
        },
        submitHandler: function (form) {
            var $login_form = $('.login-form');
            var csrf = $login_form.find("input[name=csrfmiddlewaretoken]").val();
            $.ajax({
                method: 'POST',
                dataType: 'json',
                url: 'http://127.0.0.1:8000/login/',
                contentType: "application/json; charset=utf-8",
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                },
                data: JSON.stringify({
                    username: $login_form.find("input[name=username]").val(),
                    password: $login_form.find("input[name=password]").val(),
                }),
                success: function (result) {
                    window.location.replace("http://127.0.0.1:8000/blogs");
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    $(".login-error").text(XMLHttpRequest.responseJSON['data']);
                }
            });
            return false;
        }

    });


    $('.register-form').validate({
        rules: {
            username: {
                required: true,
            },
            password1: {
                required: true,
            },
            password2: {
                required: true,
            },
            date_of_birth: {
                required: true,
                date: true,
            },
        },
        messages: {
            username: "Please enter your username",
            password: "Please enter your password"
        },
        submitHandler: function (form) {
            var $registration_form = $('.register-form');
            var csrf = $registration_form.find("input[name=csrfmiddlewaretoken]").val();
            $.ajax({
                method: 'POST',
                dataType: 'json',
                url: 'http://127.0.0.1:8000/signup/',
                contentType: "application/json; charset=utf-8",
                beforeSend: function (xhr, settings) {
                    xhr.setRequestHeader("X-CSRFToken", csrf);
                },
                data: JSON.stringify({
                    username: $registration_form.find("input[name=username]").val(),
                    password: $registration_form.find("input[name=password1]").val(),
                    profile: {
                        gender: $registration_form.find("select[name=gender]").val(),
                        address: $registration_form.find("input[name=address]").val(),
                        date_of_birth: $registration_form.find("input[name=date_of_birth]").val()
                    }
                }),
                success: function (result) {
                    $(".message a").trigger("click");
                },
                error: function (XMLHttpRequest, textStatus, errorThrown) {
                    if ("username" in XMLHttpRequest.responseJSON['data']) {
                        $(".register-error").text(XMLHttpRequest.responseJSON['data']['username']);
                    }
                }

            });
            return false;
        }
    });

    // Toogle Login and SignUp Form
    $('.message a').click(function () {
        $('form').animate({
            height: 'toggle',
            opacity: 'toggle'
        }, 'slow');
    });

    $('.circle-button').click(function () {
        $('.blog-content').animate({
            height: 'toggle',
            opacity: 'toggle'
        }, 'slow');
    });


    var slug = window.location.pathname.split('/')[2];
    $.ajax({
        method: 'GET',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/blog/' + slug,
        success: function (result) {
            populate_blog(result.blog);
            result.comments.forEach(function (comment) {
                populate_comment(comment);
            });
        },
        error: function (XMLHttpRequest, textStatus, errorThrown) {}
    });


    $('.cd-form').on('submit', function (event) {
        event.preventDefault();
        var $blog_form = $(this);
        var date = new Date();
        var csrf = $blog_form.find("input[name=csrfmiddlewaretoken]").val();
//        var data = JSON.stringify({
//            "title": $blog_form.find("input[name=title]").val(),
//            "text": $blog_form.find("textarea[name=text]").val(),
//            "summary": $blog_form.find("textarea[name=summary]").val(),
//            "created_on": date.getDate().toString() + '-' + date.getMonth().toString() + '-' + date.getFullYear().toString(),
//            "is_published": $blog_form.find("input[name=is_published]").prop('checked'),
//            "comments_allowed": $blog_form.find("input[name=comments_allowed]").prop('checked'),
//            "is_public": $blog_form.find("input[name=is_public]").prop('checked')
//        });
//        console.log(data);
        $.ajax({
            method: 'POST',
            dataType: 'json',
            url: 'http://127.0.0.1:8000/blog/',
            contentType: "application/json; charset=utf-8",
            beforeSend: function (xhr, settings) {
                xhr.setRequestHeader("X-CSRFToken", csrf);
            },
            data: JSON.stringify({
                "title": $blog_form.find("input[name=title]").val(),
                "text": $blog_form.find("textarea[name=text]").val(),
                "summary": $blog_form.find("textarea[name=summary]").val(),
                "created_on": date.getFullYear().toString() + '-' + date.getMonth().toString() + '-' + date.getDate().toString(),
                "is_published": $blog_form.find("input[name=is_published]").prop('checked'),
                "comments_allowed": $blog_form.find("input[name=comments_allowed]").prop('checked'),
                "is_public": $blog_form.find("input[name=is_public]").prop('checked')
            }),
            success: function (result) {
                add_blog_post(result);
                $(".circle-button").trigger("click");
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                
            }
        });
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
                user_ip: "127.0.0.1"
            }),
            success: function (result) {
                populate_comment(result);
                $(".comment-text").val("");
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {

            }
        });
    });

});
