from .views import *
from django.urls import path,include

urlpatterns = [
    path('', index, name='index'),
    path('login/', user_login, name='login'),
    path('signup/', signup, name='signup'),
    path('home/logout/', user_logout, name='logout'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
         activate, name='activate'),
    path('search/', include('haystack.urls')),

]