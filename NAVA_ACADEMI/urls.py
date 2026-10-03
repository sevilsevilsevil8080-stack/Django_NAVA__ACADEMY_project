from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_student, name='register'),
    path('signup/', views.signup, name='signup'),
    path('dashboard/', views.student_dashboard, name='student_dashboard'),
    path(
    'notifications/<int:notification_id>/read/',
    views.mark_notification_read,
    name='mark_notification_read'),
    path('login/', views.login_student, name='login'),
    path('logout/', views.logout_student, name='logout'),
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path(
    'courses/<int:course_id>/enroll/',
    views.enroll_course,
    name='enroll_course'),
    path(
    'payments/<int:payment_id>/',
    views.payment_page,
    name='payment_page'),
    
]