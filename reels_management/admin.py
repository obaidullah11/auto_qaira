from django.contrib import admin
from .models import  Reel, ReelComment



@admin.register(Reel)
class ReelAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'user', 'car', 'created_at', 'total_likes_display')
    list_filter = ('user', 'car', 'created_at')
    search_fields = ('title', 'description', 'car__name', 'user__username')

    def total_likes_display(self, obj):
        return obj.total_likes()
    total_likes_display.short_description = 'Likes'

@admin.register(ReelComment)
class ReelCommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'reel', 'user', 'comment', 'created_at')
    list_filter = ('created_at', 'reel', 'user')
    search_fields = ('comment', 'reel__title', 'user__username')
