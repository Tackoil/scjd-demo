from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from chart_data import views
from django.urls import include, path
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'files', views.FileHistoryViewSet)

urlpatterns = [
    path('', include(router.urls))
]

urlpatterns += [
    url(r'^charts/$', views.ChartList.as_view()),
    url(r'^charts/(?P<pk>[0-9]+)/$', views.ChartDetail.as_view()),
    url(r'^display/$', views.DisplayAPIView.as_view()),
]

