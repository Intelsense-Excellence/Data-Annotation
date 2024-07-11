from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import DataAnnotation, Annotator
from django.contrib import messages


def home(request):
    if request.method == 'POST':
        annotatorID = request.POST['AnnotatorID']
        obj_id = request.POST['id']
        number = request.POST['number']
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

        return redirect(request.path_info + '?page=' + str(number))

    else:
        data = DataAnnotation.objects.filter(badAudio=False, isAnnotated=False).order_by('-id')[:10]
        paginator = Paginator(data, 1)
        page_number = request.GET.get('page')
        data = paginator.get_page(page_number)

        path = data[0].audio
        print(path)

        return render(request, 'home.html', {'data': data, 'path': path})


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
