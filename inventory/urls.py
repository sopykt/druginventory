from django.urls import path
from .views import MedicineListView

app_name = 'inventory'

urlpatterns = [
    path('', MedicineListView.as_view(), name='medicine_list'),
]
