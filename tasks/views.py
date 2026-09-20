from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Task


@login_required
def task_list(request):
    tasks = Task.objects.filter(user=request.user).order_by("-created_at")

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if title:
            Task.objects.create(
                user=request.user,
                title=title,
                description=description,
            )

        return redirect("task_list")

    return render(
        request,
        "tasks/task_list.html",
        {"tasks": tasks},
    )


@login_required
def toggle_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user,
    )

    if request.method == "POST":
        task.completed = not task.completed
        task.save()

    return redirect("task_list")


@login_required
def delete_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user,
    )

    if request.method == "POST":
        task.delete()

    return redirect("task_list")

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(
        Task,
        id=task_id,
        user=request.user,
    )

    if request.method == "POST":
        title = request.POST.get("title", "").strip()
        description = request.POST.get("description", "").strip()

        if title:
            task.title = title
            task.description = description
            task.save()

        return redirect("task_list")

    return render(
        request,
        "tasks/edit_task.html",
        {"task": task},
    )