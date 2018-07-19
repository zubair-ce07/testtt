from django.contrib import admin
from .models import Player, PlayerFollows, PlayerComments
from .models import Team, TeamFollows, TeamComments
from .models import User
from .models import Article, ArticleFollows, ArticleComments


# Register your models here.

admin.site.register(Player)
admin.site.register(Team)
admin.site.register(User)
admin.site.register(Article)
admin.site.register(PlayerFollows)
admin.site.register(PlayerComments)
admin.site.register(TeamFollows)
admin.site.register(TeamComments)
admin.site.register(ArticleFollows)
admin.site.register(ArticleComments)
