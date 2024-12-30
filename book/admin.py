# admin.py

from django.contrib import admin
from .models import Click
from .models import Rectangle

class ClickAdmin(admin.ModelAdmin):
    list_display = ('stall_number', 'events')  # Add fields to display
    search_fields = ('stall_number', 'events')  # Add search capability
    list_filter = ('events',)  # Filter by events

# Register the model with custom admin class
admin.site.register(Click, ClickAdmin)

class RectangleAdmin(admin.ModelAdmin):
    list_display = ('index', 'x', 'y', 'width', 'height')  # Fields to display
    search_fields = ('index', 'x', 'y')  # Add search capability
    list_filter = ('width', 'height')  # Add filtering capability

# Register the model with the custom admin class
admin.site.register(Rectangle, RectangleAdmin)
