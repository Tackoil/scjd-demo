from django.urls import include, path
from rest_framework import routers
from . import views


urlpatterns = [

    # 图表模拟数据接口
    path('patent-pie/', views.patent_pie),
    path('patent-line-race/', views.patent_line_race),
    path('patent-line/', views.patent_line),
    path('patent-map/', views.patent_map),
    path('news-word-map/', views.news_word_map),
    path('enterprise-bar/', views.enterprise_bar),
    path('ep-alter-line/', views.ep_alter_line),
    path('ep-distribution-pie/', views.ep_distribution_pie),

]