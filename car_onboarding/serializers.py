from rest_framework import serializers
from .models import *
# serializers.py


class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadedFile
        fields = ['file']

class CarImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImage
        fields = ['image']

class CarListingSerializer(serializers.ModelSerializer):
    images = serializers.ListField(
        child=serializers.URLField(),
        required=False,
        help_text="List of image URLs"
    )

    class Meta:
        model = CarListing
        fields = '__all__'
        read_only_fields = ['user']  # user is set automatically

    def create(self, validated_data):
        user = self.context['request'].user  # get user from request context (from JWT)
        validated_data['user'] = user
        return super().create(validated_data)