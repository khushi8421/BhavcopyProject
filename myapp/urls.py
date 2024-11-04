

from django.urls import path
from .views import home, download_bhavcopy, search_equity, update_equity, delete_equity,available_dates

urlpatterns = [
    path('', home, name='home'),
    path('download-bhavcopy/', download_bhavcopy, name='download_bhavcopy'),
    path('search-equity/', search_equity, name='search_equity'),
    path('update-equity/', update_equity, name='update_equity'),
    path('delete-equity/', delete_equity, name='delete_equity'),
    path('available_dates/', available_dates, name='available_dates'),
]






