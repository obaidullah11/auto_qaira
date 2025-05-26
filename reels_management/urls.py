from django.urls import path
from .views import (
    ReelListView,
    ReelUploadView,
    UserReelListView,
    ReelDetailView,
    like_unlike_reel,
    add_comment
)

urlpatterns = [
    path('reels/', ReelListView.as_view(), name='reel-list'),
    path('reels/upload/', ReelUploadView.as_view(), name='reel-upload'),
    path('reels/user/', UserReelListView.as_view(), name='user-reels'),
    path('reels/<int:pk>/', ReelDetailView.as_view(), name='reel-detail'),
    path('reels/<int:reel_id>/like/', like_unlike_reel, name='reel-like'),
    path('reels/<int:reel_id>/comment/', add_comment, name='reel-comment'),
]
