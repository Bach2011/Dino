from asyncio.windows_events import NULL
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django import forms
from django.db import IntegrityError
from django.urls import reverse
from .models import TextAnswer, User, Question, Quiz, Answer, Response, Choices, RightAnswer
from django.contrib.auth.decorators import login_required
from django.core.validators import validate_email
# Create your views here.

@login_required
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
def play(request,id):
    if request.method == "POST":
        pass
    else:
        return render(request, "Dino/play.html", {
            "quiz":Quiz.objects.get(id=id),
            "questions":Question.objects.filter(quiz_id=id),
            "choices": Choices.objects.filter(question_id=id)
        })
def create_question(request, id):
    if request.method == "POST":
        name = request.POST.get('question')
        text = request.POST.get('text')
        if text != "" or text is not None:
            if TextAnswer.objects.all().exists():
                TextAnswer.objects.create(question_id=Question.objects.last().id + 1, answer=text)
            else:
                TextAnswer.objects.create(question_id=1, answer=text)
            RightAnswer.objects.create(answer=TextAnswer.objects.last(),quiz_id=id)
            Question.objects.create(title=name, right_answer_id=RightAnswer.objects.last().id, type="text", quiz_id=id)
        else :
            if RightAnswer.objects.all().exists() :
                Question.objects.create(title=name, id=id, right_answer_id=RightAnswer.objects.last().id, type="multiple choice", quiz_id=id)
            else:
                Question.objects.create(title=name, id=id, right_answer_id=1, type="multiple choice",quiz_id=id)
            option1 = request.POST.get('optionA')
            option2 = request.POST.get('optionB')
            option3 = request.POST.get('optionC')
            option4 = request.POST.get('optionD')
            right_choice = int(request.POST.get('correct'))
            Choices.objects.create(choice=option1, quiz_id=id)
            Choices.objects.create(choice=option2, quiz_id=id)
            Choices.objects.create(choice=option3, quiz_id=id)
            Choices.objects.create(choice=option4, quiz_id=id)
            right_choice = Choices.objects.get(quiz_id=id)[id-1]
            RightAnswer.objects.create(quiz_id=id, choice=right_choice)
            return redirect(reverse('edit_quiz', args=id))
        quiz = Quiz.objects.get(id=id)
        quiz.question.add(Question.objects.last())
        quiz.save()
        return redirect(reverse("edit_quiz", args=[id]))
    else:
        return render(request, "Dino/create_question.html", {
            "id":id
        })
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
def edit_quiz(request, id):
    try:
        return render(request, "Dino/edit_quiz.html", {
            'questions': Question.objects.filter(quiz_id=id),
            'quiz':Quiz.objects.get(id=id, owner=request.user)
        })
    except:
        return render(request, "Dino/error.html", {
            "error":"Quiz not found!"
        })
def my_quizzes(request):
    return render(request,"Dino/my_quizzes.html", {
        'quizzes': Quiz.objects.filter(owner=request.user)
    })
def edit_question(request,id, quiz_id):
    quiz = Quiz.objects.get(owner=request.user, id=quiz_id)
    question = Question.objects.get(quiz_id=quiz.id, id=id)
    choice = Choices.objects.filter(question_id=id)
    try:
        if question.type == "multiple choice":
            return render(request,"Dino/edit_question.html", {
                    "quiz":Quiz.objects.get(id=quiz_id),
                    "question":question,
                    "choices": choice
                })
        else:
            answer = TextAnswer.objects.get(question_id=id).answer
            return render(request,"Dino/edit_question.html", {
                    "quiz":Quiz.objects.get(id=quiz_id),
                    "question":question,
                    "answer": answer
            })
    except:
        return render(request,"Dino/error.html", {
            "error" : "Quiz/question not found"
        })
def quizzes(request):
    return render(request, "Dino/quizzes.html", {
        "quizzes":Quiz.objects.all()
    })