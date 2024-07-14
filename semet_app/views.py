from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, UserRegistrationForm, UserEditForm, ProfileEditForm, AdditionEditForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LogoutView
from .models import Profile, Additional_Info, Message
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import UserSearchForm
from django.conf import settings
from django.core.mail import send_mail
import smtplib
from django.http import Http404

def error_404_view(request, exception):
    return render(request, 'Home/404.html', {}, status=404)


@login_required
def send_message(request, username):
    if request.method == 'POST':
        receiver = User.objects.get(username=username)
        
        message_text = request.POST.get('message')

        # Ensure sender's profile exists
        sender_profile, created = Profile.objects.get_or_create(user=request.user)

        # Ensure receiver's profile exists
        receiver_profile, created = Profile.objects.get_or_create(user=receiver)

        message = Message.objects.create(sender=request.user, receiver=receiver, message=message_text)
        sender_profile.messages.add(message)
        receiver_profile.messages.add(message)
        messages.success(request, 'Message sent successfully')
        return redirect('public_profile', username=username)
    else:
        return render(request, 'Home/send_message.html', {'username': username})


def public_profile(request, username):
    user = User.objects.get(username=username)
    return render(request, 'Home/public_profile.html', {'user': user, 'section':'profile_search'})

@login_required
def user_search(request):
    if request.method == 'POST':
        form = UserSearchForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            # Perform a case-insensitive search for usernames containing the search term
            users = User.objects.filter(username__icontains=username)
            return render(request, 'Home/search_results.html', {'users': users, 'form':form, 'section':'profile_search' })
    else:
        form = UserSearchForm()
    return render(request, 'Home/user_search.html', {'form': form, 'section':'profile_search'})


def home(request):
    return render(request, 'Home/home.html')
    
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            try:
                with smtplib.SMTP_SSL(settings.EMAIL_HOST, settings.EMAIL_PORT2) as connection:
                    connection.login(user=settings.EMAIL_HOST_USER, password=settings.EMAIL_HOST_PASSWORD)
                    connection.sendmail(
                        from_addr=settings.EMAIL_HOST_USER,
                        to_addrs='ukwedjedimeji@gmail.com',
                        msg=f'Subject:Daily Quotes\n\nNew subscription from: {email}\n\nMessage: congrats dawg'
                    )
                    connection.close()

                return render(request, 'Home/subscription_successful.html')
            except Exception as e:
                return render(request, 'Home/invalid_request.html')
        else:
            return render(request, 'Home/invalid_email.html')
    return render(request, 'Home/invalid_request.html')

@login_required
def edit_additional_info(request):
    additional_info, created = Additional_Info.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        additional_info_form = AdditionEditForm(instance=additional_info, data=request.POST)
        
        if additional_info_form.is_valid():
            additional_info_form.save()
            messages.success(request, 'Additional Information updated successfully')
              # or wherever you want to redirect after successful update
        else:
            messages.error(request, 'Error updating your additional information')
    else:
        additional_info_form = AdditionEditForm(instance=additional_info)
    
    return render(request, 'Home/edit_additional_info.html', {
        'additional_info_form': additional_info_form,
        'section': 'edit',
    })
    
@login_required
def edit(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        profile_form = ProfileEditForm(instance=request.user.profile, data=request.POST, files=request.FILES)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
        else:
            messages.error(request, 'Error updating your profile')
    else:
        user_form = UserEditForm(instance=request.user)
        profile_form = ProfileEditForm(instance=request.user.profile)
    
    return render(request, 'Home/edit.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'section': 'edit'
    })

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
                user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create the user profile
            Profile.objects.create(user=new_user)
            Additional_Info.objects.create(user=new_user)
            return render(request,
                'Home/signup_done.html',
                {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,
        'Home/signup.html',
        {'user_form': user_form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, 
                                username = cd['username'],
                                password = cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated '\
                        'successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        LoginForm()
    return render(request, 'Home/login.html', {'form':form})

@login_required
def dashboard(request):
    profile = request.user.profile
    return render(request,
                  'Dashboard/dashboard.html',
                  {'section':'dashboard',
                   'profile': profile},)

class LogoutView(LogoutView):
    def get(self, request):
        logouts = logout(request)
        return render(request, 'Home/logged_out.html', {'logout':logout})
        # return redirect('login')
        

            
