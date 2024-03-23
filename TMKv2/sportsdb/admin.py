from django.contrib import admin
from .models import League, Team, Match, Standing
# Register your models here.

class MatchAdmin(admin.ModelAdmin):
    list_display = ('matchid', 'matchteams', 'leagueid', 'homescore', 'awayscore', 'date')
    list_filter = ('leagueid', 'date')
    search_fields = ('leagueid', 'date')
    ordering = ('leagueid',)

admin.site.register(League)
admin.site.register(Team)
admin.site.register(Match, MatchAdmin)
admin.site.register(Standing)

