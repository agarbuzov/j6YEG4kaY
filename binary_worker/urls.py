from django.urls import path, include
from .views import Create, Read, Update, Delete, Search

urlpatterns = [
    path('create/', Create.as_view(), name='create'),  # добавлять пары ключ/значение
    path('read/', Read.as_view(), name='read'),  # выводить список всех ключей
    path('update/', Update.as_view(), name='update'),  # изменять значение по ключу
    path('delete/', Delete.as_view(), name='delete'),  # удалять пары ключ/значение
    path('search/', Search.as_view(), name='search'),  # осуществлять поиск подстроки во всех значениях
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
