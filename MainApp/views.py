from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Svs_z, Svs_k


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_snippet_page(request):
    context = {'pagename': 'Добавление нового сниппета'}
    return render(request, 'pages/add_snippet.html', context)


def svs_z_page(request):
    svs_zs = Svs_z.objects.all()   #все данные из БД
    context = {
        'pagename': 'Просмотр svs_z',
        'svs_zs': svs_zs
    }
    return render(request, 'pages/view_svs_z.html', context)
