from django.contrib import admin
from .models import StudentProfile, Course, Enrollment, Payment, Notification

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'phone',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__first_name',
        'user__last_name',
        'phone',
    )








@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'teacher',
        'capacity',
        'price',
        'start_date',
        'is_active',
    )

    list_filter = (
        'is_active',
        'start_date',
    )

    search_fields = (
        'title',
        'teacher',
    )











@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'course',
        'created_at',
    )

    list_filter = (
        'course',
        'created_at',
    )

    search_fields = (
        'student__username',
        'student__first_name',
        'student__last_name',
        'course__title',
    )















@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = (
        'student',
        'course',
        'amount',
        'status',
        'transaction_id',
        'created_at',
    )

    list_filter = (
        'status',
        'created_at',
    )

    search_fields = (
        'enrollmentstudentusername',
        'enrollmentstudentfirst_name',
        'enrollmentstudentlast_name',
        'enrollmentcoursetitle',
        'transaction_id',
    )














@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):

    list_display = (
        'user',
        'title_fa',
        'title_en',
        'is_read',
        'created_at',
    )

    list_filter = (
        'is_read',
        'created_at',
    )

    search_fields = (
        'user__username',
        'user__email',
        'title_fa',
        'title_en',
        'message_fa',
        'message_en',
    )

    ordering = (
        '-created_at',
    )