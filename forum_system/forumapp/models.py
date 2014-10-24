from django.db import models
from django.contrib.auth.models import User

# Create your models here.



# below is database models to our project




GENDER_CHOICES = (
    (0, 'male'),
    (1, 'female'),
    (2, 'not specified'),
)

class UserProfile(models.Model):
    user = models.OneToOneField(User) 
    uni_id =  models.CharField(max_length = 9) # eg.312046529  
    gender = models.IntegerField(choices=GENDER_CHOICES,default=2)
    is_Academics = models.BooleanField() # true or false 
    topic_count = models.IntegerField(default=0, blank=True)
    post_count = models.IntegerField(default=0, blank=True)
    descrip = models.CharField(max_length = 200) 
    # need to install python pil , do it if and only if we have time
    #img=models.ImageField(upload_to = 'pic_folder/', default = 'pic_folder/None/no-img.jpg')

    def __unicode__(self):
        return self.user.username



# forum module


class Category(models.Model):
    category_name = models.CharField(max_length=20, blank=True)
    create_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.category_name

class Thread(models.Model):

    is_intrash = models.BooleanField(default=False) # true or false 
    title = models.CharField(max_length=50)
    replies = models.IntegerField(default=0) 
    views = models.IntegerField(default=0) 
    author = models.ForeignKey(User)  
    category = models.ManyToManyField(Category, blank=True)
    like = models.IntegerField(default = 0) # .. same as facebook "like" counter
    content = models.TextField()

    lastpost = models.DateTimeField(auto_now=True)
    update_time = models.DateTimeField(auto_now=True)
    publish_time = models.DateTimeField(auto_now_add=True)

    def isIntrash(self):
        if self.is_intrash == True:
            return True


    def __unicode__(self):
        return u'%s %s %s' % (self.title, self.author, self.publish_time)


class Comment(models.Model):

    like =  models.IntegerField(default = 0)
    content = models.TextField()
    create_time = models.DateTimeField(auto_now_add=True)
    from_user = models.ForeignKey(User, related_name='relationships')
    to_user = models.ForeignKey(User, related_name='related_to')
    to_thread = models.ForeignKey(Thread)



    def __unicode__(self):
        return self.content



# course review module


class Subject(models.Model):
    subject_name = models.CharField(max_length = 100) # Software platforms..
    subject_code = models.CharField(max_length = 8) # ELEC3609
    lecturer = models.CharField(max_length = 50)
    rating = models.IntegerField() # .. out of 5

    def __unicode__(self):
        return self.subject_code

class Review(models.Model):

    subject_code = models.ForeignKey(Subject)
    author = models.ForeignKey(User)
    title = models.CharField(max_length=50)
    content = models.TextField()
    rating = models.IntegerField() # .. out of 5
    update_time = models.DateTimeField(auto_now=True)
    publish_time = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return u'[%s] %s %s %s' % (self.subject_code, self.title, self.author, self.publish_time)



# whiteboard module

class Document(models.Model):
    uploader = models.ForeignKey(User)
    resource_title = models.CharField(max_length=50)
    upload_date = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length = 100) # XXX.txt XX.doc ..

    def __unicode__(self):
        return self.resource_title


class Video(models.Model):

    uploader = models.ForeignKey(User)
    resource_title = models.CharField(max_length=50)
    video_url = models.CharField(max_length = 200)
    upload_date = models.DateTimeField(auto_now_add=True)


    def __unicode__(self):
        return self.resource_title

