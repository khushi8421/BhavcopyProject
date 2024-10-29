
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EquityRecordViewSet, home_view

router = DefaultRouter()
router.register(r'equityrecords', EquityRecordViewSet)  # Automatically creates CRUD routes

urlpatterns = [
    path('', home_view, name='home'),  
    #path('download/', DownloadBhavcopy.as_view(), name='download_bhavcopy'),
    path('', include(router.urls)),  # CRUD routes
]




