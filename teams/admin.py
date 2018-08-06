from django.contrib import admin
from .models import Team, Player, BattingAverage, BowlingAverage, Photo, Format


@admin.register(Format)
class FormatAdmin(admin.ModelAdmin):
    list_display = ['id', 'text']
    list_filter = ['text']


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'content_type', 'object_id']
    list_filter = ['content_type']


@admin.register(BattingAverage)
class BattingAverageAdmin(admin.ModelAdmin):
    list_display = ['id', 'player', 'average', 'runs', 'strike_rate', 'hundreds', 'highest_score', 'is_active']
    list_filter = ['format']


@admin.register(BowlingAverage)
class BowlingAverageAdmin(admin.ModelAdmin):
    list_display = ['id', 'player', 'wickets', 'economy', 'strike_rate', 'is_active']
    list_filter = ['format']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ranking', 'type', 'is_active']
    list_filter = ['ranking', 'type']
    search_fields = ['name']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ranking', 'playing_role', 'is_active']
    list_filter = ['name', 'ranking', 'formats']
    search_fields = ['name']
