from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Svs_z, Svs_k
from MainApp.forms import ZvsForm


def index_page(request):
    context = {'pagename': 'PythonBin'}
    return render(request, 'pages/index.html', context)


def add_zvs_page(request):   #request содержит всю инф.которую мы получаем из браузера
    if request.method == "POST":    #обработка данных полученных из Формы


#        form_date = request.POST
        #print(f"{form_date=}")
#        zvs = Svs_z(
#            name=form_date['name'],
#            lang=form_date['lang'],
#            code=form_date['code']
#        )
#        zvs.save()

        form = ZvsForm(request.POST)
        if form.is_valid():
            form.save()
        return redirect('zvs-list')

    elif request.method == "GET":
        form = ZvsForm()
        context = {
            'pagename': 'Добавление нового ZVS',\
            'form': form
            }
        return render(request, 'pages/add_snippet.html', context)




def svs_z_page(request):
    svs_zs = Svs_z.objects.all()   #все данные из БД
    context = {
        'pagename': 'Просмотр базы svs_z',
        'svs_zs': svs_zs
    }
    return render(request, 'pages/view_svs_z.html', context)


def zvs_detail(request, zvs_id):   #отображение отдельного zvs
    zvs = Svs_z.objects.get(pk=zvs_id)
    context = {
        'pagename': 'Страница отдельного zvs',
        "zvs": zvs,
    }
    return render(request, 'pages/page_zvs.html', context)


