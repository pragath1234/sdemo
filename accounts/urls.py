from django.urls import path
from . import views

from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('', views.home, name='home'),
    path('accounts/mainframe/', views.upload, name='mainframe'),
    path(r'^external/', views.external,name='external'),
    path(r'^external_excel/', views.external_excel,name='external_excel'),
    path(r'^multiple_excel/', views.multiple_excel,name='multiple_excel'),

    path(r'^xls/', views.export, name='export'),
    path(r'^csv/', views.export_csv, name='export_csv'),
    path(r'^json/', views.export_json, name='export_json'),
    path('accounts/register/', views.register, name='register'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(next_page='home'), name='logout')
]
