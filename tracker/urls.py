from django.urls import path 
from . import views 

urlpatterns = [
    path("pick", views.pick_stocks, name = "pick"),
    path("selected_stocks", views.selected_stocks_to_track, name="selected_stocks")
]

