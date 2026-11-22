from django.urls import path, re_path

from . import views

app_name = 'cursora'

urlpatterns = [
    path('', views.index, name='home'),
    path('info/', views.info, name='info'),
    path('log/', views.log, name='log'),
    re_path(r'^accesare(?P<accesare_id>\d+)/?$', views.detalii_accesare, name='detalii_accesare'),
    path('despre/', views.despre, name='despre'),
    path('istoric/', views.istoric, name='istoric'),
    path('produse/', views.in_lucru, name='produse'),
    path('contact/', views.in_lucru, name='contact'),
    path('cos-virtual/', views.in_lucru, name='cos_virtual'),
    path('instructori/', views.in_lucru, name='instructori'),
    path('intrebari-frecvente/', views.in_lucru, name='intrebari_frecvente'),
]
