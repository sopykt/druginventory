from django.contrib import admin
from .models import Medicine

@admin.register(Medicine)
class MedicineAdmin(admin.ModelAdmin):
    """
    Customizes the Django admin interface for the Medicine model.
    """
    list_display = (
        'name',
        'composition',
        'category',
        'quantity',
        'expiration_date',
        'is_expired',
        'updated_at',
    )
    list_filter = (
        'category',
        'administration_type',
        'count_type',
        'expiration_date',
    )
    search_fields = (
        'name',
        'composition',
        'category',
    )
    fieldsets = (
        ('Medicine Details', {
            'fields': ('name', 'composition', 'category')
        }),
        ('Stock Information', {
            'fields': ('quantity', 'count_type', 'expiration_date')
        }),
        ('Administration', {
            'fields': ('administration_type',)
        }),
        ('Other', {
            'fields': ('remarks',),
            'classes': ('collapse',) # Makes this section collapsible
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
    
    # Custom action to mark items as out of stock
    def make_out_of_stock(self, request, queryset):
        queryset.update(quantity=0)
    make_out_of_stock.short_description = "Mark selected medicines as out of stock"

    actions = [make_out_of_stock]
