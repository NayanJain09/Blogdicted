from django.shortcuts import render,HttpResponse,redirect
from .models import Contact
from django.contrib import messages
from blog.models import Category, Post,User
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.contrib.auth  import authenticate,  login, logout
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def home(request):
    posts = Post.objects.all().order_by('-views')
    categories = Category.objects.all()
    for post in posts:
        print(post.title)
    paginator = Paginator(posts, 5) #  posts in each page
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        posts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        posts = paginator.page(paginator.num_pages)
    context = {
        'page':page,
        'posts':posts,
        'categories':categories
    }
    return render(request,'home/home.html',context)

def contact(request):
    if request.method=='POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        msg = request.POST['content']
        contact = Contact(name=name,email=email,phone=phone,content=msg)
        contact.save()
        # subject = "Website Inquiry" 
        # body = {
		# 	'name':name, 
		# 	'email': email, 
		# 	'message':msg, 
		# }
	    
        # message = "\n".join(body.values())
        # messages.success(request,'Submitted Successfully')
        # send_mail(subject,message, settings.EMAIL_HOST_USER,[settings.EMAIL_HOST_USER], fail_silently=False)
        messages.success(request,'Submitted Successfully')
    
    return render(request,'home/contact.html')

def profile(request,name):
        author = User.objects.filter(username=name).first()
        posts = Post.objects.filter(author=author)
        context={
            'author':author,
            'posts' : posts
        } 
        # print('inside PPPPPPPPPPPPPPPPPP',author.username)
        return render(request,'home/about.html',context)

def search(request):
    query=request.POST['query']
    if len(query)>100:
        allPosts=Post.objects.none()
    else:
        allPostsTitle= Post.objects.filter(title__icontains=query)
        allPostsAuthor= Post.objects.filter(author__username__icontains=query)
        allPostsContent =Post.objects.filter(content__icontains=query)
        allPostsCategories = Post.objects.filter(categories__title__icontains=query)
        allPosts=  allPostsTitle.union(allPostsContent, allPostsAuthor,allPostsCategories)
        allPosts = allPosts.order_by('-views')
    if allPosts.count()==0:
        messages.warning(request, "No search results found. Please refine your query")

    paginator = Paginator(allPosts, 1) #  posts in each page
    page = request.GET.get('page')
    try:
        allPosts = paginator.page(page)
    except PageNotAnInteger:
    # If page is not an integer deliver the first page
        allPosts = paginator.page(1)
    except EmptyPage:
    # If page is out of range deliver last page of results
        allPosts = paginator.page(paginator.num_pages)
    params={'allPosts': allPosts, 'query': query,'page':page}
    return render(request, 'home/search.html', params)

def handleSignUp(request):
    if request.method=="POST":
        # Get the post parameters
        username=request.POST['username']
        email=request.POST['email']
        fname=request.POST['fname']
        lname=request.POST['lname']
        pass1=request.POST['pass1']
        pass2=request.POST['pass2']

        # check for errorneous input
        if not username.isalnum():
            messages.error(request, " Username should only contain letters and numbers")
            return redirect('home')
        if pass1==pass2:
            if User.objects.filter(username=username).exists():
                messages.warning(request,"Username already exists")
                return redirect('home')
            elif User.objects.filter(email=email).exists():
                messages.warning(request,"Email already registered")
                return redirect('home')
            else:
                myuser = User.objects.create_user(username, email, pass1)
                myuser.first_name= fname
                myuser.last_name= lname
                myuser.save()
                messages.success(request, " Your BlogDicted account has been successfully created")
                return redirect('home')
        else:
            messages.warning(request,"Password not matched!")
            return redirect('home')
    else:
       return redirect('home')

def handleLogin(request):
    if request.method=="POST":
        # Get the post parameters
        loginusername=request.POST['loginusername']
        loginpassword=request.POST['loginpassword']

        user=authenticate(username= loginusername, password= loginpassword)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("home")
        else:
            messages.warning(request, "Invalid credentials! Please try again")
            return redirect("home")

    return HttpResponse("404- Not found")

def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('home')
