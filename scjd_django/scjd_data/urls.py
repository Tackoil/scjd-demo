from django.urls import path

from . import views

urlpatterns = [
    path('patent-pie/', views.patent_pie),
    path('patent-line-race/', views.patent_line_race),
    path('patent-line/', views.patent_line),
    path('patent-map/', views.patent_map),
    path('news-word-map/', views.news_word_map),
    path('enterprise-bar/', views.enterprise_bar),
    path('ep-alter-line/', views.ep_alter_line),
    path('ep-distribution-pie/', views.ep_distribution_pie),

    # 定义资源上传接口
    path('api/upload/', views.upload),
    # json文件上传接口
    path('file/json_upload/',views.File.as_view())

    # 通用资源CURD接口
    

]