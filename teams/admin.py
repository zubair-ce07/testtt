from django.contrib import admin
from .models import Team, Player, BattingAverage, BowlingAverage, Photo

# Register your models here.


# admin.site.register(TestPhoto)


@admin.register(Photo)
class PlayerTeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'object_id']
    list_filter = ['content_type']


@admin.register(BattingAverage)
class BattingAverageAdmin(admin.ModelAdmin):
    list_display = ['id', 'player', 'average', 'hundreds', 'highest_score', 'is_active']
    list_filter = ['format']


@admin.register(BowlingAverage)
class BowlingAverageAdmin(admin.ModelAdmin):
    list_display = ['id', 'player', 'wickets', 'economy', 'is_active']
    list_filter = ['format']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ranking', 'type', 'is_active']
    list_filter = ['ranking', 'type']
    search_fields = ['name']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ranking', 'playing_role', 'is_active']
    list_filter = ['name', 'ranking']
    search_fields = ['name']


