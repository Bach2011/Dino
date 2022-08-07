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
def play(request,id, question_order):
    if request.method == "POST":
        try:
            # getting the resources
            answer = int(request.POST.get('answer'))
            question_id = Question.objects.filter(quiz_id=id)[question_order-1].id
            answer = Choices.objects.filter(question_id=question_id)[answer-1]
            point = int(request.POST.get('point'))
            if answer.true == True:
                Answer.objects.create(choices_id=answer.id, quiz=Quiz.objects.get(pk=id), true=True, response_id=Response.objects.last().id+1)
            else:
                Answer.objects.create(choices_id=answer.id, quiz=Quiz.objects.get(pk=id), true=False)
            if question_order != 1:
                response = Response.objects.get(quiz_id=id,user=request.user)
                response.point += point
                response.answer.add(Answer.objects.last())
                response.save()
            else:
                response = Response.objects.create(quiz_id=id, point=point, user=request.user)
                response.answer.add(Answer.objects.last())
            if Question.objects.filter(quiz_id=id).last() == Question.objects.get(pk=question_id):
                return HttpResponseRedirect(reverse("result", args=[id]))
            else:
                return HttpResponseRedirect(reverse("play", args=[id,question_order+1]))
        except Exception as e:
            return render(request, "Dino/error.html", {
                "error": e
            })
    else:
        try:
            question = Question.objects.filter(quiz_id=id)[question_order-1]
            return render(request, "Dino/play.html", {
                "quiz":Quiz.objects.get(id=id),
                "question":question,
                "choices": Choices.objects.filter(question_id=question.id),
                "id":question_order
            })
        except Exception as e:
            return render(request, "Dino/error.html", {
                "error": e
            })
def quiz(request, id):
    try:
        response = Response.objects.get(quiz_id=id, user=request.user)
        return render(request, "Dino/quiz.html", {
            "quiz": Quiz.objects.get(id=id),
            "response":response,
        })
    except Response.DoesNotExist:
        return render(request, "Dino/quiz.html", {
            "quiz": Quiz.objects.get(id=id)
        })
    except Exception as e:
        return render(request, "Dino/error.html", {
            "error": e
        })
@login_required
def create_question(request, id):
    try:
        if request.method == "POST":
            name = request.POST.get('question')
            correct = int(request.POST.get('correct'))
            point = request.POST.get('point')
            choices = []
            # getting the choices
            for i in range(4):
                choices.append(request.POST.get(f"option{i+1}"))
            print(choices)
            # creating choice objects
            for choice in choices:
                if choice == choices[correct-1]:
                    try:
                        Choices.objects.create(question_id=Question.objects.last().id + 1, choice=choice, true=True)
                    except:
                        Choices.objects.create(question_id=1, choice=choice, true=True)
                else:
                    try:
                        Choices.objects.create(question_id=Question.objects.last().id + 1, choice=choice)
                    except:
                        Choices.objects.create(question_id=1, choice=choice)
            # create question
            Question.objects.create(title=name, quiz_id=id, point=point)
            quiz = Quiz.objects.get(pk=id)
            quiz.question.add(Question.objects.last())
            quiz.max_point = quiz.max_point + Question.objects.last().point
            quiz.save()
            return HttpResponseRedirect(reverse('edit_quiz',args=[id]))
        else:
            return render(request, "Dino/create_question.html", {
                "id":id,
                "a": range(1,5)
            })
    except Exception as e:
        return render(request, "Dino/error.html", {
            "error": e
        })
@login_required
def create_quiz(request):
    try:
        if request.method == "POST":
            name = request.POST.get('name')
            Quiz.objects.create(name=name, owner=request.user)
            if Quiz.objects.all().exists():
                return redirect(reverse('edit_quiz', args=[Quiz.objects.last().id]))
            else:
                return redirect(reverse("edit_quiz", args=1))
        else:
            return render(request,"Dino/create_quiz.html")
    except Exception as e:
        return render(request, "Dino/error.html", {
            "error": e
        })
@login_required
def edit_quiz(request, id):
    try:
        if request.method == "POST":
            new_name = str(request.POST.get('name'))
            if new_name == "" or new_name == "None":
                question_id = request.POST.get('question_id')
                question = Question.objects.get(id=question_id)
                quiz = Quiz.objects.get(id=id)
                quiz.max_point -= question.point
                quiz.save()
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
    except Exception as e:
        return render(request, "Dino/error.html", {
            "error":e
        })
@login_required
def my_quizzes(request):
    try:
        if request.method == "POST":
            quiz_id = request.POST.get('delete')
            quiz = Quiz.objects.get(pk=quiz_id)
            quiz.delete()
            return HttpResponseRedirect(reverse("my_quizzes"))
        else:
            return render(request,"Dino/my_quizzes.html", {
                'quizzes': Quiz.objects.filter(owner=request.user)
            })
    except Exception as e:
        return render(request, "Dino/error.html", {
            "error": e
        })
@login_required
def edit_question(request,id, quiz_id):
    try: 
        quiz = Quiz.objects.get(owner=request.user, id=quiz_id)
        question = Question.objects.get(quiz_id=quiz.id, id=id)
        choice = Choices.objects.filter(question_id=id)
        if request.method == "POST":
            point = request.POST.get('point')
            choices = []
            for i in range(4):
                choices.append(request.POST.get(f"option{i+1}"))
            title = request.POST.get("question")
            question.title = title
            question.point = point
            question.save()
            for i,new_choice in enumerate(choices):
                choice = Choices.objects.filter(question_id=id)[i]
                if choice == Choices.objects.filter(question_id=id)[int(request.POST.get('correct'))]:
                    choice.true = True
                    choice.choice = new_choice
                    choice.save()
                else:
                    choice.true = False
                    choice.choice = new_choice
                    choice.save()
            return HttpResponseRedirect(reverse("edit_quiz",args=[quiz_id]))
        else:
            return render(request,"Dino/edit_question.html", {
                            "quiz":Quiz.objects.get(id=quiz_id),
                            "question":question,
                            "choices": choice
                        })
    except Exception as e:
        return render(request, "Dino/error.html", {
            "error":e
        })
@login_required
def quizzes(request):
    try:
        quizzes = []
        for quiz in Quiz.objects.all():
            if Question.objects.filter(quiz_id=quiz.id).count() != 0:
                quizzes.append(quiz)
        return render(request, "Dino/quizzes.html", {
            "quizzes":quizzes
        })
    except Exception as e:
        return render(request, "Dino/error.html", {
            "error": e
        })
def result(request,id):
    try:
        response = Response.objects.get(user=request.user, quiz_id=id)
        return render(request, "Dino/result.html", {
            "quiz": Quiz.objects.get(pk=id),
            "response": response,
            "max_point": Quiz.objects.get(id=id).max_point,
        })
    except Exception as e:
        return render(request, "Dino/error.html", {
            "error": e
        })