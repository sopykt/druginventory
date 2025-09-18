from django.contrib import admin
from .models import Medicine

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    """
    Customizes the admin interface for the Medicine model.
    """
    list_display = (
        'name', 
        'composition', 
        'category', 
        'quantity', 
        'low_stock_threshold', # Add field to display
        'expiration_date', 
        'is_expired'
    )
    search_fields = ('name', 'composition', 'category')
    list_filter = ('category', 'administration_type', 'expiration_date')
    list_per_page = 25
    
    # Organize the edit form for better usability
    fieldsets = (
        (None, {
            'fields': ('name', 'composition', 'category')
        }),
        ('Stock Details', {
            'fields': ('quantity', 'low_stock_threshold', 'count_type', 'expiration_date')
        }),
        ('Administration', {
            'fields': ('administration_type', 'remarks')
        }),
    )

