from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('zvs/add', views.add_zvs_page, name='zvs-add'),
    path('zvs/list', views.svs_z_page, name='zvs-list'),

    path('zvs/<int:zvs_id>/', views.zvs_detail, name='zvs-detail'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
