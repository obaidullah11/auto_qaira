from rest_framework import serializers
from .models import Reel, ReelComment
from car_onboarding.models import CarListing

class ReelCommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = ReelComment
        fields = ['id', 'user', 'comment', 'created_at']

class ReelSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    total_likes = serializers.SerializerMethodField()
    comments = ReelCommentSerializer(many=True, read_only=True)
    car = serializers.PrimaryKeyRelatedField(queryset=CarListing.objects.all())

    class Meta:
        model = Reel
        fields = [
            'id', 'title', 'description', 'video', 'hashtag',
            'user', 'car', 'likes', 'total_likes', 'comments', 'created_at'
        ]
        read_only_fields = ['id', 'user', 'likes', 'total_likes', 'comments', 'created_at']

    def get_total_likes(self, obj):
        return obj.total_likes()
