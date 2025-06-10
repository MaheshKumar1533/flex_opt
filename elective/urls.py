from django.urls import path
from . import views

urlpatterns = [
    # Student URLs
    path('', views.home, name='home'),
    path('login/', views.student_login, name='student_login'),
    path('logout/', views.student_logout, name='student_logout'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path('quiz/<int:quiz_id>/', views.quiz_detail, name='quiz_detail'),
    path('quiz/<int:quiz_id>/submit/', views.submit_quiz_response, name='submit_quiz_response'),

    # Admin URLs
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/create-quiz/', views.create_quiz, name='create_quiz'),
    path('admin/quiz/<int:quiz_id>/assign/', views.assign_students, name='assign_students'),
    path('admin/quiz/<int:quiz_id>/results/', views.quiz_results, name='quiz_results'),
    path('admin/subject-overview/', views.subject_overview, name='subject_overview'),
    path('admin/add-students/', views.add_students, name='add_students'),
    path('api/quiz-stats/', views.get_quiz_stats_api, name='quiz_stats_api'),
]
