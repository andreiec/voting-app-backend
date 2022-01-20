from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('votes/', views.getVotes),
    path('votes/<str:pk>/', views.getVote),
    path('add-vote/', views.insertVote),
]
