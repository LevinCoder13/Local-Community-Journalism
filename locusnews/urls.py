from django.urls import path
from .import views

urlpatterns = [
    path('',views.home,name='home'),

    path('loginview',views.loginview,name='loginview'),
    path('approval',views.approval,name='approval'),

    path('registerview',views.registerview,name='registerview'),
    path('register',views.register,name='register'),

    path('commonuser',views.commonuser,name='commonuser'),
    path('postnews',views.postnews,name='postnews'),


    path('journal',views.journal,name='journal'),

    path('handlelogout/',views.handlelogout, name='handlelogout'), 

    path('toggle_vote/<int:news_id>/', views.toggle_vote, name='toggle_vote'),
 
]

# path('',views.,name=''),