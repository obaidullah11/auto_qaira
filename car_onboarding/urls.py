from django.urls import path
from .views import *

urlpatterns = [
    path('add/', CarListingCreateView.as_view(), name='carlisting-create'),
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('api/cars/', CarListingList.as_view(), name='car-list'),
    path('api/my-cars/', UserCarListing.as_view(), name='my-car-list'),
    path('api/cars/<int:pk>/', CarListingDetail.as_view(), name='car-detail'),

    
]
