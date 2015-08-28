# from django.contrib import admin
# from web.posts.admin import PostInline, RequestInline, PostViewInline
# from web.users.models import User, Address
#
#
# class UserAdmin(admin.ModelAdmin):
#     inlines = [PostInline, RequestInline, PostViewInline]
#     list_display = ('email', 'first_name', 'last_name', 'gender', 'complete_address', 'is_active', 'is_admin')
#     list_filter = ('email', 'first_name', 'last_name', 'gender', 'is_active', 'is_admin')
#     search_fields = ('first_name', 'last_name', 'email', 'address__route',
#                      'address__state', 'address__city', 'address__country')
#
#     # noinspection PyMethodMayBeStatic
#     def complete_address(self, user):
#         return 'Street# %s, %s, %s, %s, %s' % (user.address.street, user.address.route, user.address.city,
#                                                user.address.state, user.address.country)
#
#
# class AddressAdmin(admin.ModelAdmin):
#     list_display = ('zip_code', 'street', 'route', 'city', 'state', 'country')
#     list_filter = ('country', 'state', 'city')
#     search_fields = ('zip_code', 'street', 'route', 'city', 'state', 'country')
#
#
# admin.site.register(User, UserAdmin)
# admin.site.register(Address, AddressAdmin)
