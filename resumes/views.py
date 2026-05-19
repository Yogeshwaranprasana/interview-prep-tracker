from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Resume


@login_required(login_url='/login/')
def resume_list(request):
    resumes = Resume.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'resumes/list.html', {'resumes': resumes})


@login_required(login_url='/login/')
def add_resume(request):
    if request.method == 'POST':
        title = request.POST['title']
        summary = request.POST.get('summary', '')
        resume_file = request.FILES.get('resume_file')

        Resume.objects.create(
            user=request.user,
            title=title,
            summary=summary,
            resume_file=resume_file
        )
        return redirect('resume_list')

    return render(request, 'resumes/add_resume.html')


@login_required(login_url='/login/')
def edit_resume(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    if request.method == 'POST':
        resume.title = request.POST['title']
        resume.summary = request.POST.get('summary', '')
        new_file = request.FILES.get('resume_file')
        if new_file:
            resume.resume_file = new_file
        resume.save()
        return redirect('resume_list')

    return render(request, 'resumes/edit_resume.html', {'resume': resume})


@login_required(login_url='/login/')
def delete_resume(request, id):
    resume = get_object_or_404(Resume, id=id, user=request.user)
    resume.delete()
    return redirect('resume_list')
