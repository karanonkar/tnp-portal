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

        jobs_with_count = []

        for job in company_jobs:
            applications_count = Application.objects.filter(job=job).count()

            jobs_with_count.append({
                'job': job,
                'applications_count': applications_count
            })

        context = {
            'jobs_with_count': jobs_with_count
    }

        return render(request, 'accounts/company_dashboard.html', context)

        

    # ================= STUDENT =================
    elif user.role == 'student':

        jobs = Job.objects.all().order_by('-created_at')

        applications = Application.objects.filter(student=user)

        applied_job_ids = applications.values_list('job_id', flat=True)

        context = {
        '   jobs': jobs,
            'applied_job_ids': list(applied_job_ids)
        }

        return render(request, 'accounts/student_dashboard.html', context)

    # ================= TPO =================
    elif user.role == 'tpo':

        total_users = User.objects.count()
        total_students = User.objects.filter(role='student').count()
        total_companies = User.objects.filter(role='company').count()
        total_jobs = Job.objects.count()
        total_applications = Application.objects.count()

        context = {
            'total_users': total_users,
            'total_students': total_students,
            'total_companies': total_companies,
            'total_jobs': total_jobs,
            'total_applications': total_applications,
        }

        return render(request, 'accounts/tpo_dashboard.html', context)

    # ================= SUPERUSER =================
    elif user.is_superuser:
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

#add job post view

@login_required
def post_job(request):

    if request.user.role != 'company':
        return redirect('dashboard')

    if request.method == 'POST':

        Job.objects.create(
            company=request.user.company,
            title=request.POST.get('title'),
            description=request.POST.get('description'),
            package=request.POST.get('package'),
            last_date=request.POST.get('last_date'),

            min_10th_percentage=request.POST.get('min_10th_percentage') or None,
            min_12th_percentage=request.POST.get('min_12th_percentage') or None,
            min_diploma_percentage=request.POST.get('min_diploma_percentage') or None,
            min_bachelor_percentage=request.POST.get('min_bachelor_percentage') or None,
            min_master_percentage=request.POST.get('min_master_percentage') or None,

            max_current_backlogs=request.POST.get('max_current_backlogs') or None,
            max_history_backlogs=request.POST.get('max_history_backlogs') or None,
        )

        messages.success(request, "Job Posted Successfully!")
        return redirect('dashboard')

    return render(request, 'accounts/post_job.html')

@login_required
def my_applications(request):
    if request.user.role != 'student':
        return redirect('dashboard')

    applications = Application.objects.filter(
        student=request.user
    ).select_related('job')

    return render(request, 'accounts/my_applications.html', {
        'applications': applications
    })
# ======================
# LOGOUT VIEW
# ======================

def user_logout(request):
    logout(request)
    return redirect('login')

@login_required
def job_applicants(request, job_id):

    if request.user.role != 'company':
        return redirect('dashboard')

    job = get_object_or_404(Job, id=job_id, company=request.user.company)

    applications = Application.objects.filter(
        job=job
    ).select_related('student')

    return render(request, 'accounts/job_applicants.html', {
        'job': job,
        'applications': applications
    })

@login_required
def update_application_status(request, app_id, status):

    if request.user.role != 'company':
        return redirect('dashboard')

    application = get_object_or_404(Application, id=app_id)

    # Security: company can update only their job applications
    if application.job.company != request.user.company:
        return redirect('dashboard')

    if status in ['shortlisted', 'rejected']:
        application.status = status
        application.save()

    return redirect('job_applicants', job_id=application.job.id)