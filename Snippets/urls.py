from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('zvs/add', views.add_zvs_page, name='zvs-add'),
    path('zvs/list', views.svs_z_page, name='zvs-list'),
    path('zvs/<int:zvs_id>/', views.zvs_detail, name='zvs-detail'),

    path('zvs/zvs-my', views.zvs_my, name='zvs-my'),

    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),

    path('register/', views.registration, name='register'),


    path('kvs/list', views.svs_k_page, name='kvs-list'),
    path('kvs/add', views.add_kvs_page, name='kvs-add'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
