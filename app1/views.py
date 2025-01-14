from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate
from .models import *
from django.conf import settings
import os
from django.contrib.auth import get_user,get_user_model
from django.db import transaction
from django.contrib.auth.decorators import login_required

User = get_user_model()

@login_required(login_url='login')
def home(request):
    
    
    if request.method == "POST":
        if 'post_form' in request.POST:
            body = request.POST.get('body')
            image = request.FILES.get('image')
                
            user_posts = User_Posts.objects.create(body=body, image=image)
            user_posts.user.add(request.user)  # Add the authenticated user to the post
            return redirect('home')
        
        if 'comment_form' in request.POST:
            post_id = request.POST.get('post_id')
            comment_text = request.POST.get('comment_text')
            current_post = get_object_or_404(User_Posts, id=post_id)
            Comment.objects.create(post=current_post, user=request.user, text=comment_text)
            if current_post.user.first() != request.user:
                notification.objects.create(
                    body=f"{request.user.username} has Commented on your post {current_post.body[:30]}....."
                ).user.add(current_post.user.first())
            return redirect('home')
        
        if 'like_form' in request.POST:
            post_id = request.POST.get('post_id')
            current_post = User_Posts.objects.get(id=post_id)
            user = request.user
            
            if current_post.likes.filter(id=user.id).exists():
                # Remove the like if it already exists
                current_post.likes.remove(user)
                
            else:
                # Add a new like
                current_post.likes.add(user)
                if current_post.user.first() != request.user:
                    notification.objects.create(
                    body=f"{request.user.username} has liked Your post {current_post.body[:30]}....."
                ).user.add(current_post.user.first()) 
            
            return redirect('home')
        

    

    posts_by_user = User_Posts.objects.all().order_by('-created_at')
    current_u=Profile.objects.get(user=request.user)

    
    
    return render(request, 'homepage.html', {'posts_by_user': posts_by_user,'cu':current_u})



def login_view(request):
    if request.method == 'POST':
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'loginpage.html',{'error':'invalid credentials '})
  
    
    return render(request,'loginpage.html')


def signup(request):
    if request.method == 'POST':
        username=request.POST['username']
        email=request.POST['email']
        password1=request.POST['password1']
        password2=request.POST['password2']
        if password1 == password2:
            if User.objects.filter(username=username).exists():
                return render(request,'signup.html',{'error':'user already exists'})
            else:
                user=User.objects.create(username=username,email=email)
                user.set_password(password1)
                user.save()
                login(request,user)
                return redirect('home')
            
        else:
            return render(request,'signup.html',{'error':'both password dont match'})




    return render(request,'signup.html')


def user_profiles(request):
    profiles=Profile.objects.exclude(user=request.user)
    return render(request,'profiles.html',{'profiles':profiles})

def user_profile_page(request, pk):
    user = get_object_or_404(User, pk=pk)
    pro = get_object_or_404(Profile,user_id=pk)
    user_posts = User_Posts.objects.filter(user=user).order_by('-created_at')
    is_following = pro.is_followed_by(request.user)
    followers_count = pro.followers.count()
    #posts_by_current_user = User_Posts.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        if 'follow_button' in request.POST:
            action = request.POST['follow_button']
            current_user = request.user.profile

            if action == "follow":
                #current_user.followers.add(user)
                pro.followers.add(request.user)
                notification.objects.create(
                body=f"{request.user.username} has started following you"
            ).user.add(user)
            
            elif action == "unfollow":
                #current_user.followers.remove(user)
                pro.followers.remove(request.user)

        elif 'image_button' in request.POST:
            if 'profile_image' in request.FILES:
                pro.profile_image = request.FILES['profile_image']  # Set the uploaded image
                pro.save()
                return redirect('home')
            
        if 'comment_form' in request.POST:
            post_id = request.POST.get('post_id')
            comment_text = request.POST.get('comment_text')
            current_post = get_object_or_404(User_Posts, id=post_id)
            Comment.objects.create(post=current_post, user=request.user, text=comment_text)
            if current_post.user.first() != request.user:
                notification.objects.create(
                    body=f"{request.user.username} has Commented on your post {current_post.body[:30]}....."
                ).user.add(current_post.user.first())
            post_owner = current_post.user.first()  # Retrieve the first user in the ManyToMany relationship
            return redirect('user_profile', pk=post_owner.id)
        
        if 'like_form' in request.POST:
            post_id = request.POST.get('post_id')
            current_post = User_Posts.objects.get(id=post_id)
            user = request.user
            
            if current_post.likes.filter(id=user.id).exists():
                # Remove the like if it already exists
                current_post.likes.remove(user)
                
            else:
                # Add a new like
                current_post.likes.add(user)
                if current_post.user.first() != request.user:
                    notification.objects.create(
                    body=f"{request.user.username} has liked Your post {current_post.body[:30]}....."
                ).user.add(current_post.user.first()) 
            
            post_owner = current_post.user.first()  # Retrieve the first user in the ManyToMany relationship
            return redirect('user_profile', pk=post_owner.id)
            
            
            

    return render(request, 'user_profile_page.html', {
        'user': user,
        'pro': pro,
        'user_posts': user_posts,
        'is_following': is_following,
        'followers_count': followers_count,
        
    })


def user_followers(request,pk):
    user=get_object_or_404(User,pk=pk)
    
    pro=Profile.objects.get(user=user)
    user_followers=pro.followers.all()
    return render(request,'followers.html',{'user_followers':user_followers,'pro':pro})


def user_following(request,pk):
    user=get_object_or_404(User,pk=pk)
    pro=Profile.objects.get(user=user)
    user_following=user.following.all()

    return render(request,'followings.html',{'pro':pro,'user_following':user_following})

@login_required(login_url='/login/')
def edit_bio(request):
    profile=get_object_or_404(Profile,user=request.user)
    if request.method == 'POST':
        new_bio=request.POST['new_bio']
        pro_image=request.FILES.get('pro_image')
        account_type = request.POST.get('account_type') == 'on'

        profile.private_account = account_type
        profile.bio=new_bio
        
        if pro_image:
            # Optional: delete the old image to save space
            if profile.profile_image:
                old_image_path = os.path.join(settings.MEDIA_ROOT, profile.profile_image.name)
                if os.path.isfile(old_image_path):
                    os.remove(old_image_path)
            
            profile.profile_image = pro_image

        profile.save()
        return redirect('user_profile',pk=request.user.id)
        
    return render(request,'edit_bio.html',{'profile':profile})