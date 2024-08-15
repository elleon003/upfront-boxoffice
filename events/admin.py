from django.contrib import admin
from .models import Event, Category

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'presenter', 'event_date','created', 'status']
    list_filter = ['status', 'created', 'presenter']
    list_editable = ['price', 'event_date']
    search_fields = ['title', 'description']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['presenter']
    date_hierarchy = 'event_date'
    ordering = ['event_date', 'status']
    show_facets = admin.ShowFacets.ALWAYS

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name']
    prepopulated_fields = {'slug': ('name',)}

































    

