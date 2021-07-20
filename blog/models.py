from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils.text import slugify
from datetime import datetime

class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Post(models.Model):
    sno=models.AutoField(primary_key=True)
    title=models.CharField(max_length=255)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # categories = models.ForeignKey(Category,on_delete=models.DO_NOTHING,null=True, blank=True)
    categories = models.ManyToManyField(Category)
    views= models.IntegerField(default=0)
    slug = models.SlugField(max_length=250,unique=True)
    timeStamp=models.DateTimeField(auto_now_add=True)
    content=models.TextField()
    def save(self,*args,**kwargs): 
        if len(self.slug)==0:    
            # print('SLUG LENGTH',self.slug)
            t = datetime.now()
            s = t.strftime("%H:%M:%S.%f")
            string = "%s-%s" % (s,self.title)
            self.slug = slugify(string)
        super(Post,self).save() 

    def __str__(self):
        return self.title + " by " + self.author.username

class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    comment=models.TextField()
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post=models.ForeignKey(Post, on_delete=models.CASCADE)
    parent=models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.comment[0:15] +"... by "+self.user.username

class User(AbstractUser):
    posts = models.ForeignKey(Post, on_delete=models.CASCADE,null=True)