from django.shortcuts import render
from django.http import HttpResponse
from django.core import serializers

from polls.models import Question, Choice
import json
# Create your views here.


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)


def results(request, question_id):
    response = "You're looking at results of question %s."
    return HttpResponse(response % question_id)


def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)


def all_questions(request):
    response = serializers.serialize("json", Question.objects.all())
    return HttpResponse(response)


def question_by_id(request, question_id):
    response = [
        Question.objects.get(pk=question_id).question_txt,
        serializers.serialize("json", Question.objects.get(pk=question_id).choice_set.all())
    ]

    return HttpResponse(response)


def question_choices(request, question_id):
    response = Question.objects.get(pk=question_id).choice_set.all()
    return HttpResponse(response)
