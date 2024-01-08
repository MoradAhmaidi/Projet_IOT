from django.urls import path
from . import views
from . import api
urlpatterns = [
  path('', views.home, name='home'),
  path('api', api.dhtser, name='json'),
  path('login', views.login, name='login'),
  path('logout', views.logout, name='logout'),
  path('user/list', views.userlist, name='userlist'),
  path('user/add', views.useradd, name='useradd'),
  path('user/update/<int:id>/', views.userupdate, name='userupdate'),
  path('user/delete/<int:id>/', views.userdetele, name='userdetele'),
  path('parametres/messages', views.messagelist, name='messagelist'),
  path('parametres/messages/<str:name>', views.messageupdate, name='messageupdate'),
  path('parametres/norms/<str:name>', views.normsupdate , name='normsupdate'),
  path('parametres/notification' , views.home , name='list'),
  path('parametres/notification/update' , views.home , name='update'),
]
