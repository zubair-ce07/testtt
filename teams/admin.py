from django.contrib import admin
from .models import Team, Player, BattingAverage, BowlingAverage, TestModel


# Register your models here.

# admin.site.register(Player)
# admin.site.register(Team)


@admin.register(BattingAverage)
class BattingAverageAdmin(admin.ModelAdmin):
    list_display = ['id', 'player', 'average', 'hundreds', 'highest_score']
    list_filter = ['format']


@admin.register(BowlingAverage)
class BowlingAverageAdmin(admin.ModelAdmin):
    list_display = ['id', 'player', 'wickets', 'economy']
    list_filter = ['format']


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ranking', 'type']
    list_filter = ['ranking', 'type']
    search_fields = ['name']


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'ranking', 'playing_role']
    list_filter = ['name', 'ranking']
    search_fields = ['name']


class TestModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'is_active',)
    list_filter = ('is_active',)
    actions = ['delete_model']

    def delete_model(self, request, queryset):
        # print(queryset)
        queryset.update(is_active=False)

    def queryset(self, request):
        """ Returns a QuerySet of all model instances that can be edited by the
        admin site. This is used by changelist_view. """
        # Default: qs = self.model._default_manager.get_query_set()
        qs = self.model._default_manager.all_with_deleted()
        # TODO: this should be handled by some parameter to the ChangeList.
        ordering = self.ordering or ()  # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs


admin.site.register(TestModel, TestModelAdmin)
