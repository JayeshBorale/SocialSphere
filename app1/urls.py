from django.urls import path,include

from . import views
urlpatterns = [

    path('',views.home,name="home"),
    path('login/',views.login_view,name="login"),
    path('signup/',views.signup,name="signup"),
    path('profile/',views.user_profiles,name="profile"),
    path('user_profile/<int:pk>',views.user_profile_page,name="user_profile"),
    path('followers/<pk>',views.user_followers,name="user_followers"),
    path('following/<pk>',views.user_following,name="following"),
    path('edit_bio',views.edit_bio,name="edit_bio"),
    

]
