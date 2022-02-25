from django.contrib.gis.db import models
from Creator.models import Creator

class Type(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Types'

class Blog(models.Model):
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='blogs/blog/' )
    type = models.ForeignKey(Type , on_delete=models.CASCADE)
    # user = models.ForeignKey(Creator , on_delete=models.CASCADE)
    user = models.IntegerField()
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Blogs'