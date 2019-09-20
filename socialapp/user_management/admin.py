from django.contrib import admin

from user_management.models import SocialGroup, UserProfile, AcademicInformation, WorkInformation

admin.register(UserProfile)
admin.register(AcademicInformation)
admin.register(WorkInformation)
admin.register(SocialGroup)
