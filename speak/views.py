import math
import smtplib
from datetime import timedelta, datetime, timezone
from random import choice
from string import ascii_uppercase

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.utils.timezone import is_aware

from .forms import NewUserForm, UserForm
from .models import Testing, Question, MCQ, Sitting, Lesson, Audio, UserInfo, Payments
from django.core.urlresolvers import reverse
import copy
# Create your views here.


def index(request):
    username = request.user.username
    return render(request, 'speak/home.html', {'username': username})


def activate(request,username,code):
    user = User.objects.get(username=username)
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    User_Info= UserInfo.objects.get(user=user)
    if User_Info.Code == str(code):
        user.is_active=True
        user.save()
        new_code=(''.join(choice(ascii_uppercase) for i in range(20)))
        User_Info.Code=new_code
        User_Info.save()
        login(request, user)
        return HttpResponseRedirect(reverse('home'))
    else:
        return render(request,'speak/error.html')



def newpassword(request,username,code):
    if request.method == 'POST':
        pswrd=request.POST['password']
        rep_pswrd= request.POST['repeat-password']
        user = User.objects.get(username=username)
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        User_Info= UserInfo.objects.get(user=user)
        if User_Info.Code == str(code):
            if pswrd!=rep_pswrd:
                return render(request,'speak/error.html',{'message':'Wrong repeated password'})
            user.set_password(pswrd)
            user.save()
            new_code=(''.join(choice(ascii_uppercase) for i in range(20)))
            User_Info.Code=new_code
            print(new_code)
            User_Info.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request,'speak/error.html')
    else:
        return render(request, 'speak/newpassword.html', {'username':username,'code':code})


def forgotten(request):
    if request.method == 'POST':
        Username = request.POST['username']
        email = request.POST['email']
        code=(''.join(choice(ascii_uppercase) for i in range(20)))
        if User.objects.filter(username=Username).exists():
            userr=User.objects.get(username=Username)
            user_Info=UserInfo.objects.get(user=userr)
            code=user_Info.Code
            Username=userr.username
            gmail_user = 'no-reply@easyspokenenglish.com.pk'
            gmail_pwd = 'K4ksc#8g'
            FROM = 'no-reply@easyspokenenglish.com.pk'
            Link= "easyspokenenglish.com.pk/newpassword/"+Username+"/"+code
            TO = str(userr.email)
            SUBJECT = 'Password Renewal'
            TEXT = "Click the link below to change your password \n" \
                   "%s" %Link
            # Prepare actual message
            message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, "".join(TO), SUBJECT, TEXT)
            try:
                server = smtplib.SMTP("smtp.easyspokenenglish.com.pk", 587)
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                server.close()
                print('successfully sent the mail forgotten')
            except:
                print ("failed to send mail")
            return render(request, 'speak/email.html')
        else:
            return render(request,'speak/error.html',{'message':'Wrong Username was entered'})
    else:
        return render(request, 'speak/forgotten.html')



@login_required(login_url='/payment-methods/')
def account(request):
    username= request.user
    user_id= username.id
    User_Info= UserInfo.objects.get(user=request.user)
    DateRegisterd= User_Info.DateRegistered
    Address= User_Info.Address
    Phone= User_Info.Phone
    User_Payments= Payments.objects.filter(userinfo=User_Info)

    ############################################### Ali Make this presentable ########################################
    return render(request, 'speak/accounts.html',{'UserName':username,'User_ID':user_id,'User_Info':User_Info,
                                                  'User_Payments':User_Payments, 'username':username})


@login_required(login_url='/login/')
def changepassword(request):
    if request.method == 'POST':
        user = request.user
        new_passw= request.POST['password']

        repassw= request.POST['repeat-password']
        if new_passw == repassw:
            user.set_password(new_passw)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            return render(request, 'speak/error.html',{'message':'password did not match'})
    else:
        return render(request, 'speak/changepassword.html')


@login_required(login_url='/sampleLessons/')
def LessonView(request):
    taken = Sitting.objects.filter(user=request.user).filter(Passed=True)
    username = request.user.username
    highest = 0
    for Tests in taken:
        if Tests.__id__()>highest:
            highest = Tests.__id__()
    try:
        Show_lessons = Lesson.objects.filter(id__lte=highest+1)
    except:
        Show_lessons = Lesson.objects.filter(id__lte=highest)

    return render(request, 'speak/Lessons.html', {'Lessons': Show_lessons, 'username': username})


@login_required(login_url='/login/')
def LessonView_ID(request, LessonId):
    taken = Sitting.objects.filter(user=request.user).filter(Passed=True)
    LessonId= int(LessonId)
    highest= 1
    for Tests in taken:
        if Tests.__id__()>highest:
            highest= Tests.__id__()
        highest += 1
    if LessonId>highest:
        return HttpResponseNotFound('<h1>Page not found</h1>')
    lesson= get_object_or_404(Lesson, pk=LessonId)
    audio= Audio.objects.filter(Lesson=lesson)
    url=(audio.first()).Audio_File.url
    username = request.user.username
    #return HttpResponse(url)
    return render(request, 'speak/lesson_id.html', {'Lesson':lesson, 'Audios': audio, 'username': username})


@login_required(login_url='/samplePractice/')
def practice(request):
    taken = Sitting.objects.filter(user=request.user).filter(Passed=True)
    highest= 0
    for Tests in taken:
        if Tests.__id__()>highest:
            highest=Tests.__id__()
    try:
        Show_quiz = Testing.objects.filter(Lesson_id__lte=highest+1)
    except:
        Show_quiz = Testing.objects.filter(Lesson_id__lte=highest)
    username = request.user.username
    return render(request, 'speak/practice.html', {'Quizes': Show_quiz, 'username': username})

@login_required(login_url='/login/')
def practice_id(request,Q_ID):
    if request.method == 'POST':
        score=0
        #ans=request.POST['Quest_dic' ]
        Ans= copy.deepcopy(request.POST)
        del Ans['csrfmiddlewaretoken']
        Keys=Ans.keys()
        #mcq_list = request.POST.getlist('Quest_dic')
        for key in Keys:
            id=Ans[key]
            MCQ_Ans=MCQ.objects.get(pk=id)
            if MCQ_Ans.__IsTrue__():
                score+=1

        ##############################################################################################################
        ######################    Stor the score in sitting ##########################################################
        ######################      Return to score page    ##########################################################
        ##############################################################################################################

        return HttpResponse('ans.key' + str(score))
    else:
        Test = get_object_or_404(Testing, pk=Q_ID)
        Questions_set = Question.objects.all().filter(Testing=Test)
        que = ''
        mcs = ''
        Quetions_dic = {}

        for Questions in Questions_set:
            mcs = MCQ.objects.all().filter(Question=Questions)
            Quetions_dic[Questions] = mcs

        username = request.user.username
        return render(request, 'speak/practice_id.html', {'Quiz': Test, 'Quest_dic':Quetions_dic,'username':username})



@login_required(login_url='/sampleQuiz/')
def quizes(request):
    taken = Sitting.objects.filter(user=request.user).filter(Passed=True)
    highest= 1
    for Tests in taken:
        if Tests.__id__()>highest:
            highest=Tests.__id__()
    try:
        Show_quiz = Testing.objects.filter(Lesson_id__lte=highest+1)
    except:
        Show_quiz = Testing.objects.filter(Lesson_id__lte=highest)
    if User is not None:
        username = request.user.username
    else:
        username = None
    return render(request, 'speak/Quiz.html', {'Quizes': Show_quiz, 'username': username})


@login_required(login_url='/login/')
def quiz(request,Q_ID):
    if request.method == 'POST':
        score=0
        #ans=request.POST['Quest_dic' ]
        Ans= copy.deepcopy(request.POST)
        del Ans['csrfmiddlewaretoken']
        Keys=Ans.keys()
        #mcq_list = request.POST.getlist('Quest_dic')
        for key in Keys:
            id=Ans[key]
            MCQ_Ans=MCQ.objects.get(pk=id)
            if MCQ_Ans.__IsTrue__():
                score+=1
        total = len(Keys)
        percentage = (score/total)*100
        percentage = math.ceil(percentage)
        if percentage>60:
            cleared = True
        else:
            cleared = False
        test = get_object_or_404(Testing, pk=Q_ID)
        Sit = Sitting(user=request.user,Test=test, Score=percentage, Passed=cleared)
        Sit.save()
        practice=True
        ############################################################################################################
        ##########################################  Return to score page ###########################################
        ########################################## Ali make score.html presentable #################################
        return render(request, 'speak/score.html', {'score': score, 'percentage': percentage,
                                                    'cleared':cleared, 'out_of': total, 'Test':test})
    else:
        try:
            Last_cleared = Sitting.objects.filter(user=request.user).filter(Passed=True).latest('Time_Stamp')
            current= datetime.now()
            diff= current - Last_cleared.Time_Stamp.replace(tzinfo=None)
        except:
            diff=timedelta(days=2)

        if diff<timedelta(days=1):
            TimeLeft= timedelta(days=1)- diff
            return render(request,'speak/timeleft.html',{'TimeLeft':TimeLeft,'username':request.user})
        ############################################################################################################
        ############################################################################################################
        ############################    Ali add countdown timer using TimeLeft to TimeLeft HTML#####################
        ############################################################################################################
        ############################################################################################################
        ############################################################################################################
        username= request.user
        user_id= username.id
        User_Info = UserInfo.objects.get(user=request.user)
        try:
            User_Payments= Payments.objects.filter(userinfo=User_Info).latest('Expiry')
            if User_Payments.Expiry.replace(tzinfo=None)< datetime.now():
                return render(request,'speak/due.html',{'Name':username, 'ID':user_id})
        except:
            return render(request,'speak/due.html',{'Name':username, 'ID':user_id})

        Test = get_object_or_404(Testing, pk=Q_ID)
        Questions_set = Question.objects.all().filter(Testing=Test)
        que = ''
        mcs = ''
        Quetions_dic = {}

        for Questions in Questions_set:
            mcs = MCQ.objects.all().filter(Question=Questions)
            Quetions_dic[Questions] = mcs

        ###################################################################################################################
        ################################        Write Try except Statements if felt neccessary         ####################
        ###################################################################################################################
        username = request.user.username
        return render(request, 'speak/tempQuiz.html', {'Quiz': Test, 'Quest_dic':Quetions_dic,'username':username})


def signout(request):
    logout(request)
    return HttpResponseRedirect(reverse('home'))


def signup(request):
    if request.method == 'POST':

        username = str(request.POST['username'])
        password = request.POST['password']
        email = request.POST['email']
        rep_password = request.POST['rep_password']
        code=(''.join(choice(ascii_uppercase) for i in range(20)))
        address = request.POST['Address']
        phone = request.POST['phone']
        if User.objects.filter(username=username).exists():
            NewUser= NewUserForm()
            SignIn= UserForm()
            return render(request, 'speak/log.html', {'NewUser': NewUser, 'SignIn': SignIn, 'Priority': "Signup",
                                                      'Signup_Message': 'Username Exist'})
        #code to check reentered password to be implemented here
        #check if user exist or password missing code here
        print("here her"+'\n')
        if rep_password==password:
            user = User.objects.create_user(username,email,password)
            user.save()
            userInfo= UserInfo(user=user, Address=address, Phone=phone, Code=code)
            userInfo.save()
            user.is_active = False
            gmail_user = 'no-reply@easyspokenenglish.com.pk'
            gmail_pwd = 'K4ksc#8g'
            FROM = 'no-reply@easyspokenenglish.com.pk'
            Link= "easyspokenenglish.com.pk/auth/"+username+"/"+code
            TO = str(email)
            SUBJECT = 'Authentication Email from Easy Spoken English'
            TEXT = "Thank you for joining Easy Spoken English please click the link below to activate your account \n" \
                   "%s" %Link
            print(email)
            # Prepare actual message
            message = """From: %s\nTo: %s\nSubject: %s\n\n%s
            """ % (FROM, "".join(TO), SUBJECT, TEXT)
            try:
                server = smtplib.SMTP("smtp.easyspokenenglish.com.pk", 587)
                server.ehlo()
                server.starttls()
                server.login(gmail_user, gmail_pwd)
                server.sendmail(FROM, TO, message)
                server.close()
                print('successfully sent the mail')
            except:
                print ("failed to send mail")
            return render(request,'speak/authmail.html')
        else:
            return HttpResponseRedirect(reverse('login'))
    else:
        NewUser= NewUserForm()
        SignIn= UserForm()
    return render(request, 'speak/log.html', {'NewUser': NewUser, 'SignIn': SignIn, 'Priority': "Signup"})


def signin(request):

    if request.method == 'POST':

        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('home'))
        else:
            message="Invalid username or password"
            NewUser = NewUserForm()
            SignIn = UserForm()
            return render(request,'speak/log.html', {'NewUser': NewUser, 'SignIn': SignIn, 'Priority': "Login", "message":message})
    else:
        NewUser = NewUserForm()
        SignIn = UserForm()
    return render(request,'speak/log.html', {'NewUser': NewUser, 'SignIn': SignIn, 'Priority': "Login"})


def aboutUs(request):
    return render(request,'speak/aboutus.html',{'username':request.user})


def sampleLessons(request):
    return render(request,'speak/sampleLessons.html')


def samplePractice(request):
    return render(request,'speak/samplePractice.html')


def sampleQuiz(request):
    return render(request,'speak/sampleQuiz.html')

def sampleLesson1(request):
    return render(request,'speak/sampleLesson1.html')

def samplePractice1(request):
    return render(request,'speak/samplePractice1.html')

def sampleQuiz1(request):
    return render(request,'speak/sampleQuiz1.html')

def sampleLesson2(request):
    return render(request,'speak/sampleLesson2.html')

def samplePractice2(request):
    return render(request,'speak/samplePractice2.html')

def sampleQuiz2(request):
    return render(request,'speak/sampleQuiz2.html')

def sampleLesson3(request):
    return render(request,'speak/sampleLesson3.html')

def samplePractice3(request):
    return render(request,'speak/samplePractice3.html')

def sampleQuiz3(request):
    return render(request,'speak/sampleQuiz3.html')

def paymentmethods(request):
    return render(request,'speak/paymentMethods.html')