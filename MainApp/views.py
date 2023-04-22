from django.http import Http404
from django.shortcuts import render, redirect
from MainApp.models import Svs_z, Svs_k, Svs_zz
from MainApp.forms import ZvsForm, KvsForm, ZZvsForm, UserRegistrationForm, CommentForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages


def index_page(request):
    print("user= ", request.user)
    if request.user.is_authenticated:  #если авторизован - True
        errors = []
    else:
        errors = ["password or username not correct"]
    context = {
        'pagename': 'Добро пожаловать на сайт 7 otd!',
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

    print("request GET= ", request.GET)
    lang = request.GET.get("lang") #реализация фильтрации по языку программирования
                               #если просто запрос без фильтра, то lang = None
    print(f"{lang=}")
    if lang is not None:
        svs_zs = svs_zs.filter(lang=lang)

    sort = request.GET.get("sort") #извлекаем sort
    print(f"{sort=}")
    if sort == "name":
        svs_zs = svs_zs.order_by(sort) #sort переменная т.е. name
        sort = "-name"
    elif sort == "-name":
        svs_zs = svs_zs.order_by(sort)
        sort = "name"
    else:
        sort = "name"


    context = {
        'pagename': 'Просмотр базы svs_z',
        'svs_zs': svs_zs,
        'lang': lang,
        'sort': sort,
    }
    return render(request, 'pages/view_svs_z.html', context)



def zvs_detail(request, zvs_id):   #отображение отдельного zvs
    zvs = Svs_z.objects.get(pk=zvs_id)
    comment_form = CommentForm()
    comments = zvs.comments.all()  #получаем все комментарии zvs_id
    print (comments)
    context = {
        'pagename': 'Страница отдельного zvs',
        "zvs": zvs,
        "comments": comments,
        "comment_form": comment_form,
    }
    return render(request, 'pages/page_zvs.html', context)


def comment_add(request):    #добавление комментария
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        zvs_id = request.POST['zvs_id']
        print(zvs_id)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.snippet = Svs_z.objects.get(id=zvs_id)
            comment.save()

        return redirect(f'/zvs/{zvs_id}')

    raise Http404


def zvs_delete(request, zvs_id):
    zvs = Svs_z.objects.get(pk=zvs_id) #получаем zvs с нужным ID из BD
    zvs.delete()

    return redirect('zvs-list')




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


@login_required()
def zvs_my(request):
    svs_zs = Svs_z.objects.filter(user=request.user)  #данные из БД для зарегистрированного пользователя
    context = {
        'pagename': 'Просмотр моих svs_z',
        'svs_zs': svs_zs
    }
    return render(request, 'pages/view_svs_z.html', context)




        #KVS

def svs_k_page(request):
    svs_ks = Svs_k.objects.all().order_by('-date')   #все данные из БД

    total_rab = Svs_k.objects.aggregate(Sum('rab'))
    total_test = Svs_k.objects.aggregate(Sum('test'))
    total_priem = Svs_k.objects.aggregate(Sum('priem'))

    print(total_rab)
    print(total_test)
    print(total_priem)
    print(type(total_rab))
    print(type(total_test))
    print(type(total_priem))

    sum_rab = total_rab["rab__sum"]
    sum_test = total_test["test__sum"]
    sum_priem = total_priem["priem__sum"]
    print(sum_priem)


    print("request GET= ", request.GET)
    operator = request.GET.get("operator")  # реализация фильтрации по языку программирования
                                            # если просто запрос без фильтра, то lang = None
    print(f"{operator=}")

    data_start = request.GET.get("date_start")
    data_stop = request.GET.get("date_stop")
    print("date_start= ", data_start)
    print("date_stop= ", data_stop)


    priem_gr = request.GET.get("priem_gr")    #если галочка установлена то priem_gr= on
    print("priem_gr= ", priem_gr)

    if data_start and data_stop is not None:
        data_start = request.GET.get("date_start")
        data_stop = request.GET.get("date_stop")
        svs_ks = Svs_k.objects.filter(date__range=[data_start, data_stop]).order_by('-date')
        print("svs_ks (date)= ", svs_ks)
        total_rab = Svs_k.objects.filter(date__range=[data_start, data_stop]).aggregate(Sum('rab'))
        total_test = Svs_k.objects.filter(date__range=[data_start, data_stop]).aggregate(Sum('test'))
        total_priem = Svs_k.objects.filter(date__range=[data_start, data_stop]).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]

    if operator is not None:
        svs_ks = svs_ks.filter(operator=operator)
        print("svs_ks (operator)= ", svs_ks)
        total_rab = Svs_k.objects.filter(operator=operator).aggregate(Sum('rab'))
        total_test = Svs_k.objects.filter(operator=operator).aggregate(Sum('test'))
        total_priem = Svs_k.objects.filter(operator=operator).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]
        print("sum_priem2= ", sum_priem)

    if priem_gr is not None:
        svs_ks = Svs_k.objects.filter(priem=True)
        print("svs_ks(priem)= ", svs_ks)
        total_rab = Svs_k.objects.filter(priem=True).aggregate(Sum('rab'))
        total_test = Svs_k.objects.filter(priem=True).aggregate(Sum('test'))
        total_priem = Svs_k.objects.filter(priem=True).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]


    if operator and data_start and data_stop is not None:
        data_start = request.GET.get("date_start")
        data_stop = request.GET.get("date_stop")
        svs_ks = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator)
        print("svs_ks (date&operator)= ", svs_ks)
        total_rab = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).aggregate(Sum('rab'))
        total_test = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).aggregate(Sum('test'))
        total_priem = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]

    if data_start and data_stop and operator and priem_gr is not None:
        data_start = request.GET.get("date_start")
        data_stop = request.GET.get("date_stop")
        svs_ks = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).filter(priem=True)
        print("svs_ks (date&operator&priem)= ", svs_ks)
        total_rab = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).filter(priem=True).aggregate(Sum('rab'))
        total_test = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).filter(priem=True).aggregate(Sum('test'))
        total_priem = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).filter(priem=True).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]

    if data_start and data_stop and priem_gr is not None:
        data_start = request.GET.get("date_start")
        data_stop = request.GET.get("date_stop")
        svs_ks = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(priem=True)
        print("svs_ks (date&priem)= ", svs_ks)
        total_rab = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(priem=True).aggregate(Sum('rab'))
        total_test = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(priem=True).aggregate(Sum('test'))
        total_priem = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(priem=True).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]

    if operator and priem_gr is not None:
        svs_ks = Svs_k.objects.filter(operator=operator).filter(priem=True)
        print("svs_ks (date&priem)= ", svs_ks)
        total_rab = Svs_k.objects.filter(operator=operator).filter(priem=True).aggregate(Sum('rab'))
        total_test = Svs_k.objects.filter(operator=operator).filter(priem=True).aggregate(Sum('test'))
        total_priem = Svs_k.objects.filter(operator=operator).filter(priem=True).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]










        # svs_ks = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).filter(priem=True)
        # total_rab = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).filter(priem=True).aggregate(Sum('rab'))
        # total_test = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).filter(priem=True).aggregate(Sum('test'))
        # total_priem = Svs_k.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).filter(priem=True).aggregate(Sum('priem'))
        # sum_rab = total_rab["rab__sum"]
        # sum_test = total_test["test__sum"]
        # sum_priem = total_priem["priem__sum"]








    # if operator is not None:
    #     svs_ks = svs_ks.filter(operator=operator)
    #     total_rab = Svs_k.objects.filter(operator=operator).aggregate(Sum('rab'))
    #     total_test = Svs_k.objects.filter(operator=operator).aggregate(Sum('test'))
    #     total_priem = Svs_k.objects.filter(operator=operator).aggregate(Sum('priem'))
    #     sum_rab = total_rab["rab__sum"]
    #     sum_test = total_test["test__sum"]
    #     sum_priem = total_priem["priem__sum"]
    #     print("sum_priem2= ", sum_priem)
    #
    # if data_start and data_stop is not None:
    #     data_start = request.GET.get("date_start")
    #     data_stop = request.GET.get("date_stop")
    #     print("date_start= ", data_start)
    #     print("date_stop= ", data_stop)
    #
    #     svs_ks = Svs_k.objects.filter(date__range=[data_start, data_stop])
    #     total_rab = Svs_k.objects.filter(date__range=[data_start, data_stop]).aggregate(Sum('rab'))
    #     total_test = Svs_k.objects.filter(date__range=[data_start, data_stop]).aggregate(Sum('test'))
    #     total_priem = Svs_k.objects.filter(date__range=[data_start, data_stop]).aggregate(Sum('priem'))
    #     sum_rab = total_rab["rab__sum"]
    #     sum_test = total_test["test__sum"]
    #     sum_priem = total_priem["priem__sum"]
    #     #print(f"{pool_date=}")
    #
    #
    # if priem_gr is not None:
    #     svs_ks = Svs_k.objects.filter(priem=True)
    #     print("svs_ks= ", svs_ks)
    #
    #     total_rab = Svs_k.objects.filter(priem=True).aggregate(Sum('rab'))
    #     total_test = Svs_k.objects.filter(priem=True).aggregate(Sum('test'))
    #     total_priem = Svs_k.objects.filter(priem=True).aggregate(Sum('priem'))
    #     sum_rab = total_rab["rab__sum"]
    #     sum_test = total_test["test__sum"]
    #     sum_priem = total_priem["priem__sum"]



    #print(total_rab[rab_sum])
    context = {
        'pagename': 'Просмотр базы svs_k',
        'svs_ks': svs_ks,
        'sum_rab': sum_rab,
        'sum_test': sum_test,
        'sum_priem': sum_priem,
        'operator': operator,
        #'pool_date': pool_date,
    }
    return render(request, 'pages/view_svs_k.html', context)



def add_kvs_page(request):   #request содержит всю инф.которую мы получаем из браузера
    if request.method == "POST":    #обработка данных полученных из Формы
#        form_date = request.POST
        #print(f"{form_date=}")
#        zvs = Svs_z(
#            name=form_date['name'],
#            lang=form_date['lang'],
#            code=form_date['code']
#        )
#        zvs.save()
        form = KvsForm(request.POST)
        if form.is_valid():
            zvs = form.save(commit=False)  #отложть сохранение и вернуть объект zvs
                    #    zvs.user = request.user  #данные внес пользователь каторый сейчас зарегестрирован, в поле USER
            zvs.save()
        return redirect('kvs-list')

    elif request.method == "GET":
        form = KvsForm()
        context = {
            'pagename': 'Добавление нового KVS',\
            'form': form
            }
        return render(request, 'pages/add_kvs.html', context)


def kvs_detail(request, kvs_id):   #отображение отдельного kvs
    print("kvs_ID=", kvs_id)
    kvs = Svs_k.objects.get(pk=kvs_id)
    context = {
        'pagename': 'Страница отдельного kvs',
        "kvs": kvs,
    }
    return render(request, 'pages/page_kvs.html', context)



def kvs_delete(request, kvs_id):
    print(kvs_id)
    kvs = Svs_k.objects.get(pk=kvs_id) #получаем kvs с нужным ID из BD
    kvs.delete()
    return redirect('kvs-list')






def foto(request):   #отображение fotoalbom
    print("FOTO")

    context = {
        'pagename': 'Страница фотоальбома',

    }
    return render(request, 'pages/fotoalbom.html', context)


def albom_holiday(request):   #отображение fotoalbom
    print("FOTO")

    context = {
        'pagename': 'Страница фотоальбома',

    }
    return render(request, 'pages/albom_holiday.html', context)










        #ZVS

def svs_zz_page(request):
    svs_zz = Svs_zz.objects.all().order_by('-date')   #все данные из БД

    total_rab = Svs_zz.objects.aggregate(Sum('rab'))
    total_test = Svs_zz.objects.aggregate(Sum('test'))
    total_priem = Svs_zz.objects.aggregate(Sum('priem'))

    print(total_rab)
    print(total_test)
    print(total_priem)
    print(type(total_rab))
    print(type(total_test))
    print(type(total_priem))

    sum_rab = total_rab["rab__sum"]
    sum_test = total_test["test__sum"]
    sum_priem = total_priem["priem__sum"]
    print(sum_priem)


    print("request GET= ", request.GET)
    operator = request.GET.get("operator")  # реализация фильтрации по языку программирования
                                            # если просто запрос без фильтра, то lang = None
    print(f"{operator=}")

    data_start = request.GET.get("date_start")
    data_stop = request.GET.get("date_stop")
    print("date_start= ", data_start)
    print("date_stop= ", data_stop)


    priem_gr = request.GET.get("priem_gr")    #если галочка установлена то priem_gr= on
    print("priem_gr= ", priem_gr)

    if data_start and data_stop is not None:
        data_start = request.GET.get("date_start")
        data_stop = request.GET.get("date_stop")
        svs_zz = Svs_zz.objects.filter(date__range=[data_start, data_stop]).order_by('-date')
        print("svs_zz (date)= ", svs_zz)
        total_rab = Svs_zz.objects.filter(date__range=[data_start, data_stop]).aggregate(Sum('rab'))
        total_test = Svs_zz.objects.filter(date__range=[data_start, data_stop]).aggregate(Sum('test'))
        total_priem = Svs_zz.objects.filter(date__range=[data_start, data_stop]).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]

    if operator is not None:
        svs_zz = svs_zz.filter(operator=operator)
        print("svs_zz (operator)= ", svs_zz)
        total_rab = Svs_zz.objects.filter(operator=operator).aggregate(Sum('rab'))
        total_test = Svs_zz.objects.filter(operator=operator).aggregate(Sum('test'))
        total_priem = Svs_zz.objects.filter(operator=operator).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]
        print("sum_priem2= ", sum_priem)

    if priem_gr is not None:
        svs_zz = Svs_zz.objects.filter(priem=True)
        print("svs_zz(priem)= ", svs_zz)
        total_rab = Svs_zz.objects.filter(priem=True).aggregate(Sum('rab'))
        total_test = Svs_zz.objects.filter(priem=True).aggregate(Sum('test'))
        total_priem = Svs_zz.objects.filter(priem=True).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]


    if operator and data_start and data_stop is not None:
        data_start = request.GET.get("date_start")
        data_stop = request.GET.get("date_stop")
        svs_zz = Svs_zz.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator)
        print("svs_zz (date&operator)= ", svs_zz)
        total_rab = Svs_zz.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).aggregate(Sum('rab'))
        total_test = Svs_zz.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).aggregate(Sum('test'))
        total_priem = Svs_zz.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]

    if data_start and data_stop and operator and priem_gr is not None:
        data_start = request.GET.get("date_start")
        data_stop = request.GET.get("date_stop")
        svs_zz = Svs_zz.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).filter(priem=True)
        print("svs_zz (date&operator&priem)= ", svs_zz)
        total_rab = Svs_zz.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).filter(priem=True).aggregate(Sum('rab'))
        total_test = Svs_zz.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).filter(priem=True).aggregate(Sum('test'))
        total_priem = Svs_zz.objects.filter(date__range=[data_start, data_stop]).filter(operator=operator).filter(priem=True).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]

    if data_start and data_stop and priem_gr is not None:
        data_start = request.GET.get("date_start")
        data_stop = request.GET.get("date_stop")
        svs_zz = Svs_zz.objects.filter(date__range=[data_start, data_stop]).filter(priem=True)
        print("svs_zz (date&priem)= ", svs_zz)
        total_rab = Svs_zz.objects.filter(date__range=[data_start, data_stop]).filter(priem=True).aggregate(Sum('rab'))
        total_test = Svs_zz.objects.filter(date__range=[data_start, data_stop]).filter(priem=True).aggregate(Sum('test'))
        total_priem = Svs_zz.objects.filter(date__range=[data_start, data_stop]).filter(priem=True).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]

    if operator and priem_gr is not None:
        svs_zz = Svs_zz.objects.filter(operator=operator).filter(priem=True)
        print("svs_zz (date&priem)= ", svs_zz)
        total_rab = Svs_zz.objects.filter(operator=operator).filter(priem=True).aggregate(Sum('rab'))
        total_test = Svs_zz.objects.filter(operator=operator).filter(priem=True).aggregate(Sum('test'))
        total_priem = Svs_zz.objects.filter(operator=operator).filter(priem=True).aggregate(Sum('priem'))
        sum_rab = total_rab["rab__sum"]
        sum_test = total_test["test__sum"]
        sum_priem = total_priem["priem__sum"]



    context = {
        'pagename': 'Просмотр базы svs_z',
        'svs_zz': svs_zz,
        'sum_rab': sum_rab,
        'sum_test': sum_test,
        'sum_priem': sum_priem,
        'operator': operator,
        #'pool_date': pool_date,
    }
    return render(request, 'pages/view_svs_zz.html', context)



def add_zzvs_page(request):   #request содержит всю инф.которую мы получаем из браузера
    if request.method == "POST":    #обработка данных полученных из Формы

        form = ZZvsForm(request.POST)
        if form.is_valid():
            zzvs = form.save(commit=False)  #отложть сохранение и вернуть объект zvs
                    #    zvs.user = request.user  #данные внес пользователь каторый сейчас зарегестрирован, в поле USER
            zzvs.save()
        return redirect('zzvs-list')

    elif request.method == "GET":
        form = ZZvsForm()
        context = {
            'pagename': 'Добавление нового ZZVS',\
            'form': form
            }
        return render(request, 'pages/add_zzvs.html', context)


def zzvs_detail(request, zzvs_id):   #отображение отдельного kvs
    print("zzvs_ID=", zzvs_id)
    zzvs = Svs_zz.objects.get(pk=zzvs_id)
    context = {
        'pagename': 'Страница отдельного zzvs',
        "zzvs": zzvs,
    }
    return render(request, 'pages/page_zzvs.html', context)



def zzvs_delete(request, zzvs_id):
    print(zzvs_id)
    zzvs = Svs_zz.objects.get(pk=zzvs_id) #получаем kvs с нужным ID из BD
    zzvs.delete()
    return redirect('zzvs-list')



