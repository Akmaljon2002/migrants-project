from django.urls import path
from apps.users import views

urlpatterns = [
    path('create/', views.create_user, name='user_create'),
    path('get/', views.list_users, name='get_users'),
    path('update/user/<int:pk>', views.update_user, name='update_user'),
    path('delete/user/<int:pk>', views.delete_user, name='delete_user'),
    path('get/user/<int:pk>', views.get_user, name='get_user'),
    path('get/current/', views.get_current_user, name='get_current_user'),
    path('login/', views.login, name='user_login'),
    path('logout/', views.logout, name='user_logout'),
]
