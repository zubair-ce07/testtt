from django.contrib import admin
from .models import Team
from .models import Player, BattingAverage, BowlingAverage

# Register your models here.

admin.site.register(Player)
admin.site.register(Team)


@admin.register(BattingAverage)
class BattingAverageAdmin(admin.ModelAdmin):
    list_display = ['id', 'player', 'highest_score', 'average', 'hundreds']
    list_filter = ['format']
    search_fields = ['player']


@admin.register(BowlingAverage)
class BowlingAverageAdmin(admin.ModelAdmin):
    list_display = ['id', 'player', 'wickets', 'economy']
    list_filter = ['format']
    search_fields = ['player']


