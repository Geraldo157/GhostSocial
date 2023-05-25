from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.contrib.auth.models import User
from django.contrib import auth


def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        if not User.objects.filter(username=username).exists() or User.objects.filter(email=email).exists():
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.save()
            return redirect('login')
    else:
        return render(request, 'users/register.html')


def Login(request):
    if request.POST == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect('blog-home')
            else:
                return render(request, 'users/login.html')
        else:
            return render(request, 'users/login.html')
    else:
        return render(request, 'users/login.html')


@login_required
def profile(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
