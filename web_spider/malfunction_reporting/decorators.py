from django.shortcuts import get_object_or_404, redirect
from malfunction_reporting.models import Task


def assignee_or_owner_required(original):
    """
    Decorator to limit access to only those user that are either assigned
    task or user is the one who reported the safety hazard

    Arguments:
        original (callable): function to which limit access to

    Returns:
        wrapper (callable): wrapped original function but with limiting access
    """
    def wrapper(request, pk):
        task = get_object_or_404(Task, pk=pk)

        if (task.assignee == request.user) or (task.safetyhazard.reported_by == request.user):
            response = original(request, pk)
        else:
            response = redirect('malfunction_reporting:index')
        return response
    return wrapper
