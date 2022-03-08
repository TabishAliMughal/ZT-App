from django.contrib.gis.db import models
from Blog.Blog.models import Blog
from django.contrib.auth.models import User

class ReactTypes(models.Model):
    name = models.CharField(max_length=15)
    icon = models.CharField(max_length=25)
    points_add = models.IntegerField()
    points_subtract = models.IntegerField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'React Types'

class Post(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=500,blank=True,null=True)
    text = models.CharField(max_length=50000,blank=True,null=True)
    image = models.FileField(upload_to='blogs/post/',blank=True,null=True)
    video = models.URLField(blank=True,null=True)
    sound = models.FileField(upload_to='blogs/post/',blank=True,null=True)
    blog = models.ForeignKey(Blog , on_delete=models.CASCADE)
    time = models.DateTimeField(auto_created=True,auto_now_add=True)
    views = models.IntegerField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Posts'

class PostReact(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.IntegerField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    react = models.ForeignKey(ReactTypes , on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Reacts'
    def __str__(self):
        return "{} > {}".format(self.post,self.react)

class PostComment(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.IntegerField()
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    comment = models.CharField(max_length=250)
    class Meta:
        verbose_name_plural = 'Comments'
    def __str__(self):
        return "{} > {}".format(self.post,self.comment)
