from django.urls import path, include

urlpatterns = [
    path('ips/', include('middleware.urls')),
    path('api-user/', include('user_management.urls')),
    path('api-todo/', include('user_todo.urls')),
]
