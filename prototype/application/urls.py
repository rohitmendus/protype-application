from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogOutView.as_view(), name="logout"),
    path('users/', views.UsersView.as_view(), name="users"),
    path('user-delete/<int:id>', views.UsersDelete.as_view(), name="user-delete"),
    path('user-edit/<int:id>', views.UsersEdit.as_view(), name="user-edit"),
    path('programmes/', views.ProgrammesView.as_view(), name="programmes"),
    path('programme-delete/<int:id>', views.ProgrammesDelete.as_view(), name="programme-delete"),
    path('programme-edit/<int:id>', views.ProgrammesEdit.as_view(), name="programme-edit"),
    path('departments/', views.DepartmentsView.as_view(), name="departments"),
    path('download_user_dept/', views.DownloadFileUser.as_view(), name="download_user_dept"),
    path('upload_user_dept/', views.UploadUserDeptView.as_view(), name="upload_user_dept"),
    path('download_pgm_dept/', views.DownloadFileProgramme.as_view(), name="download_pgm_dept"),
    path('upload_pgm_dept/', views.UploadProgrammeDeptView.as_view(), name="upload_pgm_dept")
]