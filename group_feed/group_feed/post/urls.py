from django.urls import path

from . import views

app_name='post'

urlpatterns = [
    path("", views.PostList.as_view(), name="all"),
    path("new/", views.CreatePost.as_view(), name="create"),
    path("by/<str:username>/",views.UserPosts.as_view(),name="for_user"),
    path("by/<str:username>/<int:pk>/",views.PostDetail.as_view(),name="single"),
    path("delete/<int:pk>/",views.DeletePost.as_view(),name="delete"),
    path('post/<int:pk>/comment/',views.add_comment_to_post,name='add_comment'),
    path('comment/<int:pk>/remove/',views.remove_comment,name='remove_comment'),
]
