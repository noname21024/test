from django.shortcuts import render
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .form import UserRegisterForm, UserUpdateForm, ProfileForm, EmailAddressForm
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from core.models import Tags
from core.models import Following, Mangas, Tags


def register(request):
    type = 'register'
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form.errors)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')
            user.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserRegisterForm()

    return render(request, 'register.html', {'type': type, 'form': form})

def logoutPage(request):
    logout(request)
    return redirect('home')

def user_page(request):
    
    tags = Tags.objects.all()

    if request.method == 'POST':
        action = request.POST.get('unfollow')
        if action:
            name_of_manga = request.POST['name-manga']
            manga = Mangas.objects.get(name = name_of_manga)
            print(name_of_manga)
            Following.objects.get(manga = manga, user = request.user).delete()  

    context = {'tags': tags}

    return render(request, 'information.html', context)


def change_information(request):
    tags = Tags.objects.all()
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST ,instance=request.user)
        p_form = ProfileForm(request.POST, request.FILES ,instance=request.user.profile)
        print(p_form.errors)
        print(u_form.errors)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Tài khoản của bạn đã được cập nhật!')
            return redirect('change-infor')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
        'tags': tags
    }

    return render(request, 'information_change.html', context)

def updated_email(request):
    tags = Tags.objects.all()

    if request.method == 'POST':
        u_form = EmailAddressForm(request.POST ,instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect('change-infor')
    else:
        u_form = EmailAddressForm(instance=request.user)
    context = {
        'u_form': u_form
    }

    return render(request, 'update_email.html', context)
