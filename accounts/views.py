from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib import messages
from .models import User, Job, Application


# ======================
# LOGIN VIEW
# ======================

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid username or password'
            })

    return render(request, 'accounts/login.html')


# ======================
# DASHBOARD VIEW
# ======================

@login_required
def dashboard(request):
    user = request.user

    # ================= HOD =================
    if user.role == 'hod':

        total_students = User.objects.filter(
            role='student',
            department=user.department
        ).count()

        total_users = User.objects.count()
        total_jobs = Job.objects.count()

        context = {
            'total_students': total_students,
            'total_users': total_users,
            'total_jobs': total_jobs
        }

        return render(request, 'accounts/hod_dashboard.html', context)


    # ================= COMPANY =================
    elif user.role == 'company':

        company_jobs = Job.objects.filter(company=user.company)
        total_jobs = company_jobs.count()

        context = {
            'company_jobs': company_jobs,
            'total_jobs': total_jobs
        }

        return render(request, 'accounts/company_dashboard.html', context)


    # ================= STUDENT =================
    elif user.role == 'student':

        jobs = Job.objects.all().order_by('-created_at')

        context = {
            'jobs': jobs
        }

        return render(request, 'accounts/student_dashboard.html', context)


    # ================= TPO =================
    elif user.role == 'tpo':

        total_users = User.objects.count()
        total_jobs = Job.objects.count()

        context = {
            'total_users': total_users,
            'total_jobs': total_jobs
        }

        return render(request, 'accounts/tpo_dashboard.html', context)


    # ================= ADMIN =================
    if user.is_superuser:
        return redirect('/admin/')

    return HttpResponse("No dashboard available for this role.")


# ======================
# APPLY JOB VIEW
# ======================

@login_required
def apply_job(request, job_id):

    if request.user.role != 'student':
        return redirect('dashboard')

    job = get_object_or_404(Job, id=job_id)

    # Prevent duplicate apply
    already_applied = Application.objects.filter(
        student=request.user,
        job=job
    ).exists()

    if already_applied:
        messages.warning(request, "You already applied for this job.")
        return redirect('dashboard')

    Application.objects.create(
        student=request.user,
        job=job
    )

    messages.success(request, "Successfully Applied!")
    return redirect('dashboard')


# ======================
# LOGOUT VIEW
# ======================

def user_logout(request):
    logout(request)
    return redirect('login')