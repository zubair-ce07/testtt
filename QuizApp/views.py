from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from http.client import HTTPResponse
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.template.context_processors import request

from .forms import *
from .models import *


def signup(request):
    if request.method == 'POST':
        # print(request.POST)
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            if form.cleaned_data.get('is_teacher', False) and form.cleaned_data.get('is_student', False):
                messages.error(request, 'You Can be Either a Student or Teacher, Not both!.')
                return render(request, 'signup.html', {'form': form})
            user=form.save(commit=False)
            user.username=user.email
            user.save()
            username = user.email
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password, backend='django.contrib.auth.backends.ModelBackend')
            login(request, user)
            return redirect('student_home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

# Create your views here.
def logout_view(request):
    logout(request)
    return redirect('accounts/login/')

@login_required
def home(request):
    if request.user.is_student:
         return redirect('student_home')
    quiz_list = Quiz.objects.all()
    return render(request, 'home.html',{'quizzes': quiz_list})

@login_required
def add_quiz(request):
    if request.method == 'POST':
        form = QuizForm(request.POST)
        if form.is_valid():
            quiz = form.save(commit=False)
            quiz.owner_id = 1
            quiz.save()
        return redirect('quiz_list')
    else:
        form = QuizForm()
    return render(request, 'add_quiz.html', {'form': form})
@login_required
def quiz_details(request, quiz_pk):
    quiz = Quiz.objects.get(pk=quiz_pk)
    # print(quiz_questions)
    return render(request, 'quiz_details.html', {'quiz': quiz, 'questions': quiz.questions.all()})
    
@login_required
def add_question(request, quiz_pk):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz_id = quiz_pk
            question.save()
            return redirect('add_options',question.pk)
    else:
        form = QuestionForm()
    return render(request, 'add_question.html', {'form': form})

@login_required
def add_options(request, question_pk):
    if request.method == 'POST':
        option1 = {'text': request.POST.get('A'), 'is_correct': True if request.POST.get('Correct') == 'A' else False,'question_id': question_pk}
        option2 = {'text': request.POST.get('B'), 'is_correct': True if request.POST.get('Correct') == 'B' else False,'question_id': question_pk}
        option3 = {'text': request.POST.get('C'), 'is_correct': True if request.POST.get('Correct') == 'C' else False,'question_id': question_pk}
        option4 = {'text': request.POST.get('D'), 'is_correct': True if request.POST.get('Correct') == 'D' else False,'question_id': question_pk}
        Answer.objects.create(**option1)
        Answer.objects.create(**option2)
        Answer.objects.create(**option3)
        Answer.objects.create(**option4)
        return redirect('quiz_details', Question.objects.get(pk=question_pk).quiz.id)
    else:
        return render(request,'add_options.html',{'question': Question.objects.get(pk=question_pk)})

def question_detail(request, quiz_pk, question_pk):
    question = get_object_or_404(Question, pk=question_pk, quiz_id=quiz_pk)
    return render(request, 'question_detail.html', {'question': question, 'answers':  question.answers.all()})

@login_required
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def take_quiz(request, quiz_pk):
    if TakenQuiz.objects.filter(student_id=request.user.id, quiz_id=quiz_pk).exists():
        return HttpResponseBadRequest(content='Already Taken, Cannot Retake')
    quiz_questions = [question for question in get_object_or_404(Quiz,pk=quiz_pk).questions.all() if question.answers.all().count() >= 2 and question.answers.filter(is_correct=True).count() == 1]
    if request.method == 'POST':
        submitted_ans = Answer.objects.filter(pk__in = [request.POST.get(str(quiz.pk)) for quiz in quiz_questions])
        score = Answer.objects.filter(id__in=[ans.id for ans in submitted_ans]).filter(is_correct=True).count()
        correct_ans = [question.answers.get(is_correct=True) for question in quiz_questions]
        quiz_solution = zip(quiz_questions, correct_ans, submitted_ans)
        TakenQuiz.objects.create(student_id=request.user.id, quiz_id=quiz_pk, score=score)
        for q, a in zip(quiz_questions, submitted_ans):
            SelectedOption.objects.create(student_id=request.user.id, question_id=q.pk,Answer_id=a.id, quiz_id=quiz_pk)
        return render(request,'result.html', {'quiz_sol': quiz_solution, 'score': score})
    return render(request, 'take_quiz.html', {'questions': zip(quiz_questions, range(1, len(quiz_questions) + 1))})


@login_required
def edit_question(request, question_pk):
    form = QuestionForm(request.POST or None, instance=Question.objects.get(pk=question_pk))

    if form.is_valid():
        form.save()
        return redirect('question_detail', get_object_or_404(Question, pk=question_pk).quiz_id, question_pk)
    return render(request, 'edit_question.html', {'form': form})

@login_required
def edit_options(request, question_pk):
    answers = Question.objects.get(pk=question_pk).answers.all()
    if request.method == 'POST':
        print(request.POST)
        for answer in answers:
            answer.text = request.POST.get(str(answer.pk))
            answer.is_correct = True if int(request.POST.get('correct')) == answer.pk else False
            answer.save()
        return redirect('question_detail', Question.objects.get(pk=question_pk).quiz_id, question_pk)

    return render(request, 'edit_options.html', {'answers': answers})
def delete_question(request, question_pk):
    question = get_object_or_404(Question, pk=question_pk)
    quiz_id = question.quiz_id
    question.delete()
    return redirect('quiz_details', quiz_id)

def delete_quiz(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk)
    quiz.delete()
    return redirect('quiz_list')

@login_required
def quiz_result(request, quiz_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk).taken_quizzes.all()


    return render(request, 'quiz_result.html', {'quizzes': quiz})

def student_home(request):
    student = request.user
    quiz_list = Quiz.objects.exclude(id__in=[quiz.quiz_id for quiz in TakenQuiz.objects.filter(student=student).all()]).all()
    return render(request, 'student_home.html',{'quizzes': quiz_list})

@login_required
def result_view(request):
    if not request.user.is_student:
        return HttpResponseBadRequest(content='Not authorized')
    student = request.user
    results = TakenQuiz.objects.all().filter(student=request.user)
    return render(request, 'result_view.html', {'results': results})