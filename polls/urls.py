from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:question_id>/', views.detail, name='detail'),
    path('add-poll/', views.add_poll, name='add_poll'),
    path('choices/<int:question_id>/', views.choice_list, name='choices'),
    path('<int:question_id>/results/', views.results, name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
    path('questions/', views.all_questions, name='all_questions'),
]
