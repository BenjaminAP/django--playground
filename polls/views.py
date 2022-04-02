from django.http import JsonResponse, HttpResponse
from django.core import serializers
from polls.serialiazers import PollSerializer
from django.views.decorators.csrf import csrf_exempt

from polls.models import Question, Choice
import json
# Create your views here.


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = [PollSerializer(q).data for q in latest_question_list]
    return JsonResponse(output, safe=False)


def choice_list(request, question_id):
    print(question_id)
    question = Question.objects.get(pk=question_id)
    output = serializers.serialize("json", question.choice_set.all())

    return HttpResponse(output)


def delete(request, question_id):
    q_to_delete = Question.objects.get(pk=question_id)
    print(q_to_delete)

    q_to_delete.delete()
    msg = '{msg: "deleted"}'

    output = serializers.serialize('json', msg)
    return HttpResponse(output)


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
