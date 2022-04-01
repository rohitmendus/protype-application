from django.urls import path
from . import views

urlpatterns = [
    path('users/', views.UsersView.as_view(), name="users"),
    path('user-delete/<int:id>', views.UsersDelete.as_view(), name="user-delete"),
    path('user-edit/', views.UsersEdit.as_view(), name="user-edit"),
]