from django.db import models
from Blog.Blog.models import Blog
from Blog.Post.models import Post


class Tags(models.Model):
    name = models.CharField(max_length=25)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Tags'


class BlogTags(models.Model):
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags , on_delete=models.CASCADE)
    def __str__(self):
        return self.tag.name
    class Meta:
        verbose_name_plural = 'Blog Tags'

class PostTags(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags , on_delete=models.CASCADE)
    def __str__(self):
        return self.tag.name
    class Meta:
        verbose_name_plural = 'Post Tags'
