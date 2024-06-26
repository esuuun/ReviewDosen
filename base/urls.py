from django.urls import path
from . import views

urlpatterns = [

    path('',views.landingPage, name='landing-page'),
    path('home/',views.home, name='home'),
    path('dosen/<str:pk>/', views.dosen, name='dosen'),
    path('create-dosen/', views.createDosen, name='create-dosen'),
    path('edit-dosen/<str:pk>/', views.editDosen, name='edit-dosen'),
    path('delete-dosen/<str:pk>/', views.deleteDosen, name='delete-dosen'),

    path('create-review/<str:pk>/',views.createReview, name='create-review'),
    path('delete-review/<str:pk>/',views.deleteReview, name='delete-review'),
    path('edit-review/<str:pk>/',views.editReview, name='edit-review'),

    path('dashboard/',views.dashboard,name='user-dashboard')

]
