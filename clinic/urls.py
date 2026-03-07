from django.contrib import admin
from django.urls import path
from appointments import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home),
    path('book/', views.book),
    path('success/', views.success),
]