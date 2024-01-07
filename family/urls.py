from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [

    path('' , views.home , name="home"),
    path('faq/' , views.faq , name="faq"),
    path('login/' , views.loginPage , name="login"),
    path('register/' , views.registerPage , name = 'register'),
    path('logout/' , views.logoutPage , name = 'logout'),

    path('map/' , views.map , name="map"),

    path('birthdaywish/<str:pk>/' , views.pdf , name="pdf"),
    path('birthday/' , views.birthdayList , name="birthdayList"),

    path('member/profile/edit/<str:pk>/' , views.edit_profile , name = 'edit'),
    path('member/profile/<str:pk>/' , views.viewProfile , name = 'viewProfile'),
    path('member/' , views.viewMember , name="viewMember"),
    path('member/contact' , views.contact , name="contact"),
    path('member/elders/' , views.leaders , name="leaders"),
    path('member/admins/' , views.seeadmins , name="seeadmins"),

    path('interest/' , views.interest , name="interest"),
    path('interest/islam/<str:pk>' , views.islam , name="islam"),
    path('interest/islam/para/<str:pk>' , views.para , name="para"),
    path('interest/islam/story/<str:pk>' , views.story , name="story"),
    path('interest/room/<str:pk>' , views.Room , name="room"),
    path('interest/room/delete_message/<str:pk>' , views.delete_message , name="delete_message"),

    path('gamehouse/' , views.gamehouse , name="gamehouse"),
    path('gamehouse/<str:pk>' , views.playgame , name="play"),
    path('gamehouse/leaderboard/<str:pk>/' , views.leaderboard , name="leaderboard"),


    # reset password
    path('reset_password/' , auth_views.PasswordResetView.as_view(template_name = "reset/reset_password.html") , name = "reset_password"),
    path('reset_password_sent/' , auth_views.PasswordResetDoneView.as_view(template_name = "reset/password_reset_sent.html") , name = "password_reset_done"),
    path('reset/<uidb64>/<token>' , auth_views.PasswordResetConfirmView.as_view(template_name = "reset/reset_form.html") , name = "password_reset_confirm"),
    path('reset_password_complete/' , auth_views.PasswordResetCompleteView.as_view(template_name = "reset/password_reset_done.html") , name = "password_reset_complete"),


]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)