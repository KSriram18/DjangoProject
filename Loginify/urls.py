from django.urls import path
from . import views

urlpatterns = [
   path('signup/', views.signup,name="signup"),
   path('login/', views.login,name="login"),
   path('confirmation/',views.confirmation,name="confirmation"),
   path('success/', views.success,name="success"),
   path('allusers/',views.getalluserdetails),
   path('singleuser/<pk>/',views.singleuserusingbyemail),
   path('updateuser/<pk>/',views.UpdateUserdetails),
   path('deleteuser/<pk>/',views.deleteUserdetails),
]
