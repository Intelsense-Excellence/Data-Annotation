from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import DataAnnotation, Annotator


def home(request):
    if request.method == 'POST':
        annotatorID = request.POST['AnnotatorID']
        obj_id = request.POST['id']
        number = request.POST['number']
        txt = request.POST['transcription']

        obj = DataAnnotation.objects.get(id=obj_id)
        obj.transcript = txt
        obj.save()

        annotator, created = Annotator.objects.get_or_create(AnnotatorID=annotatorID)
        annotator.count += 1
        annotator.save()

        return redirect(request.path_info + '?page=' + str(number))

    else:
        data = DataAnnotation.objects.all().order_by('id')
        paginator = Paginator(data, 1)
        page_number = request.GET.get('page')
        data = paginator.get_page(page_number)
        return render(request, 'home.html', {'data': data})
