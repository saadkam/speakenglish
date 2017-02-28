# Create your models here.
from django.contrib.auth.models import Permission, User
from django.db import models


class Lesson(models.Model):
    Name = models.CharField(max_length=250)

    def __str__(self):
        return 'Lesson: ' + self.Name


class Audio(models.Model):
    Lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    Audio_Text = models.TextField()
    Audio_File = models.FileField()
    Audio_Urdu = models.TextField(max_length=2000)

    def __str__(self):
        return 'Audio: ' + self.Audio_Text


class UserInfo(models.Model):
    user = models.OneToOneField(User, unique=True, primary_key=True)
    Address = models.TextField()
    DateRegistered = models.DateTimeField(auto_now_add=True)
    Phone = models.CharField(max_length=20)
    Code = models.CharField(max_length=30)

    def __id__(self):
        return self.id

    def __str__(self):
        return 'User:' + str(self.user.id) + ' ' +self.user.username

class Payments(models.Model):
    userinfo= models.ForeignKey(UserInfo, on_delete=models.CASCADE)
    Payment_Ammount= models.IntegerField()
    date= models.DateTimeField(auto_now_add=False, editable=True, )
    Expiry= models.DateTimeField(auto_now_add=False, editable=True, )

class Testing(models.Model):
    Lesson = models.OneToOneField(Lesson, unique=True, primary_key=True)
    Name = models.CharField(max_length=250)
    Publication = models.DateTimeField(auto_now_add=True)
    Required_Score = models.IntegerField(default=100)

    def __id__(self):
        return self.Lesson.id

    def __str__(self):
        return 'Test: ' + self.Name


class Sitting(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Test = models.ForeignKey(Testing, on_delete=models.CASCADE)
    Score = models.IntegerField(default=0)
    Passed = models.BooleanField(default=False)
    Time_Stamp = models.DateTimeField(auto_now=True)

    def __id__(self):
        return  self.Test.__id__()

    def __str__(self):
        return self.user.username +' Test: ' + str(self.Test.Lesson.id) + ' Score ' + str(self.Score)


class Question(models.Model):
    Testing = models.ForeignKey(Testing, on_delete=models.CASCADE)
    Question_Text = models.TextField(help_text='This is the question')

    def __str__(self):
        return self.Question_Text


class MCQ(models.Model):
    MCQ_Text = models.TextField(help_text='This is the MCQ')
    Is_Correct = models.BooleanField(help_text='True if correct else false')
    Question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def __str__(self):
        return self.MCQ_Text + ' = ' + str(self.Is_Correct)

    def __IsTrue__(self):
        return self.Is_Correct


