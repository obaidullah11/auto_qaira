from django.urls import path
from .views import PrivacyPolicyView, PrivacyPolicyRetrieveView,TermandpolicyRetrieveView,TermandpolicyView

urlpatterns = [
    path('admin/privacy-policy/', PrivacyPolicyView.as_view(), name='privacy-policy-update'),
    path('privacy-policy/', PrivacyPolicyRetrieveView.as_view(), name='privacy-policy-get'),
    path('admin/terms-and-conditions/', TermandpolicyView.as_view(), name='terms-and-conditions-update'),
    path('terms-and-conditions/', TermandpolicyRetrieveView.as_view(), name='terms-and-conditions-get'),
]
