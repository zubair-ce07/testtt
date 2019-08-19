from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_control
import random
from QuizApp.forms import QuizForm, QuestionForm, CustomUserCreationForm
from QuizApp.models import *


def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if not form.cleaned_data.get('is_teacher', False) and not form.cleaned_data.get('is_student', False):
                messages.error(request, 'Invalid input! Please specify one of the following (Teacher, Student)')
                return render(request, 'signup.html', {'form': form})
            user = form.save()
            username = user.username
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password, backend='django.contrib.auth.backends.ModelBackend')
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('accounts/login/')


@login_required
def home(request):
    if request.user.is_student:
        return redirect('student_home')
    quiz_list = Quiz.objects.filter(owner=request.user)
    return render(request, 'home.html', {'quizzes': quiz_list})



@login_required
def add_quiz(request):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.owner = request.user
            quiz.save()
        return redirect('add_question', quiz.pk)
    else:
        form = QuizForm()
    return render(request, 'add_quiz.html', {'form': form})


@login_required
def quiz_details(request, quiz_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    quiz = Quiz.objects.get(pk=quiz_pk)
    return render(request, 'quiz_details.html', {'quiz': quiz, 'questions': quiz.questions.all()})


@login_required
def add_question(request, quiz_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz_id = quiz_pk
            question.save()
            return redirect('add_options', question.pk)
    else:
        form = QuestionForm()
    return render(request, 'add_question.html', {'form': form, 'quiz': get_object_or_404(Quiz, pk=quiz_pk)})


@login_required
def add_options(request, question_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    if request.method == 'POST':
        option1 = {'text': request.POST.get('A'), 'is_correct': True if request.POST.get('Correct') == 'A' else False,
                   'question_id': question_pk}
        option2 = {'text': request.POST.get('B'), 'is_correct': True if request.POST.get('Correct') == 'B' else False,
                   'question_id': question_pk}
        option3 = {'text': request.POST.get('C'), 'is_correct': True if request.POST.get('Correct') == 'C' else False,
                   'question_id': question_pk}
        option4 = {'text': request.POST.get('D'), 'is_correct': True if request.POST.get('Correct') == 'D' else False,
                   'question_id': question_pk}
        Option.objects.create(**option1)
        Option.objects.create(**option2)
        Option.objects.create(**option3)
        Option.objects.create(**option4)
        return redirect('quiz_details', Question.objects.get(pk=question_pk).quiz.id)
    else:
        return render(request, 'add_options.html', {'question': Question.objects.get(pk=question_pk)})


@login_required
def question_detail(request, question_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    question = get_object_or_404(Question, pk=question_pk)
    return render(request, 'question_detail.html', {'question': question, 'answers':  question.answers.all()})


@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def take_quiz(request, quiz_pk):
    if not request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    if Result.objects.filter(taken_by=request.user, quiz_id=quiz_pk).exists():
        return HttpResponseBadRequest(content='Already Taken, Cannot Retake')
    quiz_questions = [question for question in get_object_or_404(Quiz, pk=quiz_pk).questions.all() if
                      question.answers.all().count() == 4 and question.answers.filter(is_correct=True).count() == 1]
    if request.method == 'POST':
        submitted_ans = Option.objects.filter(pk__in=[request.POST.get(str(quiz.pk)) for quiz in quiz_questions])
        score = Option.objects.filter(id__in=[ans.id for ans in submitted_ans]).filter(is_correct=True).count()
        correct_ans = [question.answers.get(is_correct=True) for question in quiz_questions]
        quiz_solution = zip(quiz_questions, correct_ans, submitted_ans)
        Result.objects.create(taken_by=request.user, quiz_id=quiz_pk, score=score)
        for question, answer in zip(quiz_questions, submitted_ans):
            AnswerOption.objects.create(student=request.user, question=question, answer=answer)
        return render(request, 'result.html', {'quiz_sol': quiz_solution, 'score': score, 'total': len(quiz_questions)})
    random.shuffle(quiz_questions, random.random)
    return render(request, 'take_quiz.html', {'questions': enumerate(quiz_questions, start=1)})


@login_required
def edit_question(request, question_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    form = QuestionForm(request.POST or None, instance=Question.objects.get(pk=question_pk))

    if form.is_valid():
        form.save()
        return redirect('question_detail', get_object_or_404(Question, pk=question_pk).quiz_id, question_pk)
    return render(request, 'edit_question.html', {'form': form})


@login_required
def edit_options(request, question_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    answers = Question.objects.get(pk=question_pk).answers.all()
    if request.method == 'POST':
        for answer in answers:
            answer.text = request.POST.get(str(answer.pk))
            answer.is_correct = True if int(request.POST.get('correct')) == answer.pk else False
            answer.save()
        return redirect('question_detail', Question.objects.get(pk=question_pk).quiz_id, question_pk)
    if answers.count() == 0:
        return redirect('question_detail', get_object_or_404(Question,pk=question_pk).quiz_id, question_pk)
    return render(request, 'edit_options.html', {'answers': answers})


@login_required
def delete_question(request, question_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    question = get_object_or_404(Question, pk=question_pk)
    quiz_id = question.quiz_id
    question.delete()
    return redirect('quiz_details', quiz_id)


@login_required
def delete_quiz(request, quiz_pk):
    if request.user.is_student:
        return HttpResponseBadRequest(content='Not Authorized')
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    quiz.delete()
    return redirect('home')

@login_required
def quiz_result(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk).taken_quizzes.all()
    return render(request, 'quiz_result.html', {'quizzes': quiz})


@login_required
def student_home(request):
    if request.user.is_teacher:
        return HttpResponseBadRequest(content='Not Authorized')
    student = request.user
    quiz_list = Quiz.objects.exclude(
        id__in=[quiz.quiz_id for quiz in Result.objects.filter(taken_by=student)]).all().exclude(
        questions__isnull=True).exclude(id__in=[question.quiz_id for question in Question.objects.all() if question.answers.all().count() < 4])
    return render(request, 'student_home.html', {'quizzes': quiz_list})


@login_required
def result_view(request):
    if not request.user.is_student:
        return HttpResponseBadRequest(content='Not authorized')
    results = Result.objects.all().filter(student=request.user)
    return render(request, 'result_view.html', {'results': results})


def result_details(request, quiz_pk, student_pk):
    result = AnswerOption.objects.filter(student_id=student_pk, question__in=get_object_or_404(Quiz, pk=quiz_pk).questions.all())
    return render(request, 'result_details.html', {'result': result})
