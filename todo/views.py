from django.views import View, generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count

from rest_framework import viewsets
from rest_framework.decorators import api_view


from .models import TodoItem
from .serializers import TodoItemSerializer, UserSerializer
from .forms import TodoItemModelUpdateForm


class TodoViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows TodoItems to be edited or viewed
    """
    queryset = TodoItem.objects.all()
    serializer_class = TodoItemSerializer


@api_view(['POST'])
def create_alone_user(request):
    '''
    Post view to create a single user without corresponding
    todoitems
    '''
    print(request.data['username'])
    user = User(username=request.data['username'])
    user.save()
    return UserSerializer(user)

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Users
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


class TodoView(LoginRequiredMixin, generic.ListView):
    """
    Main page after login, lists all the TodoItems for 
    the logged in user 
    """
    template_name = 'todo/index.html'
    context_object_name = 'todo_items'

    def get_queryset(self):
        if (self.request.user.has_perm('todo.is_manager')):
            return TodoItem.objects.order_by('status')
        else:
            return TodoItem.objects.filter(user=self.request.user).filter(
                status__in=['pending', 'inprogress']).order_by('status')


class TodoCreateView(LoginRequiredMixin, generic.CreateView):
    """
    Generic view to create a single TodoItem for 
    the logged in user
    """
    model = TodoItem
    success_url = '/todo/'
    fields = ['description', 'user']


class TodoDetailView(LoginRequiredMixin, generic.DetailView):
    """
    Displays the detail of a single item in todo list for
    a specific user
    """
    model = TodoItem
    template_name = 'todo/detail.html'
    context_object_name = 'item'

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch method to handle user and manager
        permissions
        """
        item = get_object_or_404(TodoItem.objects.all(), pk=kwargs['pk'])
        if request.user.has_perm('todo.is_manager'):
            return super().dispatch(request)
        elif item.user.id != request.user.id:
            return redirect('todo:index')
        else:
            return super().dispatch(request)


class TodoDeleteView(LoginRequiredMixin, generic.DeleteView):
    """
    View to delete TodoItem for specific user
    """
    model = TodoItem
    template_name = 'todo/delete.html'
    success_url = '/todo'

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispath method to include manager permissions and
        and user access permissions
        """
        item = get_object_or_404(TodoItem.objects.all(), pk=kwargs['pk'])

        if request.user.has_perm('todo.is_manager'):
            return super().dispatch(request)
        elif item.user.id != request.user.id:
            return redirect('todo:index')
        else:
            return super().dispatch(request)


class TodoUpdateView(LoginRequiredMixin, generic.UpdateView):
    """
    View that updates the TodoItem for a specific user
    """
    model = TodoItem
    form_class = TodoItemModelUpdateForm
    template_name = 'todo/update.html'
    success_url = '/todo/'

    def get(self, request, *args, **kwargs):
        """
        Override get method to handle manager and
        user permissions
        """
        item = get_object_or_404(TodoItem.objects.all(), pk=kwargs['pk'])
        form = TodoItemModelUpdateForm(instance=item)
        if request.user.has_perm('todo.is_manager'):
            return render(request, 'todo/update.html', {'form': form})
        elif item.user.id == request.user.id:
            return render(request, 'todo/update.html', {'form': form})
        else:
            return redirect('todo:index')


class SummaryView(PermissionRequiredMixin, View):
    permission_required = 'todo.is_manager'
    template_name = 'todo/summary.html'

    def get(self, request):
        context = {}

        context['all_time'] = User.objects.filter(todoitem__status='complete').annotate(
            Count('todoitem')).order_by('-todoitem__count')[:3]

        current_month = timezone.make_aware(datetime.now())
        one_month_ago = current_month - timedelta(days=30)
        context['complete_last_month'] = User.objects.filter(
            todoitem__status='complete',
            todoitem__date_completed__gte=one_month_ago).annotate(
                Count('todoitem')).order_by('-todoitem__count')[:3]

        three_months_ago = current_month - timedelta(days=90)
        context['complete_last_month_with_3_months'] = User.objects.filter(
            todoitem__status='complete',
            date_joined__gte=three_months_ago,
            todoitem__date_completed__gte=one_month_ago).annotate(
                Count('todoitem')).order_by('-todoitem__count')[:3]

        two_months_ago = current_month - timedelta(days=60)
        context['inprogress_since_last_2_months'] = User.objects.filter(
            todoitem__date_created__gte=two_months_ago,
            todoitem__status='inprogress').annotate(
                Count('todoitem')).order_by('-todoitem__count')[:3]

        return render(request, self.template_name, context)
