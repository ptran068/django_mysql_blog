# posts/models.py
from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.utils.timezone import now
from PIL import Image
from django.conf import settings
#ondelete child data will be deleted wwhen the parent data deleted
User = settings.AUTH_USER_MODEL

class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE,related_name='author')
    liked = models.ManyToManyField(User, default=None, blank=True, related_name='liked')
    image = models.ImageField(blank=True, null=True, upload_to='post_pics')
    caption  = models.CharField(max_length=500)
    created_date = models.DateTimeField(default=timezone.now)
    video = models.FileField(upload_to='video_posts', null=True, blank=True)

    def __str__(self):
        return self.caption

    # def get_absolute_url(self):
    #     return reverse('index', kwargs={'pk':self.pk})

        
#############################################
LIKE_CHOICES =(
    ('Like','Like'),
    ('Unlike','Unlike')

)

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICES, default='Like', max_length=10)

    def __str__(self):
        return str(self.post)

############################################

# class Profile(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE, related_name='profile')
#     image = models.ImageField(default='default.jpg', upload_to='profile_pics')
#     address  = models.CharField(max_length=500)
#     cover_photos = models.ImageField(default='cover3.jpeg',upload_to='cover_pics')
#     follower = models.IntegerField(default=0)
#     following = models.IntegerField(default=0)

#     #in order to display in admin web, if not it is list of objects
#     def __str__(self):
#         return f'{self.user.username} Profile'

    # def get_absolute_url(self):
    #     return reverse('index', kwargs={'pk':self.pk})
###########################################

class Comment(models.Model):
    content = models.TextField(max_length=150)
    date_posted = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    post_connected = models.ForeignKey(Post, on_delete=models.CASCADE)
