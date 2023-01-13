from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Svs_z, Svs_k
from MainApp.forms import ZvsForm, UserRegistrationForm
from django.contrib import auth


def index_page(request):
    print("user= ", request.user)
    if request.user.is_authenticated:  #если авторизован - True
        errors = []
    else:
        errors = ["password or username not correct"]
    context = {
        'pagename': 'PythonBin',
        'errors': errors
    }

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
            zvs = form.save(commit=False)  #отложть сохранение и вернуть объект zvs
            zvs.user = request.user  #данные внес пользователь каторый сейчас зарегестрирован, в поле USER
            zvs.save()
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


def login_page(request):   #форма логирования
   if request.method == 'POST':
       username = request.POST.get("username")
       password = request.POST.get("password")
       # print("username =", username)
       # print("password =", password)
       user = auth.authenticate(request, username=username, password=password)
       if user is not None:
           auth.login(request, user)  #создается токин авторизации отправляемый пользователю
       else:
           # Return error message
           pass
   return redirect('home')


def logout_page(request):   #разлогирование
    auth.logout(request)
    return redirect('home')


def registration(request):  #создание пользователя
    if request.method == "POST":    #создаем пользоателя
        form = UserRegistrationForm(request.POST)   #форма с заполненными данными пользователем каторые пришли
        if form.is_valid():
            form.save()   #сохраняем в bd
            return redirect('home')
        else:                       #если не валидные данные
            #print("errors= ", form.errors.items())  #для просмотра ошибок в терминале (словарик)
            context = {'form': form}
            return render(request, 'pages/registration.html', context)
    elif request.method == "GET":   #вернуть страницу с формой
        form = UserRegistrationForm()   #возврат пустой формы
        context = {'form': form}
        return render(request, 'pages/registration.html', context)


def zvs_my(request):
    svs_zs = Svs_z.objects.filter(user=request.user)  #данные из БД для зарегистрированного пользователя
    context = {
        'pagename': 'Просмотр моих svs_z',
        'svs_zs': svs_zs
    }
    return render(request, 'pages/view_svs_z.html', context)




#KVS

def svs_k_page(request):
    svs_ks = Svs_k.objects.all()   #все данные из БД
    context = {
        'pagename': 'Просмотр базы svs_k',
        'svs_ks': svs_ks
    }
    return render(request, 'pages/view_svs_k.html', context)