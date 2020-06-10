from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import pre_save
from fback.utils import unique_slug_generator


# Create your models here.
class College(models.Model):
    user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    name=models.CharField(max_length=50)
    place=models.CharField(max_length=30)
    valid=models.BooleanField(null=True,default=False)

    def __str__(self):
        return self.name
class Course(models.Model):
    college_n=models.ForeignKey(College,on_delete=models.CASCADE)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    name=models.CharField(max_length=20)
    year=models.IntegerField()
    subjects=models.CharField(max_length=150)
    class Meta:
        unique_together=('college_n','name','year')
    def __str__(self):
        return self.name
class Student(models.Model):
    college_n=models.ForeignKey(College,on_delete=models.CASCADE)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    name=models.CharField(max_length=50)
    number=models.CharField(max_length=20)
    phone=models.CharField(max_length=10)
    course_n=models.ForeignKey(Course,on_delete=models.CASCADE)
    email=models.EmailField()
    valid=models.BooleanField(default=False,editable=False)

    class Meta:
        unique_together=('college_n','number')

    def __str__(self):
        return self.name

class Faculty(models.Model):
    college_n=models.ForeignKey(College,on_delete=models.CASCADE)
    slug = models.SlugField(max_length = 250, null = True, blank = True)
    empid=models.CharField(max_length=30)
    name=models.CharField(max_length=30)
    email=models.EmailField(null=True)
    image=models.ImageField(upload_to="media/",null=True)
    class Meta:
        unique_together=('college_n','empid')

    def __str__(self):
        return self.name



class Teach(models.Model):
    college_n=models.ForeignKey(College,on_delete=models.CASCADE)
    course_n=models.ForeignKey(Course,on_delete=models.CASCADE)

    subject=models.CharField(max_length=30)

    faculty_n=models.ForeignKey(Faculty,null=True,on_delete=models.SET_NULL)
    class Meta:
        unique_together=('college_n','course_n','subject')
class Feed(models.Model):
    college_n=models.ForeignKey(College,on_delete=models.CASCADE)
    student_n=models.ForeignKey(Student,on_delete=models.CASCADE)
    faculty_n=models.ForeignKey(Faculty,on_delete=models.CASCADE)
    subject=models.CharField(max_length=40)
    ct=models.IntegerField()
    b=models.IntegerField()
    ec=models.IntegerField()
    t=models.IntegerField()
    sc=models.IntegerField()
    month=models.CharField(max_length=20)
    year=models.CharField(max_length=4)

    date=models.DateField(auto_now_add=True)

    class Meta:
        unique_together=('college_n','student_n','faculty_n','subject','month','year')


class Ef(models.Model):
    student_n=models.ForeignKey(Student,on_delete=models.CASCADE)
    college_n=models.ForeignKey(College,on_delete=models.CASCADE)
    extra_feed=models.CharField(max_length=200,null=True)

def slug_genarator(sender,instance,*args,**kwargs):
    if not instance.slug:
       instance.slug = unique_slug_generator(instance)







pre_save.connect(slug_genarator,sender=Student)
pre_save.connect(slug_genarator,sender=College)
pre_save.connect(slug_genarator,sender=Faculty)
pre_save.connect(slug_genarator,sender=Course)
