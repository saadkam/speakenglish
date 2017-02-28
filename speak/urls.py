from django.conf.urls import url, include
from django.contrib import admin
from . import views

urlpatterns = [
    #url(r'^',include('speak.urls.py'))     For home use later
    url(r'^quiz/$', views.quizes, name='quizes'), #must delet only temp
    url(r'^lessons/$', views.LessonView, name='lessons'),
    url(r'^quiz/(?P<Q_ID>[0-9]+)/$', views.quiz, name='quiz'),
    url(r'^lessons/(?P<LessonId>[0-9]+)/$', views.LessonView_ID, name='lesson_id'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^login/$', views.signin, name='login'),
    url(r'^$', views.index, name='home'),
    url(r'^logout/$', views.signout, name='signout'),
    url(r'^practice/$', views.practice, name='practice'),
    url(r'^practice/(?P<Q_ID>[0-9]+)/$', views.practice_id, name='practice_id'),
    url(r'^account/$', views.account, name='accounts'),
    url(r'^about/$', views.aboutUs, name='aboutUs'),
    url(r'^auth/(?P<username>[\w\-]+)/(?P<code>[\w\-]+)/$', views.activate, name='activate'),
    url(r'^forgotten/$', views.forgotten, name='forgotten'),
    url(r'^newpassword/(?P<username>[\w\-]+)/(?P<code>[\w\-]+)/$', views.newpassword, name='newpassword'),
    url(r'^changepassword/$', views.changepassword, name='changepassword'),
    url(r'^sampleLessons/$', views.sampleLessons, name='sampleLessons'),
    url(r'^samplePractice/$', views.samplePractice, name='samplePractice'),
    url(r'^sampleQuiz/$', views.sampleQuiz, name='sampleQuiz'),
    url(r'^sampleLesson/1/$', views.sampleLesson1, name='sampleLesson1'),
    url(r'^sampleLesson/2/$', views.sampleLesson2, name='sampleLesson2'),
    url(r'^sampleLesson/3/$', views.sampleLesson3, name='sampleLesson3'),
    url(r'^samplePractice/1/$', views.samplePractice1, name='samplePractice1'),
    url(r'^samplePractice/2/$', views.samplePractice2, name='samplePractice2'),
    url(r'^samplePractice/32/$', views.samplePractice3, name='samplePractice3'),
    url(r'^sampleQuiz/1/$', views.sampleQuiz1, name='sampleQuiz1'),
    url(r'^sampleQuiz/2/$', views.sampleQuiz2, name='sampleQuiz2'),
    url(r'^sampleQuiz/3/$', views.sampleQuiz3, name='sampleQuiz3'),
    url(r'^payment-methods/$', views.paymentmethods, name='paymentmethods'),

]
