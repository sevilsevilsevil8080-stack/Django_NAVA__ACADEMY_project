from django.db import models
from django.contrib.auth.models import User


class StudentProfile(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )

    phone = models.CharField(
        max_length=15,
        verbose_name='شماره موبایل'
    )

    address = models.TextField(
        blank=True,
        verbose_name='آدرس'
    )

    profile_image = models.ImageField(
        upload_to='students/',
        blank=True,
        null=True,
        verbose_name='عکس پروفایل'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت نام'
    )

    def str(self):
        return self.user.get_full_name() or self.user.username














class Course(models.Model):

    title = models.CharField(
        max_length=200,
        verbose_name='عنوان دوره'
    )

    description = models.TextField(
        verbose_name='توضیحات دوره'
    )

    teacher = models.CharField(
        max_length=150,
        verbose_name='مدرس'
    )

    capacity = models.PositiveIntegerField(
        verbose_name='ظرفیت'
    )

    price = models.PositiveIntegerField(
        verbose_name='شهریه'
    )

    start_date = models.DateField(
        verbose_name='تاریخ شروع'
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name='فعال'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    def str(self):
        return self.title















class Enrollment(models.Model):

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='enrollments'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ثبت نام'
    )











    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'course'],
                name='unique_student_course'
            )
        ]

    def str(self):
        return f'{self.student.username} - {self.course.title}'











class Payment(models.Model):

    STATUS_CHOICES = [
        ('pending', 'در انتظار پرداخت'),
        ('paid', 'پرداخت شده'),
        ('failed', 'ناموفق'),
    ]

    enrollment = models.OneToOneField(
        Enrollment,
        on_delete=models.CASCADE,
        related_name='payment',
        verbose_name='ثبت‌نام'
    )

    amount = models.PositiveIntegerField(
        verbose_name='مبلغ'
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='وضعیت پرداخت'
    )

    transaction_id = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='شماره تراکنش'
    )

    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='تاریخ پرداخت'
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='تاریخ ایجاد'
    )

    @property
    def student(self):
        return self.enrollment.student

    @property
    def course(self):
        return self.enrollment.course

    def str(self):
        return f'{self.enrollment.student.username} - {self.amount}'













