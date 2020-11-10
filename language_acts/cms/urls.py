from django.urls import path
from .views.search import SearchView
from .views import ref_chooser


urlpatterns = [
    path('search/', SearchView.as_view(), name='search'),

    path(
        'reference/choose/', ref_chooser.choose,
        name='ref_choose'),
    path(
        'reference/choose/<str:pk>/',
        ref_chooser.chosen, name='ref_chosen'),
]
