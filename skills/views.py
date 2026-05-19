from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Skill


@login_required(login_url='/login/')
def skill_list(request):
    skills = Skill.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'skills/list.html', {'skills': skills})


@login_required(login_url='/login/')
def add_skill(request):
    if request.method == 'POST':
        name = request.POST['name']
        category = request.POST['category']
        level = request.POST['level']

        Skill.objects.create(
            user=request.user,
            name=name,
            category=category,
            level=level
        )
        return redirect('skill_list')

    return render(request, 'skills/add_skill.html')


@login_required(login_url='/login/')
def edit_skill(request, id):
    skill = get_object_or_404(Skill, id=id, user=request.user)

    if request.method == 'POST':
        skill.name = request.POST['name']
        skill.category = request.POST['category']
        skill.level = request.POST['level']
        skill.save()
        return redirect('skill_list')

    return render(request, 'skills/edit_skill.html', {'skill': skill})


@login_required(login_url='/login/')
def delete_skill(request, id):
    skill = get_object_or_404(Skill, id=id, user=request.user)
    skill.delete()
    return redirect('skill_list')
