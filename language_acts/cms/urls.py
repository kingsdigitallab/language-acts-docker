from django.urls import path

from .views import ref_chooser
from .views.search import SearchView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),

    path(
        'reference/choose/<str:pk>/',
        ref_chooser.chosen, name='ref_chosen'),
]
