from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .models import Profile,Post,LikePost,Followers
from django.http import HttpResponse
from itertools import chain
from django.contrib.auth.decorators import login_required
from django.db.models import Q

# Create your views here.

def Signup(request):
    try:
        if request.method=='POST':
            username=request.POST.get('username')
            email=request.POST.get('email')
            password=request.POST.get('password')
            password1=request.POST.get('password1')

            my_user=User.objects.create_user(username,email,password)
            my_user.save()
            user_model=User.objects.get(username=username)
            new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
            new_profile.save()
            if my_user is not None:
                login(request,my_user)
                return redirect('/')
            return redirect('/')
    except:
        invalid="User Already Exists"
        return render(request,"sign.html",{'invalid':invalid})

    return render(request, 'sign.html')

def Login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        MyUser=authenticate(request,username=username,password=password)
        if MyUser is not None:
            login(request,MyUser)
            return redirect('/')
        invalid="User is not Valid"
        return render(request,'login.html',{'invalid':invalid})
    return render(request, 'login.html')

@login_required(login_url='/Login')
def Logout(request):
    logout(request)
    return redirect('/Login')


@login_required(login_url='/Login')
def upload(request):
    if request.method=='POST':
        user=request.user.username
        image=request.FILES.get('image-upload')
        caption=request.POST['caption']
        new_post=Post.objects.create(user=user, image=image, caption=caption)
        print(new_post)
        new_post.save()
        return redirect('/')
    else:
        return redirect('/')
    
    

@login_required(login_url='/Login')
def Main(request):
    following_users=Followers.objects.filter(follower=request.user.username).values_list('user',flat=True)
    post=Post.objects.filter(Q(user=request.user.username)|Q(user__in=following_users)).order_by('-created_at')
    profile=Profile.objects.filter(user=request.user).first()
    context={
        'post':post,
        'profile':profile,
    }
    return render(request,'home.html',context)


@login_required(login_url='/Login')
def Likes(request,id):
    if request.method=='GET':
        username=request.user.username
        post=get_object_or_404(Post,id=id)
        like_filter=LikePost.objects.filter(post_id=id,username=username).first()
        if like_filter is None:
            new_like=LikePost.objects.create(post_id=id,username=username)
            post.no_of_likes=post.no_of_likes+1
        else:
            like_filter.delete()
            post.no_of_likes=post.no_of_likes-1
        post.save()
    print(post.id)        #generate url for current post's detail page            
    return redirect('/#'+id)


@login_required(login_url='/Login')
def Explore(request):
    post=Post.objects.all().order_by('-created_at')
    profile=Profile.objects.filter(user=request.user).first()
    context={
        'post':post,
        'profile':profile,
    }
    return render(request,'explore.html',context)
    

@login_required(login_url='/Login')
def profile(request,id_user):
    user_object=User.objects.get(username=id_user)
    profile=Profile.objects.filter(user=request.user).first()   
    user_profile=Profile.objects.filter(user=user_object).first()
    user_posts=Post.objects.filter(user=id_user).order_by('-created_at')
    user_post_length=len(user_posts)
    follower=request.user.username
    user=id_user
    if Followers.objects.filter(follower=follower,user=user).first():
        follow_unFollow='UnFollow'
    else:
        follow_unFollow='Follow'
    
    user_followers=len(Followers.objects.filter(user=id_user))
    user_following=len(Followers.objects.filter(follower=id_user))
    
    context={
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_post_length':user_post_length,
        'profile':profile,
        'follow_unFollow':follow_unFollow,
        'user_followers':user_followers,
        'user_following':user_following,
        
    }
    if request.user.username==id_user:
        if request.method=='POST':
            if request.FILES.get('image')==None:
                image=user_profile.profileImage
                bio=request.POST['bio']
                location=request.POST['location']
                user_profile.profileImage=image 
                user_profile.bio=bio
                user_profile.location=location
                user_profile.save() 
                
            if request.FILES.get('image')!=None:
                image=request.FILES.get('image')
                bio=request.POST['bio']
                location=request.POST['location']
                user_profile.profileImage=image 
                user_profile.bio=bio
                user_profile.location=location
                user_profile.save()  
                
            return redirect('/profile/'+id_user)
        else:
            return render(request,'profile.html',context)
    return render(request,'profile.html',context)
            

@login_required(login_url='/Login')
def Delete(request,id):
    post=Post.objects.get(id=id)
    post.delete()
    return redirect('/profile/'+request.user.username)        


@login_required(login_url='/Login')
def Search_results(request):
    query=request.GET.get('q')
    users=Profile.objects.filter(user__username__icontains=query)
    posts=Post.objects.filter(caption__icontains=query)
    context={
        'query':query,
        'users':users,
        'posts':posts,
    }
    return render (request,'search_user.html',context)


def Home_post(request,id):
    post=Post.objects.get(id=id)
    profile=Profile.objects.get(user=request.user)
    context={
        'post':post,
        'profile':profile,
    }
    return render(request,'home.html',context)


def Follow(request):
    if request.method=='POST':
        follower=request.POST['follower']
        user=request.POST['user']
        if Followers.objects.filter(follower=follower,user=user).first():
            delete_follower=Followers.objects.get(follower=follower,user=user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower=Followers.objects.create(follower=follower,user=user)
            new_follower.save()
            return redirect('/profile/'+user)
    else:
        return redirect('/')
            





