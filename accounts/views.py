from django.shortcuts import render ,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout


#login view
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
    
#dashboard view
@login_required
def dashboard(request):
    user=request.user

    if user.role == 'student':
        return render(request, 'student_dashboard.html')
    elif user.role == 'company':
        return render(request, 'company_dashboard.html')
    elif user.role == 'hod':
        return render(request, 'hod_dashboard.html')
    elif user.role == 'tpo':
        return render(request, 'tpo_dashboard.html')
    
#logout view
def user_logout(request):
    logout(request)
    return redirect('login')

