from django.urls import path

from . import views

urlpatterns = [
    path('patent-pie/', views.patent_pie),
    path('patent-line-race/', views.patent_line_race),
    path('patent-line/', views.patent_line),
    path('patent-map/', views.patent_map),
    path('news-word-map/', views.news_word_map)
]