from django.shortcuts import render,HttpResponse,redirect
from .models import Post,BlogComment,User,Category
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
# from tinymce.widgets import TinyMCE
# from django.contrib.auth.decorators import login_required
# Create your views here.

def blogHome(request):
    posts = Post.objects.all().order_by('-views')
    categories = Category.objects.all()
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
    return render(request,'blog/blogHome.html',context)

def blogPost(request, slug): 
    post = Post.objects.filter(slug=slug).first()
    comments = BlogComment.objects.filter(post=post, parent=None)
    replies = BlogComment.objects.filter(post=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    if post is None:
        print(post,slug,comments,replies)
        messages.warning(request,'Blog Not found!')
    if post is not None:
        post.views= post.views+1
        post.save()
    context={'post':post, 'comments': comments, 'user': request.user, 'replyDict': replyDict}    
    return render(request, "blog/blogPost.html", context)

def category(request,field):
    posts = Post.objects.filter(categories__title__icontains=field)
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
    context ={'page':page,'posts':posts,'field':field}
    return render(request,'blog/blogCat.html',context)


def postComment(request):
    if request.method == "POST":
        user=request.user
        postSno =request.POST.get('postSno')
        post= Post.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        print('AAAAAAAAAAAAAAAAA',parentSno)
        if parentSno is None:
            comment=request.POST.get('comment')
            comment=BlogComment(comment= comment, user=user, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            comment=request.POST.get('reply')
            parent = BlogComment.objects.filter(sno=parentSno).first()
            print('AAAAAAAAAAA',parent.comment)
            comment=BlogComment(comment= comment, user=user, post=post , parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
    
    return redirect(f"/blog/{post.slug}")


def create(request):
    if request.method=='POST':
        print('AAAAAAAAAAAAAAAAAAAAA')
        title = request.POST.get('title')
        content = request.POST.get('mytextarea')
        author = request.user
        categories=request.POST.getlist('category')
        print('AAAAAAAAAAAA',categories)
        # slug = slugify(title)
        post = Post(title=title,content=content,author=author)
        post.save()
        fields=[]
        for category in categories:
            fields.append(Category.objects.filter(title=category).first())
        if len(fields)==0:
            fields.append(Category.objects.filter(title='Others').first())
        post.categories.set(fields)
        post.save()    
        print(post.title+post.slug)
        messages.success(request,'Successully created')
        return redirect(f"/blog/{post.slug}")
    elif not request.user.is_authenticated:
        messages.warning(request,'Login to Create your Blog')
        return redirect('/')
    categories=Category.objects.all()
    context={'categories':categories}     
    return render(request,'blog/create.html',context)
