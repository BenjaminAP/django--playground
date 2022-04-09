
from django.http import JsonResponse, HttpResponse
from django.utils import timezone
from rest_framework import serializers

from polls.serialiazers import QuestionSerializer, ChoiceSerializer
from django.views.decorators.csrf import csrf_exempt

from polls.models import Question, Choice
import json

try:
    from types import SimpleNamespace as Namespace
except ImportError:
    from argparse import Namespace


# Create your views here.

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    output = [QuestionSerializer(q).data for q in latest_question_list]
    return JsonResponse(output, safe=False)


def choice_list(request, question_id):
    question = Question.objects.get(pk=question_id)
    output = [ChoiceSerializer(choice).data for choice in question.choices.all()]

    return JsonResponse(output, safe=False)

@csrf_exempt
def add_poll(request):
    new_poll = json.loads(request.body)

    if request.method == 'PUT':
        Question.objects.get(pk=new_poll.id)

        if QuestionSerializer(data=new_poll).is_valid():
            print(json.dumps(new_poll, sort_keys=False, indent=2))

    if request.method == 'POST':

        if QuestionSerializer(data=new_poll).is_valid():
            print(json.dumps(new_poll, sort_keys=False, indent=2))
            new_poll = json.loads(request.body, object_hook=lambda d: Namespace(**d))
            q = Question(question_txt=new_poll.question_txt, pub_date=timezone.now())
            q.save()
            [q.choices.create(choice_txt=choice.choice_txt, votes=0) for choice in new_poll.choices]
            print(QuestionSerializer(q).data)

        # new_poll = QuestionSerializer(data=json.loads(request.body))
        # print(new_poll.is_valid())
        #
        # if new_poll.is_valid():
        #     new_poll.save()
        #     print(json.dumps(new_poll.data, sort_keys=True, indent=2))
        #     # new_poll.
        # else:
        #     print(json.dumps(new_poll.data, sort_keys=True, indent=2))
        #     print(new_poll.errors)

    return JsonResponse(QuestionSerializer(q).data, safe=False)


@csrf_exempt
def poll_action(request, question_id):
    if request.method == 'PUT':
        poll_to_be_edited = Question.objects.get(pk=question_id)

        request_poll = json.loads(request.body, object_hook=lambda d: Namespace(**d))
        poll_to_be_edited.question_txt = request_poll.question_txt

        for choice in request_poll.choices:
            try:
                choice_to_update = Choice.objects.get(pk=choice.id)
                choice_to_update.choice_txt = choice.choice_txt
                choice_to_update.save()

            except Choice.DoesNotExist:
                poll_to_be_edited.choices.create(choice_txt=choice.choice_txt, votes=0)

        poll_to_be_edited.save()
        print(QuestionSerializer(poll_to_be_edited).data)
        return JsonResponse(QuestionSerializer(request_poll).data, safe=False)
        # new_poll = json.loads(request.body)
        # print(json.loads(new_poll, object_hook=lambda d: Namespace(**d)))

    if request.method == 'DELETE':
        q_to_delete = Question.objects.get(pk=question_id)
        q_to_delete.delete()

        return JsonResponse(json.dumps(question_id), safe=False)

    return HttpResponse("Fail to do Action on poll = %s" % question_id)


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
