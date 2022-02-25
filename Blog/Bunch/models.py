from django.contrib.gis.db import models
from Blog.Blog.models import Blog
from Blog.Post.models import Post


class Bunch(models.Model):
    name = models.CharField(max_length=50)
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Bunches'
    def __str__(self):
        return self.name

class BunchPost(models.Model):
    bunch = models.ForeignKey(Bunch,on_delete=models.CASCADE)
    post = models.ForeignKey(Post,on_delete=models.CASCADE)
    class Meta:
        verbose_name_plural = 'Bunch Posts'
    def __str__(self):
        return "{} > {}".format(self.bunch,self.post)



