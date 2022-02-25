from django.db import models



class Candidates(models.Model):
    # user = models.ForeignKey(User,on_delete=models.CASCADE)
    user = models.IntegerField()
    name = models.CharField(max_length=50)
    father_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='relationships/candidate' ,null=True,blank=True)
    date_of_birth = models.DateField()
    age = models.IntegerField()
    Gender = [
        ('Male', 'Male'),
        ('Female', 'Female'),
    ]
    gender = models.CharField(choices=Gender,max_length=200)
    Occupation = [
        ('None', 'None'),
        ('Job', 'Job'),
        ('Business', 'Business'),
    ]
    occupation = models.CharField(choices=Occupation,max_length=200,null=True,blank=True)
    Education = [
        ('Primary', 'Primary'),
        ('Matric', 'Matric'),
        ('Inter', 'Inter'),
        ('Graduation', 'Graduation'),
        ('Masters', 'Masters'),
        ('PHD', 'PHD'),
    ]
    education = models.CharField(choices=Education,max_length=200,null=True,blank=True)
    Living = [
        ('With Family', 'With Family'),
        ('Rent', 'Rent'),
        ('Persional', 'Persional'),
    ]
    living_status = models.CharField(choices=Living,max_length=200,null=True,blank=True)
    cast = models.CharField(max_length=50,null=True,blank=True)
    siblings = models.IntegerField(null=True,blank=True)
    height = models.IntegerField(null=True,blank=True)
    mobile = models.BigIntegerField()
    address = models.CharField(max_length=250)
    cnic = models.BigIntegerField()
    place_of_birth = models.CharField(max_length=50,null=True,blank=True)
    M_Status = [
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Married-Twice', 'Married-Twice'),
        ('Divorced', 'Divorced'),
        ('Divorced-Twice', 'Divorced-Twice'),
    ]
    marital_status = models.CharField(choices=M_Status,max_length=200)
    Parents = [
        ('Alive', 'Alive'),
        ('Mother-Only', 'Mother-Only'),
        ('Father-Only', 'Father-Only'),
        ('Passed', 'Passed'),
    ]
    parents = models.CharField(choices=Parents,max_length=200)
    discription = models.CharField(max_length=500,null=True,blank=True)
    father_occupation = models.CharField(choices=Occupation,max_length=200,null=True,blank=True)
    facebook_id = models.URLField(null=True,blank=True)
    email_address = models.EmailField(null=True,blank=True)
    Religion = [
        ('Muslim', 'Muslim'),
        ('Hindu', 'Hindu'),
        ('Cristian', 'Cristian'),
        ('Other', 'Other'),
    ]
    religion = models.CharField(choices=Religion,max_length=200)
    mother_toungue = models.CharField(max_length=50)
    monthly_income = models.IntegerField(null=True,blank=True)
    matched = models.BooleanField(default=False)
    def __str__(self):
        return self.name
    class Meta:
        verbose_name_plural = 'Candidates'