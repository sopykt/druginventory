from django.views.generic import ListView
from .models import Medicine

class MedicineListView(ListView):
    """
    A view to display a list of all medicines in the inventory.
    """
    model = Medicine
    template_name = 'inventory/medicine_list.html'
    context_object_name = 'medicines'
    paginate_by = 20 # Show 20 medicines per page

    def get_queryset(self):
        """Order medicines by name."""
        return Medicine.objects.all().order_by('name')
