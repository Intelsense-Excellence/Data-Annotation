from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import DataAnnotation, Annotator
from django.contrib import messages
import random


def home(request):
    if request.method == 'POST':
        annotatorID = request.POST['AnnotatorID']
        obj_id = request.POST['id']
        # number = request.POST['number']
        txt = request.POST['transcription']

        obj = DataAnnotation.objects.get(id=obj_id)
        obj.transcript = txt
        obj.isAnnotated = True
        obj.annotatorID = annotatorID
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


def BadAudio(request):
    if request.method == 'POST':
        obj_id = request.POST['obj_id']
        obj = DataAnnotation.objects.get(id=obj_id)
        obj.badAudio = True
        obj.save()
        return redirect('home')


def Dashboard(request):
    total_audio = DataAnnotation.objects.count()
    total_annotated = total_audio - DataAnnotation.objects.filter(badAudio=False, isAnnotated=False).count()
    annotators = Annotator.objects.all().order_by('-count')
    return render(request, 'dashboard.html',
                  {'total_audio': total_audio, 'total_annotated': total_annotated, 'annotators': annotators})
