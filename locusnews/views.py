from datetime import datetime
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
import re

from django.contrib.auth.decorators import login_required   

from .models import UserDetails,News

from django.http import JsonResponse



def home(request):
    return render(request, 'home.html')

def loginview(request):
    return render(request, 'login.html')

def registerview(request):
    return render(request, 'register.html')


def register(request):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

    if request.method == 'POST':

        Username = request.POST['username']
        Email = request.POST['email']
        Password=request.POST['password']
        Role= request.POST['role']

        if not Username.isalnum():
            messages.error(request,'Error. Username Should only contain letters and numbers.')
            return redirect('registerview')

        if(re.fullmatch(regex, Email)):
            pass
        else:
            messages.error(request,'Invalid Email')
      
        allusers = User.objects.all()

        for i in allusers:
            if(i.username==Username):
                messages.error(request,"User already exists")
                return redirect('registerview')
            
        myuser = User.objects.create_user(Username, Email, Password)
        myuser.save()

        newuser= UserDetails(username=Username, email=Email,password=Password,role=Role)
        newuser.save()

        messages.success(request,"Your account has been successfully created")
        return redirect('loginview')
    
    else:
        return HttpResponse('<h1>404-Error</h1>')
    

def approval(request):

    if request.method=="POST":
     
        loginusername=request.POST['username']
        loginpassword=request.POST['password']

        user = authenticate(request,username= loginusername, password= loginpassword)

        obj = UserDetails.objects.get(username=loginusername)
        Role = obj.role

        if user is not None and  Role=='Common User':
            login(request,user)
            messages.success(request,"Successfully Logged In as Common User")
            return redirect('commonuser')
        
        elif(user is not None and Role=='Journal'):
            login(request,user)
            messages.success(request,"Successfully Logged In as Journal")
            return redirect('journal')
    
        messages.error(request,"Invalid User. Please check the username and password" )
        return redirect("loginview")
    
def commonuser(request):
    username = request.user.username
    allnews = News.objects.all()
    return render(request,'commonuser.html',{'username':username,'allnews':allnews})

def journal(request):
    username = request.user.username
    allnews = News.objects.all()
    return render(request,'journal.html',{'username':username,'allnews':allnews})

def postnews(request):
    if request.method == 'POST':
        author = request.user 
        title = request.POST['title']
        img=request.FILES['image']
        content = request.POST['content']
        feed = News(title=title,image=img,content=content,author=author)
        feed.save()
        return redirect('commonuser')

    return render(request,'postnews.html')

def handlelogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('loginview')



def toggle_vote(request, news_id):
    news = News.objects.get(pk=news_id)
    
    # Check if user has already voted on this news
    user_voted = request.session.get(f"voted_{news_id}", None)
    
    if user_voted is None:
        # If user hasn't voted, toggle to upvote
        news.upvotes += 1
        request.session[f"voted_{news_id}"] = 'upvote'
    elif user_voted == 'upvote':
        # If user has upvoted, toggle to downvote
        news.upvotes -= 1
        news.downvotes += 1
        request.session[f"voted_{news_id}"] = 'downvote'
    else:
        # If user has downvoted or voted otherwise, toggle to upvote
        news.upvotes += 1
        news.downvotes -= 1
        request.session[f"voted_{news_id}"] = 'upvote'
        
    news.save()
    
    return JsonResponse({'upvotes': news.upvotes, 'downvotes': news.downvotes})
