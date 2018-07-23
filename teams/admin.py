from django.contrib import admin
from .models import Team
from .models import Player, BattingAverage

# Register your models here.

admin.site.register(Player)
admin.site.register(Team)


@admin.register(BattingAverage)
class BattingAverageAdmin(admin.ModelAdmin):
    list_display = ['id', 'player', 'highest_score', 'average', 'hundreds']
    list_filter = ['match_format']
    search_fields = ['player']

# Register your models here.

