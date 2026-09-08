from django.urls import path
from . import views

urlpatterns = [
    path("", views.prospect_dashboard, name="prospect_dashboard"),
    path("prospect/new", views.add_new_prospect, name="add_new_prospect"),
    path("prospect/<int:pk>/", views.prospect_detail, name="prospect_detail"),
    path("prospect/<int:pk>/update/", views.update_prospect, name="update_prospect"),
]
