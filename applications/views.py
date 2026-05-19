from django.shortcuts import render, redirect, get_object_or_404
from .models import Application
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def edit_application(request, id):

    application = get_object_or_404(Application, id=id, user=request.user)

    if request.method == 'POST':

        application.company_name = request.POST['company_name']
        application.job_role = request.POST['job_role']
        application.status = request.POST['status']
        application.applied_date = request.POST['applied_date']
        application.save()

        return redirect('dashboard')

    return render(
        request,
        'applications/edit_application.html',
        {
            'application': application
        }
    )
@login_required(login_url='/login/')
def delete_application(request, id):

    application = get_object_or_404(Application, id=id, user=request.user)

    application.delete()

    return redirect('dashboard')


@login_required(login_url='/login/')
def add_application(request):

    if request.method == 'POST':

        company_name = request.POST['company_name']
        job_role = request.POST['job_role']
        status = request.POST['status']
        applied_date = request.POST['applied_date']

        Application.objects.create(
            user=request.user,
            company_name=company_name,
            job_role=job_role,
            status=status,
            applied_date=applied_date
        )

        return redirect('dashboard')

    return render(request, 'applications/add_application.html')