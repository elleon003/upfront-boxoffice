from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'presenter', 'event_date','created', 'status']
    list_filter = ['status', 'created', 'presenter']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['presenter']
    date_hierarchy = 'event_date'
    ordering = ['event_date', 'status']
    show_facets = admin.ShowFacets.ALWAYS





































    

