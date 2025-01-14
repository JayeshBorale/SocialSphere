from django.db import models

from django.contrib.auth.models import User

class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE , related_name="profile")
    bio=models.CharField(max_length=200)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    followers=models.ManyToManyField(User,symmetrical=False,related_name="following")
    private_account = models.BooleanField(default=False)
    

    def __str__(self) :
        return self.user.username
    
    def is_followed_by(self, user):
        return self.followers.filter(id=user.id).exists()
    

    
class User_Posts(models.Model):
    user=models.ManyToManyField(User,related_name="post_user")
    body=models.CharField(max_length=300)
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="liked_posts", blank=True)

    def __str__(self):
        
        return f"{self.body[:20]}... by {', '.join([u.username for u in self.user.all()])}"



class Comment(models.Model):
    post = models.ForeignKey(User_Posts, on_delete=models.CASCADE, related_name="comments")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.text[:30]}..."
class notification(models.Model):
    user=models.ManyToManyField(User)
    body=models.CharField(max_length=100)

    def __str__(self) :
        return self.body

    