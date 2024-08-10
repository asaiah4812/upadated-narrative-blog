from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from .forms import UserRegistionForm, UserEditForm, ProfileEditForm
from django.contrib import messages
from .forms import LoginForm
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from articles.models import Articles

# Create your views here.

def signup_user(request):
    if request.method == 'POST':
        form = UserRegistionForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            new_user.save()
            Profile.objects.create(user=new_user)
            messages.success(request, 'Account Created Successfully, login to continue')
            return redirect('login')
        else:
            if 'password2' in form.errors:
                messages.error(request, 'Passwords do not match.')
            elif 'username' in form.errors:
                messages.error(request, 'A user with that username already exists.')
            elif 'email' in form.errors:
                messages.error(request, 'A user with that email address already exists.')
            else:
                messages.error(request, 'There was an error with your signup. Please try again.')
            return redirect('signup')
    else:
        form = UserRegistionForm()
    return render(request, 'registration/signup.html', {'form': form}) 


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password']) 
        
            if user is not None:
                if user.is_active:
                    login(request, user)  
                    messages.success(request, 'login successfully')
                    return redirect('articles:all_articles')      
                else:
                    messages.warning(request, 'something went wrong')
            else:
                messages.warning(request, 'Invalid username or password.')
                
        else:
            form = LoginForm()
            
    return render(request, 'registration/login.html')
    
def logout_user(request):
    logout(request)
    messages.info(request, "Your session has ended login to continue ")
    return redirect('login')



@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('articles:all_articles')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    context = {
        'user_form': user_form,
        'profile_form' : profile_form 
    }  
    return render(request, 'articles/edit.html', context)

def custom_404(request, exception):
    # You can access the requested path using `request.path_info`
    return render(request, '404.html', status=404)



def user_profile(request, username):
    user_profile = get_object_or_404(Profile, user__username=username)
    user_articles = Articles.published.filter(author=user_profile.user, status=Articles.Status.PUBLISHED)
    context = {
        'user_profile': user_profile,
        'user_articles': user_articles,
    }
    return render(request, 'articles/profile.html', context)
    

    


