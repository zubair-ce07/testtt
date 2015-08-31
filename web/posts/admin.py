from django.contrib import admin

from web.posts.models import Post, Request, PostView


class PostInline(admin.TabularInline):
    model = Post
    classes = ('grp-collapse grp-closed',)
    extra = 1


class RequestInline(admin.TabularInline):
    model = Request
    classes = ('grp-collapse grp-closed',)
    extra = 1


class PostViewInline(admin.TabularInline):
    model = PostView
    classes = ('grp-collapse grp-closed',)
    extra = 1


class PostAdmin(admin.ModelAdmin):
    inlines = [PostViewInline, RequestInline]
    list_display = ('email', 'name', 'title', 'area', 'address', 'description',
                    'kind', 'contact_number', 'demanded_price', 'is_sold',
                    'sold_on', 'posted_on', 'expired_on')
    list_filter = ('posted_by__email', 'area', 'kind', 'demanded_price', 'is_sold', 'sold_on', 'posted_on', 'expired_on')
    search_fields = ('posted_by__email', 'posted_by__first_name', 'posted_by__last_name',
                     'kind', 'title', 'description', 'location__route', 'location__state',
                     'location__city', 'location__country')

    # noinspection PyMethodMayBeStatic
    def address(self, post):
        return 'Street# %s, %s, %s, %s, %s' % (post.location.street, post.location.route, post.location.city,
                                               post.location.state, post.location.country)

    # noinspection PyMethodMayBeStatic
    def name(self, post):
        return '%s %s' % (post.posted_by.first_name, post.posted_by.last_name)

    # noinspection PyMethodMayBeStatic
    def email(self, post):
        return post.posted_by.email


class RequestAdmin(admin.ModelAdmin):
    list_display = ('email', 'name', 'post_title', 'message', 'price', 'status', 'requested_on')
    list_filter = ('requested_by__email', 'post__title', 'price', 'status', 'requested_on')
    search_fields = ['requested_by__email', 'requested_by__first_name', 'requested_by__last_name', 'message', 'status']

    # noinspection PyMethodMayBeStatic
    def post_title(self, request):
        return request.post.title

    # noinspection PyMethodMayBeStatic
    def name(self, request):
        return '%s %s' % (request.requested_by.first_name, request.requested_by.last_name)

    # noinspection PyMethodMayBeStatic
    def email(self, request):
        return request.requested_by.email


class PostViewAdmin(admin.ModelAdmin):
    list_display = ('post_viewed_title', 'email', 'name', 'viewed_on')
    list_filter = ('viewed_by__email', 'viewed_by__first_name', 'viewed_by__last_name', 'viewed_on')
    search_fields = ('post_viewed__kind', 'viewed_by__email', 'viewed_by__first_name', 'viewed_by__last_name')

    # noinspection PyMethodMayBeStatic
    def post_viewed_title(self, post_view):
        return post_view.post_viewed.title

    # noinspection PyMethodMayBeStatic
    def name(self, post_view):
        return '%s %s' % (post_view.viewed_by.first_name, post_view.viewed_by.last_name)

    # noinspection PyMethodMayBeStatic
    def email(self, post_view):
        return post_view.viewed_by.email

admin.site.register(Post, PostAdmin)
admin.site.register(Request, RequestAdmin)
admin.site.register(PostView, PostViewAdmin)
