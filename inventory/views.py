from django.views.generic import ListView
from django.db.models import Q, F
from datetime import date, timedelta
from .models import Medicine

class MedicineListView(ListView):
    """
    An enhanced view to display a list of all medicines,
    with added functionality for searching, sorting, and filtering.
    """
    model = Medicine
    template_name = 'inventory/medicine_list.html'
    context_object_name = 'medicines'
    paginate_by = 25

    def get_queryset(self):
        """
        Overrides the default queryset to implement filtering, searching, and sorting.
        """
        queryset = super().get_queryset()
        
        # Get query parameters from the URL
        query = self.request.GET.get('q')
        sort_by = self.request.GET.get('sort', 'name') # Default sort by name
        direction = self.request.GET.get('dir', 'asc') # Default direction ascending
        filter_by = self.request.GET.get('filter')

        # 1. Filtering Logic
        today = date.today()
        if filter_by == 'near_expiry':
            ninety_days_from_now = today + timedelta(days=90)
            queryset = queryset.filter(
                expiration_date__gte=today,
                expiration_date__lte=ninety_days_from_now
            )
        elif filter_by == 'expired':
            queryset = queryset.filter(expiration_date__lt=today)
        elif filter_by == 'out_of_stock':
            queryset = queryset.filter(quantity=0)
        elif filter_by == 'low_stock':
            # Filter where quantity is less than or equal to the threshold field
            queryset = queryset.filter(quantity__lte=F('low_stock_threshold'))

        # 2. Searching Logic
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(composition__icontains=query) |
                Q(category__icontains=query)
            ).distinct()

        # 3. Sorting Logic
        if sort_by in ['name', 'category', 'quantity', 'expiration_date']:
            if direction == 'desc':
                sort_by = f'-{sort_by}'
            queryset = queryset.order_by(sort_by)
            
        return queryset

    def get_context_data(self, **kwargs):
        """
        Passes the current query parameters to the template for building URLs.
        """
        context = super().get_context_data(**kwargs)
        # Pass all GET parameters to the template
        context['query_params'] = self.request.GET.urlencode()
        context['current_query'] = self.request.GET.get('q', '')
        context['current_filter'] = self.request.GET.get('filter', '')
        context['current_sort'] = self.request.GET.get('sort', 'name')
        context['current_dir'] = self.request.GET.get('dir', 'asc')
        return context

