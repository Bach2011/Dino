from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.db import IntegrityError
from django.urls import reverse
from .models import User, Question, Quiz, Answer, Response, Choices
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
# Create your views here.

def index(request):
    return render(request, "Dino/index.html")
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "Dino/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "Dino/login.html")
def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "Dino/register.html", {
                "message": "Passwords must match."
            })
        # Ensure email is valid
        try:
            validate_email(email)
            valid_email = True
        except validate_email.ValidationError:
            valid_email = False
        if valid_email == False:
            return render(request, "Dino/register.html", {
                "message":"Email does not exist"
            })
        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "Dino/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "Dino/register.html")
@login_required
def play(request,id, question_id):
    if request.method == "POST":
        return HttpResponseRedirect(reverse("play", args=[id,question_id+1]))
    else:
        question = Question.objects.filter(quiz_id=id)[question_id-1]
        return render(request, "Dino/play.html", {
            "quiz":Quiz.objects.get(id=id),
            "question":question,
            "choices": Choices.objects.filter(question_id=question.id),
            "id":question_id
        })
def quiz(request, id):
    return render(request, "Dino/quiz.html", {
        "quiz": Quiz.objects.get(id=id),
    })
@login_required
def create_question(request, id):
    if request.method == "POST":
        name = request.POST.get('question')
        correct = int(request.POST.get('correct'))
        point = request.POST.get('point')
        choices = [request.POST.get('optionA'),request.POST.get('optionB'), request.POST.get('optionC'), request.POST.get('optionD')]
        for choice in choices:
            if str(choice) == str(choices[correct-1]):
                Choices.objects.create(question_id=Question.objects.last().id + 1, choice=choice, true=True)
            else:
                Choices.objects.create(question_id=Question.objects.last().id + 1, choice=choice)
        Question.objects.create(title=name, quiz_id=id, point=point)
        return HttpResponseRedirect(reverse('edit_quiz',args=[id]))
    else:
        return render(request, "Dino/create_question.html", {
            "id":id
        })
@login_required
def create_quiz(request):
    if request.method == "POST":
        name = request.POST.get('name')
        Quiz.objects.create(name=name, owner=request.user)
        if Quiz.objects.all().exists():
            return redirect(reverse('edit_quiz', args=[Quiz.objects.last().id]))
        else:
            return redirect(reverse("edit_quiz", args=1))
    else:
        return render(request,"Dino/create_quiz.html")
@login_required
def edit_quiz(request, id):
    try:
        if request.method == "POST":
            new_name = str(request.POST.get('name'))
            if new_name == "" or new_name == "None":
                question_id = request.POST.get('question_id')
                question = Question.objects.get(id=question_id)
                question.delete()
                return HttpResponseRedirect(reverse("edit_quiz", args=[id]))
            else:
                quiz = Quiz.objects.get(id=id)
                quiz.name = new_name
                quiz.save()
                return HttpResponseRedirect(reverse("edit_quiz", args=[id]))
        else:
            return render(request, "Dino/edit_quiz.html", {
            'questions': Question.objects.filter(quiz_id=id),
            'quiz':Quiz.objects.get(id=id, owner=request.user),
            })
    except:
        return render(request, "Dino/error.html", {
            "error":"Quiz not found!"
        })
@login_required
def my_quizzes(request):
    if request.method == "POST":
        quiz_id = request.POST.get('delete')
        quiz = Quiz.objects.get(pk=quiz_id)
        quiz.delete()
        return HttpResponseRedirect(reverse("my_quizzes"))
    else:
        return render(request,"Dino/my_quizzes.html", {
            'quizzes': Quiz.objects.filter(owner=request.user)
        })
@login_required
def edit_question(request,id, quiz_id):
    quiz = Quiz.objects.get(owner=request.user, id=quiz_id)
    question = Question.objects.get(quiz_id=quiz.id, id=id)
    choice = Choices.objects.filter(question_id=id)
    if request.method == "POST":
        point = request.POST.get('point')
        answer_id = request.POST.get('answer')
        answer = Choices.objects.filter(question_id=id)[answer_id-1]
        Answer.objects.create(choice_id=answer.id, )
        if Response.objects.filter(quiz_id=quiz_id).exists():
            response = Response.objects.get(quiz_id=quiz_id)
            response.point += point
            response.add(Answer.objects.last())
            response.save()

        else:
            Response.objects.create(user=request.user, quiz_id=quiz_id, point=point)
        return HttpResponseRedirect(reverse('edit_quiz', args=[quiz_id]))
    else:
        try:
            return render(request,"Dino/edit_question.html", {
                        "quiz":Quiz.objects.get(id=quiz_id),
                        "question":question,
                        "choices": choice
                    })
        except:
            return render(request,"Dino/error.html", {
                "error" : "Quiz/question not found"
            })
@login_required
def quizzes(request):
    return render(request, "Dino/quizzes.html", {
        "quizzes":Quiz.objects.all()
    })