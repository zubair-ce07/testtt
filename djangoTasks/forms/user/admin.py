from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model

from user import models
from user import forms

USER = get_user_model()


class ProductPriceFilter(admin.SimpleListFilter):

    title = 'Price'
    parameter_name = ('price', )

    def lookups(self, request, model_admin):

        return (
            ('1', '1-360'),
            ('2', '361-660'),
            ('3', '661-960'),
        )

    def queryset(self, request, queryset):

        lower_limit = 1
        higher_limit = 960

        if self.value() == '1':
            lower_limit = 1
            higher_limit = 360
        if self.value() == '2':
            lower_limit = 1
            higher_limit = 360
        if self.value() == '3':
            lower_limit = 1
            higher_limit = 360

        return queryset.filter(price__gte=lower_limit, price__lte=higher_limit)


class ProductAdmin(admin.ModelAdmin):

    form = forms.ProductForm
    list_display = ('title', 'description', 'price', 'owner')
    list_filter = ('owner', ProductPriceFilter)
    search_fields = ('title', 'description', 'price', )
    fields = ('title', 'price', 'description', 'owner')


class UserProfileAdmin(admin.ModelAdmin):

    form = forms.UserProfileForm
    list_display = ('user', 'country', 'state', 'city', 'birthday', 'age_year')
    fields = ('country', 'state', 'city', 'birthday', 'user')
    list_filter = ('country', 'state', 'city',)
    search_fields = ('country', 'state', 'city', 'age_year')
    date_hierarchy = 'birthday'
    list_per_page = 5


class MyUserAdmin(admin.ModelAdmin):

    form = forms.RegistrationForm
    list_per_page = 5
    list_display = (
        'username', 'first_name', 'last_name', 'email',
        'gender', 'is_active', 'is_staff', 'is_superuser',
        'date_joined',
    )
    list_filter = (
        'is_active', 'gender', 'is_staff', 'date_joined',
        'userprofile__city',
    )
    search_fields = ('gender', 'first_name', 'userprofile__city')
    fields = (
        'username', 'first_name', 'last_name', 'email',
        'gender', 'password', 'is_staff',
        'is_active', 'is_superuser'
    )

admin.site.register(USER, MyUserAdmin)
admin.site.register(models.Product, ProductAdmin)
admin.site.register(models.UserProfile, UserProfileAdmin)
