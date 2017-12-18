from django import views
from django.db.models import Q, Count
from django.db.models.functions import TruncMonth
from django.forms import modelform_factory
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.decorators import method_decorator
from malfunction_reporting.forms import SafetyHazardForm, Task, SafetyHazard
from malfunction_reporting.decorators import assignee_or_owner_required
from malfunction_reporting.models import Movie, Investigation


class Index(views.View):
    """
    View class responsible for letting user create new safety hazard report
    """
    template = 'malfunction_reporting/index.html'

    def post(self, request):
        form = SafetyHazardForm(data=request.POST)

        if form.is_valid():
            report = form.save(request=request)
            response = redirect('malfunction_reporting:task_detail', report.id)
        else:
            response = render(request, self.template, {'form': form})

        return response

    def get(self, request):
        return render(request, self.template, {'form': SafetyHazardForm()})


def list_tasks(request):
    """
    List all task which were reported by or assigned to user

    Arguments:
        request (Request): request initiated by user

    Returns:
        response (Response): web page listing all the tasks related to user
    """
    tasks = Task.objects.filter(Q(assignee=request.user) | Q(safetyhazard__reported_by=request.user))
    return render(request, 'malfunction_reporting/list_tasks.html', {'tasks': tasks})


@method_decorator(assignee_or_owner_required, name='dispatch')
class TaskDetail(views.View):
    """
    Displays details of task and on post save the status of task
    """
    TaskForm = modelform_factory(Task, fields=('status',))
    template = 'malfunction_reporting/task_detail.html'

    def post(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        investigations = task.safetyhazard.investigations.all()
        form = self.TaskForm(instance=task, data=request.POST)

        if form.is_valid():
            # if status is changed to completed then save current time in completed_at
            task.completed_at = timezone.now() if form.cleaned_data['status'] == Task.COMPLETED else None
            form.save()
            response = render(request, self.template, {'form': form, 'task': task, 'investigations': investigations})
        else:
            response = render(request, self.template, {
                'form': form,
                'task': task,
                'error': 'Invalid data.',
                'investigations': investigations
            })
        return response

    def get(self, request, pk):
        task = get_object_or_404(Task, pk=pk)
        investigations = task.safetyhazard.investigations.all()
        form = self.TaskForm(instance=task)
        return render(request, self.template, {'form': form, 'task': task, 'investigations': investigations})


def dashboard(request):
    """
    Displays number of safety hazard reported this year by user
    on every month basis and also lists pending, started and completed
    task count for every month. This is to learn django ORM usage
    """
    year = timezone.now().year
    reports = SafetyHazard.objects.filter(reported_at__year=year, reported_by=request.user).values(
        month=TruncMonth('reported_at')
    ).annotate(count=Count('month')).order_by('month')

    # lists months of current year and count of tasks with different statuses for every month
    status_reports = SafetyHazard.objects.filter(reported_at__year=year, reported_by=request.user).values(
        'task__status', month=TruncMonth('reported_at')
    ).annotate(count=Count('task__status')).order_by('month')

    return render(request, 'malfunction_reporting/dashboard.html', {'reports': reports, 'statuses': status_reports})


def show_movies(request):
    """
    this view is to learn what django provides to optimize db access.
    by using prefetch related method this view lists all movies and users
    that own those movies.
    """
    movies = Movie.objects.all().prefetch_related('owners')
    return render(request, 'malfunction_reporting/movies.html', {'movies': movies})


def show_all_investigations(request):
    """
    Lists all investigations happened on users generated reports.
    """
    return render(
        request,
        'malfunction_reporting/investigations.html',
        {
            'safe_investigations': Investigation.objects.filter(report__reported_by=request.user),
            'hazard_investigations': Investigation.objects.filter(hazard__reported_by=request.user),
        }
    )
