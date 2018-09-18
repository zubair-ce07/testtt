
from datetime import timezone

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, get_user_model, logout, update_session_auth_hash
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import UpdateView, DeleteView, CreateView
from system.forms import SignUpForm, ExtendedAppraisalForm
from system.models import Appraisal


User = get_user_model()


#-----------------------------------------create appraisal View
class AppraisalCreateView(LoginRequiredMixin, CreateView):
    template_name = "form.html"
    model = Appraisal
    form_class = ExtendedAppraisalForm

    def get_initial(self):
        initial = super(AppraisalCreateView, self).get_initial()
        initial['from_user'] = self.request.user
        return initial

    def form_valid(self, form):
        obj = super(AppraisalCreateView, self).form_valid(form)
        clean = form.cleaned_data
        self.object.competence_set.create(
            decision_making=clean['decision_making'],
            confidence=clean['confidence'],
            problem_solving=clean['problem_solving'],
        )
        return obj

    def get_success_url(self):
        return reverse_lazy('manager_home')

    def get_form_kwargs(self):
        kwargs = super(AppraisalCreateView, self).get_form_kwargs()
        kwargs['manager'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AppraisalCreateView, self).get_context_data(**kwargs)
        context['context'] = "Create Appraisal"
        return context

#-----------------------------------------Delete appraisal
class AppraisalDeleteView(LoginRequiredMixin, DeleteView):
    model = Appraisal
    template_name = 'system/appraisal-confirm-delete.html'
    to_user=None

    def get_success_url(self):
        return reverse_lazy('view_employee', kwargs={'pk': self.to_user.pk})

    def get_object(self, queryset=None):
        obj = super(AppraisalDeleteView, self).get_object()
        self.to_user = obj.to_user
        return obj


#----------------------------------------update appraisal

class AppraisalUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "form.html"
    model = Appraisal
    form_class = ExtendedAppraisalForm

    def get_initial(self):
        initial = super(AppraisalUpdateView, self).get_initial()
        try:
            comp = self.object.competence_set.all()[0]
        except:
            pass
        else:
            initial['decision_making'] = comp.decision_making
            initial['confidence'] = comp.confidence
            initial['problem_solving'] = comp.problem_solving
        return initial

    def form_valid(self, form):
        clean = form.cleaned_data
        competence = self.object.competence_set.all()[0]
        competence.decision_making=clean['decision_making']
        competence.confidence=clean['confidence']
        competence.problem_solving=clean['problem_solving']
        competence.save()
        return super(AppraisalUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('view_employee', kwargs={'pk': self.object.to_user.pk})

    def get_form_kwargs(self):
        kwargs = super(AppraisalUpdateView, self).get_form_kwargs()
        kwargs['manager'] = self.request.user
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(AppraisalUpdateView, self).get_context_data(**kwargs)
        context['context'] = "Updat Appraisal"
        return context


#-----------------------------------------------List views

class ManagerIndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'system/index.html'
    model = User
    context_object_name = 'all_employees'

    def get_queryset(self):
        qs = super().get_queryset()
        employees_list = qs.filter(
            report_to=self.request.user.id)
        return employees_list

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['user_pk'] =  self.request.user.id
        return data

class EmployeeIndexView(LoginRequiredMixin, generic.ListView):
    model = Appraisal
    context_object_name = 'all_apparaisal'
    template_name = "system/view-appraisals.html"
    pk = None

    def get_queryset(self):

        # will overide in case of employee : no pk (argument)
        if self.pk is None:
            self.pk = self.request.user.id

        qs = super().get_queryset()
        all_apparaisal = qs.filter(to_user=self.pk)
        return all_apparaisal

    def get(self, *args, **kwargs):
        self.pk = kwargs.get('pk', None)
        #run in case of manager : pk
        resp = super().get(*args, **kwargs)
        return resp

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['context'] =  self.request.user.user_level
        return data
    ## in case of employee filter need to be applied on request.user.id
    ## and in case of manager filter need to be applied on id from arguments


#------------------------------------------------------Login-signup-settings

@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'form.html', {
        'form': form,
        'context': "Save"
    })

def signupUser(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Succesfully registered, Wait for admin approval.')
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'form.html', {'form': form, 'context':"Sign Up"})

def loginUser(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect(get_home_page(user.user_level))
    else:
        form = AuthenticationForm()
    return render(request,'form.html',{'form':form, 'context':"Log In"})


@login_required
def logoutUser(request):
    logout(request)
    return redirect('home')


#------------------------------------------------------Helper Functions

def get_home_page(user_level):
    return user_level + "_home"

def index(request):
    if request.user.is_authenticated:
        return redirect(get_home_page(request.user.user_level))
    else:
        return render(request, 'form.html')
