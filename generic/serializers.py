from rest_framework import serializers
from .models import SitePolicy,Termandpolicy

class SitePolicySerializer(serializers.ModelSerializer):
    class Meta:
        model = SitePolicy
        fields = ['title', 'content']
class SiteTermandpolicy(serializers.ModelSerializer):
    class Meta:
        model = Termandpolicy
        fields = ['title', 'content']
