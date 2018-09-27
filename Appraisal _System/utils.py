from django.contrib.auth import get_user_model
from django.shortcuts import redirect, get_object_or_404
from system.forms import AppraisalForm, CompetenceForm
from system.models import Appraisal, Competence


User = get_user_model()


def get_forms_context(request, id):
    """
    :param id: if request is of create or update
    :param request.POST: if request is of get or post
    :return:
    """
    if id is None:
        if request.POST:
            appraisal_form = AppraisalForm(request.POST,
                                           instance=Appraisal(),
                                           manager=request.user)
            competence_form = CompetenceForm(request.POST,
                                             instance=Competence())
        else:
            appraisal_form = AppraisalForm(instance=Appraisal(),
                                           manager=request.user)
            competence_form = CompetenceForm(instance=Competence())
    else:
        appraisal = get_object_or_404(Appraisal, pk=id)
        if request.POST:
            appraisal_form = AppraisalForm(request.POST, instance=appraisal,
                                           manager=request.user)
            competence_form = CompetenceForm(
                request.POST, instance=appraisal.competence_set.all()[0])

        else:
            appraisal_form = AppraisalForm(instance=appraisal,
                                           manager=request.user)
            competence_form = CompetenceForm(
                instance=appraisal.competence_set.all()[0])
    context = {'appraisal_form': appraisal_form,
               'competence_form': competence_form}
    return context


def save_forms(appraisal_form, competence_form, id):
    """
    :param id: if request is of create or update
    :return:
    """
    new_appraisal = appraisal_form.save()
    if id is None:
        new_competence = competence_form.save(commit=False)
        new_competence.appraisal = new_appraisal
        new_competence.save()
    else:
        competence_form.save()


def redirect_to_home(request):
    if request.user.user_level == "employee":
        return redirect('view_appraisals', pk=request.user.id)
    elif request.user.user_level == "manager":
        return redirect('view_employees')
    elif request.user.user_level == "admin":
        return redirect("admin_home")
