from django.urls import path

from .views import ref_chooser
from .views.search import SearchView

urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),
    path(
        'reference/choose/<str:app_label>/<str:model_name>/',
        ref_chooser.choose,
        name='ref_choose'),
    path(
        'reference/choose/', ref_chooser.choose,
        name='ref_choose'),
    path(
        'reference/choose/<str:pk>/',
        ref_chooser.chosen, name='ref_chosen'),
]
