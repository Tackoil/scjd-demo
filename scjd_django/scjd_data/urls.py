from django.urls import path

from . import views

urlpatterns = [
    path('patent-pie/', views.patent_pie),
]