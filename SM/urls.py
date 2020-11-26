
from django.contrib import admin
from django.urls import path,include
from App import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login),
    path('login/',views.login,name = "login"),
    path('register/',views.register,name = "register"),
    path('home/', views.home,name = "home"),
    path('category/<categoryname>/',views.Category,name = "category"),
    path('logout/',views.Logout,name = "logout"),
    path('newpost/',views.newpost,name = "newpost"),
    path('deletepost/<id>/',views.deletepost,name = 'deletepost'),
    path('like/<id>/',views.likepost),
    path('dislike/<id>/',views.dislikepost),
    path('comment/<id>/',views.comment),
    path('commentdelete/<id>/',views.commentdelete),
    path('save/<id>/',views.save),
    path('savedelete/<id>/',views.savedelete),
    path('profile/',views.profile,name = "profile"),
    path('saves/',views.saves,name = "saves"),
    path('favorites/',views.favorite,name = "favorites"),
    path('profileupdate/',views.updateprofile),
    path('userprofile/<id>/',views.userprofile,name = "userprofile"),
    path('notification/<type>/',views.notification),
    path('delnotification/',views.deletenotification),
    path("password-reset", auth_views.PasswordResetView.as_view( template_name="password/reset_password.html"), name="reset_password"),
    path("password-reset/done/", auth_views.PasswordResetDoneView.as_view( template_name="password/password_reset_done.html"), name="password_reset_done"),
    path("password-reset-confirm/<uidb64>/<token>/", auth_views.PasswordResetConfirmView.as_view( template_name="password/password_reset_confirm.html"), name="password_reset_confirm"),
    path("password-reset-complete/", auth_views.PasswordResetCompleteView.as_view( template_name="password/password_reset_complete.html"), name="password_reset_complete"),
    path("readnotification/<id>/",views.readNotification),
]
