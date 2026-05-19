from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Note


@login_required(login_url='/login/')
def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-updated_at')
    return render(request, 'notes/list.html', {'notes': notes})


@login_required(login_url='/login/')
def add_note(request):
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']

        Note.objects.create(
            user=request.user,
            title=title,
            body=body
        )
        return redirect('note_list')

    return render(request, 'notes/add_note.html')


@login_required(login_url='/login/')
def edit_note(request, id):
    note = get_object_or_404(Note, id=id, user=request.user)
    if request.method == 'POST':
        note.title = request.POST['title']
        note.body = request.POST['body']
        note.save()
        return redirect('note_list')

    return render(request, 'notes/edit_note.html', {'note': note})


@login_required(login_url='/login/')
def delete_note(request, id):
    note = get_object_or_404(Note, id=id, user=request.user)
    note.delete()
    return redirect('note_list')
