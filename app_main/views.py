from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import DataAnnotation, Annotator
from django.contrib import messages
import random
from django.contrib.auth import authenticate, login as auth_login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.method == 'POST':
        annotatorID = request.user
        obj_id = request.POST['id']
        txt = request.POST['transcription']

        obj = DataAnnotation.objects.get(id=obj_id)
        obj.transcript = txt
        obj.isAnnotated = True
        obj.annotatorID = str(annotatorID)
        obj.save()

        annotator, created = Annotator.objects.get_or_create(AnnotatorID=annotatorID)
        annotator.count += 1
        messages.info(request, annotator.count)
        annotator.save()

        response = redirect('home')
        response.set_cookie('idCookies', str(annotatorID))  # Save only the latest 5 queries
        return response

    else:
        data = DataAnnotation.objects.filter(badAudio=False, isAnnotated=False).order_by('-id')[:20]
        # paginator = Paginator(data, 1)
        # page_number = request.GET.get('page')
        # data = paginator.get_page(page_number)
        indx = random.randint(0, 19)
        data = data[indx]
        idCookies = request.COOKIES.get('idCookies', '').split(',')[0]
        return render(request, 'home.html', {'data': data, 'idCookies': idCookies})

@login_required
def BadAudio(request):
    if request.method == 'POST':
        obj_id = request.POST['obj_id']
        obj = DataAnnotation.objects.get(id=obj_id)
        obj.badAudio = True
        obj.save()
        return redirect('home')

@login_required
def Dashboard(request):
    total_audio = DataAnnotation.objects.count()
    total_annotated = total_audio - DataAnnotation.objects.filter(badAudio=False, isAnnotated=False).count()
    annotators = Annotator.objects.all().order_by('-count')
    return render(request, 'dashboard.html',
                  {'total_audio': total_audio, 'total_annotated': total_annotated, 'annotators': annotators})


def Login(request):
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect("home")
        messages.info(request, 'Invalid Username/Password')
        return render(request, 'login.html')

    return render(request, 'login.html')


def Register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')

        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'register.html')

        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            auth_login(request, user)
            return redirect('home')  # Redirect to a success page
        except ValidationError as e:
            messages.error(request, str(e))
        except Exception as e:
            messages.error(request, "An error occurred: " + str(e))

    return render(request, 'register.html')


def logout_user(request):
    logout(request)
    return redirect("home")
