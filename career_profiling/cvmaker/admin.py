from .models import BookMarkCV
from .models import Education
from .models import Experience
from .models import Profile
from .models import Skill
from django.contrib import admin

admin.site.register(BookMarkCV)
admin.site.register(Education)
admin.site.register(Experience)
admin.site.register(Profile)
admin.site.register(Skill)
