function add_blog_post(blog) {

    var $blog_post = $("<div class=\"col-md-12 blog-post\" style=\"display: block\";>" +
        "<div class=\"post-title\">" +
        "<a href=\"single.html\">" +
        "<h1 class='blog-title'>" + blog.title + "</h1>" +
        "</a>" +
        "</div>" +
        "<div class=\"post-info\">" +
        "<span>" + blog.created_on + " by <a href=\"#\" target=\"_blank\">" + blog.created_by.username + "</a></span>" +
        "</div>" +
        "<p>" + blog.summary + "</p>" +
        "<a href=\"single.html\" class=\"button button-style button-anim fa fa-long-arrow-right\"><span>Read More</span></a>" +
        "</div>");

    $(".content-page").append($blog_post);
}



(function ($) {
    'use strict';

    jQuery(document).ready(function () {

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
    });

    /* Populate Blogs */
    $.ajax({
        method: 'GET',
        dataType: 'json',
        url: 'http://127.0.0.1:8000/blog/',
        success: function (blogs) {
            blogs.forEach(function (blog) {
                add_blog_post(blog);
                console.log(blog);
            });
        }
    });
})(jQuery);
