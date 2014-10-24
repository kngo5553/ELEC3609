from django.shortcuts import render,redirect
from django.template import RequestContext, loader

from forumapp.models import Thread,Subject,Review

from django import forms
from django.shortcuts import render_to_response
from django.http import HttpResponse,HttpResponseRedirect
from forumapp.models import User,UserProfile, Comment

from django.core.paginator import Paginator

from django.contrib.auth import authenticate
from django.contrib import auth
from django.db.models import Q  # imported to help with querying
# Create your views here.


# context_instance=RequestContext(request) means always return current existing request google it


def profile(request,para):

    request_user = User.objects.get(id=para)
    user_profile= UserProfile.objects.get(user=request_user)

    user_threads = Thread.objects.filter(author=request_user,is_intrash=False).order_by('-publish_time').all()[0:1]

    is_myself = False

    if request.user.id == request_user.id:
        is_myself =True

    description = None
    if request.method == 'POST' :
            description= request.POST.get('description')
            user_profile.descrip = description
            user_profile.save()



    return render_to_response('profile.html', locals(),context_instance=RequestContext(request))

def alogin(request, *args, **kwargs):
    username = request.GET.get('new_username', None)
    errors= []
    account=None
    password=None
    if request.method == 'POST' :
        if not request.POST.get('account'):
            errors.append('Please Enter account')
        else:
            account = request.POST.get('account')
        if not request.POST.get('password'):
            errors.append('Please Enter password')
        else:
            password= request.POST.get('password')
        if account is not None and password is not None :
             user = authenticate(username=account,password=password)
             if user is not None:
                 if user.is_active:
                     auth.login(request,user)
                     return HttpResponseRedirect('/index')
                 else:
                     errors.append('disabled account')
             else :
                  errors.append('invaild user')
    return render_to_response('login.html', locals(),context_instance=RequestContext(request))




def register(request):
    errors= []
    account=None
    password=None
    password2=None
    email=None
    uniid=None
    CompareFlag=False
    status=True

    if request.method == 'POST':
        if not request.POST.get('account'):
            errors.append('Please Enter account.')
            status=False
        else:
            account = request.POST.get('account')

        if not request.POST.get('password'):
            errors.append('Please Enter password.')
            status=False
        else:
            password= request.POST.get('password')

        if not request.POST.get('password2'):
            errors.append('Please comfirm your password.')
            status=False
        else:
            password2= request.POST.get('password2')

        if not request.POST.get('email'):
            errors.append('Please Enter your email.')
            status=False
        else:
            email= request.POST.get('email')

        if password is not None and password2 is not None:
            if password == password2:
                CompareFlag = True
            else :
                errors.append('Retyped Password do not match, please retype the password.')
                status=False

        if not request.POST.get('uniid'):
            errors.append('Please Enter your uni ID.')
            status=False
        else:
            uniid = request.POST.get('uniid')
        


        if  account is not None and password is not None and password2 is not None and email is not None and CompareFlag and uniid is not None:
            if len(account) < 4 or len(account) > 16:                
                errors.append('Username should be minimum 4 and maximum 16 Characters.')
                status=False

            if len(uniid) != 9 :
                errors.append('Uni id must be 9 digital numbers.')
                status=False
            if len(password) <6 or len(password)>16:
                errors.append('Password should be minimum 6 and maximum 16 Characters.')
                status=False

            if User.objects.filter(username= account):
                errors.append('%s has been already registered.' % account)
                status=False

        if status == True:

            new_user=User.objects.create_user(account,email,password)
            new_user.is_active=True
            new_user.save
            new_userprofile=UserProfile()
            new_userprofile.user = new_user
            new_userprofile.uni_id=uniid
            new_userprofile.is_Academics=0
            new_userprofile.descrip = "This guys is lazy."
            new_userprofile.save()

            return HttpResponseRedirect('/login/?new_username=%s&uni_id=%s' % (new_user.username,new_userprofile.uni_id) )

    return render_to_response('register.html', {'errors': errors},context_instance=RequestContext(request))





def search_review(request):

    after_range_num = 5
    bevor_range_num = 4
    try:
        page = int(request.GET.get("page",1))
        print('page----->',page)
        if page < 1:
            page = 1
    except ValueError:
        page = 1

    query_code = request.GET.get('subject_code')

    info = Subject.objects.filter(subject_code=query_code).all()
    subject_list = Subject.objects.all()
    top_subject=Subject.objects.order_by('-rating').all()[:1]

    paginator = Paginator(info,16)
    
    
    try:
        articleList = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        articleList = paginator.page(1)
    print('articleList---->',articleList.object_list)

    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+bevor_range_num]


    return render_to_response('search_review_list.html',locals(),context_instance=RequestContext(request))




def search_thread(request):

    after_range_num = 5
    bevor_range_num = 4
    try:
        page = int(request.GET.get("page",1))
        print('page----->',page)
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    query_thread = request.GET.get('search')

    info = Thread.objects.filter(title__contains=query_thread, is_intrash=False).order_by('-publish_time')


    paginator = Paginator(info,16)
    
    
    try:
        articleList = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        articleList = paginator.page(1)
    print('articleList---->',articleList.object_list)

    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+bevor_range_num]


    return render_to_response('search_thread.html',locals(),context_instance=RequestContext(request))



def alogout(request):
    auth.logout(request)
    return HttpResponseRedirect('/index')


def detail(request,thread_id):        
    try:
        thread = Thread.objects.get(id=thread_id)
    except Thread.DoesNotExist:
        raise Http404

    after_range_num = 5
    bevor_range_num = 4
    try:
        page = int(request.GET.get("page",1))
        print('page----->',page)
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    
    info = Comment.objects.filter(to_thread=thread_id).order_by('-create_time').all()

    
    paginator = Paginator(info,5)
    
    
    try:
        articleList = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        articleList = paginator.page(1)
    print('articleList---->',articleList.object_list)

    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+bevor_range_num]

    if  thread.is_intrash == False:
        reply_post(request,thread)
        move_to_trash(request,thread)

    return render_to_response("view_post.html",locals(),context_instance=RequestContext(request))



def move_to_trash(request,thread):
    
    if request.method == 'POST':
        print "sss" 
        print request.POST
        print "not"
        if request.POST.has_key('delete'):
            thread.is_intrash=True
            thread.save()
            return HttpResponseRedirect('/general_thread_list/trashbin/')


def show_trash(request):
    

    after_range_num = 5
    bevor_range_num = 4
    try:
        page = int(request.GET.get("page",1))
        print('page----->',page)
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    
    info = Thread.objects.filter(is_intrash=True).order_by('-publish_time').all()

    paginator = Paginator(info,16)
    
    
    try:
        articleList = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        articleList = paginator.page(1)
    print('articleList---->',articleList.object_list)

    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+bevor_range_num]


    return render_to_response("trashbin.html",locals(),context_instance=RequestContext(request))







class ThreadForm(forms.Form):

    title = forms.CharField(label=u'Title', widget=forms.TextInput(attrs={'size':30, 'max_length':30})) 
    content = forms.CharField(label=u'Content', widget=forms.Textarea(attrs={'size':10000})) 





def  creation(request):

    errors= []
    title=None
    content=None


    if request.method == 'POST':
        if not request.POST.get('title'):
            errors.append('Please fill out title.')
        else:
            title = request.POST.get('title')

        if not request.POST.get('content'):
            errors.append('Please fill out content area.')
        else:
            content= request.POST.get('content')
       


        if title is not None and content is not None :

            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.topic_count += 1
            user_profile.save()

            new_thread = Thread()
            new_thread.title = title
            new_thread.author = request.user
            new_thread.replies = 0
            new_thread.views = 0
            new_thread.like = 0;
            new_thread.is_intrash=False
            new_thread.content = content
            new_thread.save()

            new_comment = Comment()
            new_comment.content = "Hi, Why not leave something here?"
            new_comment.from_user = request.user

            new_comment.to_user = new_thread.author
            new_comment.to_thread = new_thread

            new_comment.save()


          
            return HttpResponseRedirect('/general_thread_list/%s/' % new_thread.id)
    

    return render_to_response('create_post.html', {'errors': errors},context_instance=RequestContext(request))



def  reply_post(request,thread):

    errors= []
    content=None
    a="11"

    if request.method == 'POST':

        if not request.POST.get('content'):
            errors.append('Please fill out content area.')
        else:
            content= request.POST.get('content')
       


        if content is not None :

 
            user_profile = UserProfile.objects.get(user=request.user)
            user_profile.post_count += 1
            user_profile.save()

            new_comment = Comment()
            new_comment.content = content
            new_comment.from_user = request.user

            new_comment.to_user = thread.author
            new_comment.to_thread = thread

            new_comment.save()

            thread.replies +=1
            thread.save()

            return HttpResponseRedirect('/')
    

    return render_to_response('view_post.html', {'errors': errors},context_instance=RequestContext(request))



def thread_list(request):
    after_range_num = 5
    bevor_range_num = 4
    try:
        page = int(request.GET.get("page",1))
        print('page----->',page)
        if page < 1:
            page = 1
    except ValueError:
        page = 1
    
    info = Thread.objects.filter(is_intrash=False).order_by('-publish_time').all()

    paginator = Paginator(info,16)
    
    
    try:
        articleList = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        articleList = paginator.page(1)
    print('articleList---->',articleList.object_list)

    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+bevor_range_num]
    return render_to_response("general_thread_list.html",locals(),context_instance=RequestContext(request))


def view_myposts(request):
    after_range_num = 5
    bevor_range_num = 4
    try:
        page = int(request.GET.get("page",1))
        print('page----->',page)
        if page < 1:
            page = 1
    except ValueError:
        page = 1


    info = Thread.objects.filter(author=request.user,is_intrash=False).order_by('-publish_time').all()

    paginator = Paginator(info,16)
    
    
    try:
        articleList = paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        articleList = paginator.page(1)
    print('articleList---->',articleList.object_list)

    if page >= after_range_num:
        page_range = paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+bevor_range_num]
    return render_to_response("view_myposts.html",locals(),context_instance=RequestContext(request))


def review_list(request):
    subject_list = Subject.objects.all()
    after_range_num=5
    bevor_range_num =4
    try:
        page=int(request.GET.get("page",1))
        print('page----->',page)
        if page <1:
            page=1
    except ValueError:
        page=1
        
    info=Subject.objects.all()
    top_subject=Subject.objects.order_by('-rating').all()[:1]
    paginator=Paginator(info,16)
	
    try:
        articleList=paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        articleList=paginator.page(1)
    print('articleList---->',articleList.object_list)
        
    if page>= after_range_num:
        page_range=paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range = paginator.page_range[0:int(page)+bevor_range_num]
    return render_to_response('general_review_list.html' ,locals(),context_instance=RequestContext(request))


def whiteboard(request):

    return render_to_response('whiteboard.html' ,locals(),context_instance=RequestContext(request))

def white(request):

    return render_to_response('white.html' ,locals(),context_instance=RequestContext(request))




def index(request):

    new_threads=Thread.objects.filter(is_intrash=False).order_by('-publish_time').all()[0:5]


    return render_to_response('index.html' ,locals(),context_instance=RequestContext(request))

def course_review(request,subject_id):
    try:
        course=Subject.objects.get(id=subject_id)
    except Subject.DoesNotExist:
        raise Http404


    after_range_num=5
    bevor_range_num=4
    try:
        page=int(request.GET.get("page",1))
        print('page----->',page)
        if page<1:
            page=1
    except ValueError:
        page=1

    info=Review.objects.filter(subject_code=subject_id).order_by('-update_time').all()
    paginator=Paginator(info,5)
    
    try:
        articleList=paginator.page(page)
    except(EmptyPage,InvalidPage,PageNotAnInteger):
        articleList=paginator.page(1)
    print('articleList----->',articleList.object_list)
    
    if page>=after_range_num:
        page_range=paginator.page_range[page-after_range_num:page+bevor_range_num]
    else:
        page_range=paginator.page_range[0:int(page)+bevor_range_num]
    return render_to_response("view_review.html",locals(),context_instance=RequestContext(request))


def create_review(request):
    errors= []
    title = None
    content = None
    rating = None
    subject_code = None
    subject_list = Subject.objects.all()
    print subject_list

    if request.method == 'POST':
        if not request.POST.get('subject_code'):
            errors.append('Please fill out subject_code.')
        else:
            subject_code = request.POST.get('subject_code')
        if not request.POST.get('title'):
            errors.append('Please fill out title.')
        else:
            title = request.POST.get('title')
        if not request.POST.get('content'):
            errors.append('Please fill out content area.')
        else:
            content= request.POST.get('content')
        if not request.POST.get('rating'):
            errors.append('Please fill out content rating.')
        else:
            rating= request.POST.get('rating')            
       

        if title is not None and content is not None and rating is not None and subject_code is not None:
            user_profile = UserProfile.objects.get(user=request.user)
			#add in user.review_count
            #user_profile.review_count += 1
            user_profile.save()
            subject = Subject.objects.get(subject_code = subject_code)
            new_review = Review()
            new_review.subject_code = subject
            new_review.author = request.user
            new_review.title = title
            new_review.content = content
            new_review.rating = rating
            new_review.save()
          
            return HttpResponseRedirect('/course/%s/' % subject.id)
    
    return render_to_response('create_review.html', {'errors': errors,'subject_list':subject_list},context_instance=RequestContext(request))



class UserForm(forms.Form): 
    username = forms.CharField(label='username',max_length=100)
    password = forms.CharField(label='password',widget=forms.PasswordInput())


class UserForm2(forms.Form):
    username = forms.CharField(label = 'Login name: ', max_length = 16)
    password = forms.CharField(label = 'Passoword: ', widget=forms.PasswordInput())
    email = forms.EmailField(label = 'Email: ',required = False)
    first_name= forms.CharField(label = 'First name: ',min_length=1,max_length=20)
    last_name = forms.CharField(label = 'Last name: ',min_length=1,max_length=20)
    gender = forms.ChoiceField(choices=(('m','male'),('f','female')),required = False)
    uni_id = forms.IntegerField(label = "Uni ID")
