from django.db import models

class Post(models.Model):
    
    Category = models.CharField(max_length = 50)
    Content = models.TextField(max_length= 200)
    IsComment = models.BooleanField(default=0)
    Time = models.DateTimeField(auto_now_add=True)
    OwnerUsername = models.CharField(max_length = 50)
    OwnerId = models.IntegerField()
    OwnerName = models.CharField(max_length = 50)
    OwnerSurname = models.CharField(max_length = 50)

class Likes(models.Model):
    PostId = models.IntegerField()
    OwnerId = models.IntegerField()
    LikeStatus = models.IntegerField()
    

class Comments(models.Model):
    CommentsOwner = models.CharField(max_length = 50)
    CommentsOwnerId= models.IntegerField()
    Comment = models.TextField()
    PostId = models.IntegerField()
    CommentTime = models.DateTimeField(auto_now_add=True)

class SavePost(models.Model):
    SaveOwnerId = models.IntegerField()
    SavePostId = models.IntegerField()
    SaveStatus = models.BooleanField(default=False)

class Notification(models.Model):
    NotificationOwner = models.CharField(max_length = 20)
    NotificationOwnerId = models.IntegerField()
    NotificationType = models.CharField(max_length = 20)
    NotificationSentBy = models.CharField(max_length = 20)
    NotificationPostId = models.IntegerField()
    NotificationTime = models.DateTimeField(auto_now_add=True)
    NotificationStatus = models.BooleanField(auto_created=False)
