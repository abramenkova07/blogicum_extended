from django.urls import path

from . import views


app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(),
         name='index'),
    path('posts/<int:pk>/', views.post_detail,
         name='post_detail'),
    path('posts/create/', views.post_modify,
         name='create_post'),
    path('posts/<int:pk>/edit/', views.post_modify,
         name='edit_post'),
    path('posts/<int:pk>/delete/', views.post_delete,
         name='delete_post'),
    path('profile/<slug:username>/', views.show_profile,
         name='profile'),
    path('edit_profile/', views.profile_edit,
         name='edit_profile'),
    path('posts/<int:pk>/comment/', views.comment_modify,
         name='add_comment'),
    path('posts/<int:pk>/edit_comment/<int:id>/', views.comment_modify,
         name='edit_comment'),
    path('posts/<int:pk>/delete_comment/<int:id>/', views.comment_delete,
         name='delete_comment'),
    path('category/<slug:category_slug>/', views.category_posts,
         name='category_posts'),
]
