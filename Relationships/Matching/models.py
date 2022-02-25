from django.db import models
from django.contrib.auth.models import User
from Relationships.Candidate.models import Candidates


class Match(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.IntegerField()
    male = models.ForeignKey(Candidates,on_delete=models.CASCADE,related_name='male')
    female = models.ForeignKey(Candidates,on_delete=models.CASCADE,related_name='female')
    male_side_agree = models.BooleanField()
    female_side_agree = models.BooleanField()
    active = models.BooleanField()
    processed = models.BooleanField()
    def __str__(self):
        return "{} > {}".format(self.male,self.female)
    class Meta:
        verbose_name_plural = 'Match'