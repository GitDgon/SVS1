from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from MainApp import views

urlpatterns = [
    path('', views.index_page, name='home'),
    path('snippets/add', views.add_snippet_page, name='svs-add'),
    path('snippets/list', views.svs_z_page, name='svs-list'),

    path('zvs/<int:zvs_id>/', views.zvs_detail, name='zvs-detail'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
