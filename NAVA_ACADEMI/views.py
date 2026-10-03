from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import StudentRegistrationForm
from .models import StudentProfile, Course, Enrollment, Payment, Notification


def register_student(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )

            StudentProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )

            login(request, user)

            return redirect('student_dashboard')

    else:
        form = StudentRegistrationForm()

    return render(
        request,
        'nava_academy/register.html',
        {'form': form}
    )












def signup(request):
    if request.method == 'POST':
        form = StudentRegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
            )

            StudentProfile.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                address=form.cleaned_data['address'],
            )

            login(request, user)

            return redirect('student_dashboard')

    else:
        form = StudentRegistrationForm()

    return render(
        request,
        'nava_academy/signup.html',
        {'form': form}
    )











def login_student(request):
    error = None

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # حالت اول: کاربران معمولی که username آنها همان email است
        user = authenticate(
            request,
            username=email,
            password=password,
        )

        # حالت دوم: پیدا کردن کاربر از طریق email
        if user is None:
            try:
                account = User.objects.get(email=email)

                user = authenticate(
                    request,
                    username=account.username,
                    password=password,
                )

            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            return redirect('student_dashboard')

        error = 'ایمیل یا رمز عبور اشتباه است.'

    return render(
        request,
        'nava_academy/login.html',
        {'error': error}
    )











@login_required(login_url='login')
def student_dashboard(request):

    user = request.user

    profile = user.student_profile

    enrollments = Enrollment.objects.filter(
        student=user,
        payment__status='paid'
    ).select_related('course')

    pending_payments = Payment.objects.filter(
        enrollment__student=user,
        status='pending'
    ).select_related(
        'enrollment__course'
    )

    notifications = Notification.objects.filter(
    user=user
    ).order_by('-created_at')

    unread_notifications = notifications.filter(
        is_read=False
    )

    read_notifications = notifications.filter(
        is_read=True
    )

    unread_notifications_count = unread_notifications.count()


    return render(
        request,
        'nava_academy/dashboard.html',
        {
            'user': user,
            'profile': profile,
            'enrollments': enrollments,
            'pending_payments': pending_payments,
            'unread_notifications': unread_notifications,
            'read_notifications': read_notifications,
            'unread_notifications_count': unread_notifications_count,
        }
    )







@login_required(login_url='login')
def mark_notification_read(request, notification_id):

    notification = get_object_or_404(
        Notification,
        id=notification_id,
        user=request.user
    )

    notification.is_read = True
    notification.save(update_fields=['is_read'])

    return redirect('student_dashboard')









def logout_student(request):
    logout(request)
    return redirect('login')









def course_list(request):

    courses = Course.objects.filter(
        is_active=True
    ).order_by('start_date')

    return render(
        request,
        'nava_academy/courses.html',
        {
            'courses': courses,
        }
    )












@login_required(login_url='login')
def course_detail(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        is_active=True
    )

    # تعداد ثبت‌نام‌های فعلی دوره
    enrolled_count = Enrollment.objects.filter(
        course=course
    ).count()

    return render(
        request,
        'nava_academy/course_detail.html',
        {
            'course': course,
            'enrolled_count': enrolled_count,
        }
    )








@login_required(login_url='login')
def enroll_course(request, course_id):

    course = get_object_or_404(
        Course,
        id=course_id,
        is_active=True
    )

    # بررسی ثبت‌نام قبلی کاربر
    existing_enrollment = Enrollment.objects.filter(
        student=request.user,
        course=course
    ).first()

    if existing_enrollment:

        payment = Payment.objects.filter(
            enrollment=existing_enrollment
        ).first()

        # اگر پرداخت قبلاً انجام شده
        if payment and payment.status == 'paid':
            return render(
                request,
                'nava_academy/course_detail.html',
                {
                    'course': course,
                    'message': 'شما قبلاً شهریه این دوره را پرداخت کرده‌اید.'
                }
            )

        # اگر پرداخت وجود دارد ولی پرداخت نشده
        if payment:
            return redirect(
                'payment_page',
                payment_id=payment.id
            )

        # اگر ثبت‌نام وجود دارد ولی Payment ندارد
        payment = Payment.objects.create(
            enrollment=existing_enrollment,
            amount=course.price
        )

        return redirect(
            'payment_page',
            payment_id=payment.id
        )

    # ==============================
    # بررسی ظرفیت دوره
    # ==============================

    enrolled_count = Enrollment.objects.filter(
        course=course
    ).count()

    if enrolled_count >= course.capacity:
        return render(
            request,
            'nava_academy/course_detail.html',
            {
                'course': course,
                'message': 'ظرفیت این دوره تکمیل شده است.'
            }
        )

    # ==============================
    # ایجاد ثبت‌نام جدید
    # ==============================

    enrollment = Enrollment.objects.create(
        student=request.user,
        course=course
    )

    # ==============================
    # ایجاد اعلان ثبت‌نام
    # ==============================

    Notification.objects.create(
        user=request.user,

        title_fa='ثبت‌نام در دوره',
        message_fa=f'ثبت‌نام شما در دوره «{course.title}» با موفقیت انجام شد.',

        title_en='Course Enrollment',
        message_en=f'You have successfully enrolled in the course "{course.title}".',
    )

    # ==============================
    # ایجاد پرداخت
    # ==============================

    payment = Payment.objects.create(
        enrollment=enrollment,
        amount=course.price
    )

    return redirect(
        'payment_page',
        payment_id=payment.id
    )


@login_required(login_url='login')
def payment_page(request, payment_id):

    payment = get_object_or_404(
        Payment,
        id=payment_id,
        enrollment__student=request.user
    )

    if request.method == 'POST':

        payment.status = 'paid'

        payment.transaction_id = f'TXN-{payment.id}-{request.user.id}'

        from django.utils import timezone
        payment.paid_at = timezone.now()

        payment.save()

        return redirect('student_dashboard')

    return render(
        request,
        'nava_academy/payment.html',
        {
            'payment': payment,
        }
    )


