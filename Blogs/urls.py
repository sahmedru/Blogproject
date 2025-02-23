from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("", views.posts_list, name='posts_list'),
    path("post/<int:id>/", views.post_detail, name='post_detail'),  
    path("post/<int:id>/like/", views.like_post, name='like_post'),
    path("login/", auth_views.LoginView.as_view (template_name="registration/login.html"), name='login'),
    path("logout/", views.logout_view, name='logout'),
    path("signup/", views.signup, name='signup'),
    path("create/", views.create_post, name='create_post'),
    path("update/<int:id>/", views.post_update, name='post_update'),
    path("delete/<int:id>", views.post_delete, name='post_delete'),

]
