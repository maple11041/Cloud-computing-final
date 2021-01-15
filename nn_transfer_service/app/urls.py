

from . import views
from django.urls import path
from . import api_for_rm

urlpatterns = [
    path('', views.index, name='index'),
    # path('POin', api_for_rm.PoinAPI.as_view(), name='Post PO in file'),
    path('Image', api_for_rm.ImageAPI.as_view(), name='wait for image'),
]