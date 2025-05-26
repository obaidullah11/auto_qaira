from django.db import models
from users.models import User
from car_onboarding.models import CarListing




class Reel(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(CarListing, on_delete=models.CASCADE, related_name='reels')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video = models.FileField(upload_to='reels/videos/')
    thumbnail = models.ImageField(upload_to='reels/thumbnails/', null=True, blank=True)
    likes = models.ManyToManyField(User, related_name='liked_reels', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

class ReelComment(models.Model):
    reel = models.ForeignKey(Reel, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
