from collections import namedtuple

from django.http import JsonResponse, HttpResponse
from django.utils import timezone

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
    if request.method == 'POST':
        new_poll = json.loads(request.body.decode('utf-8'))
        print()

        if QuestionSerializer(data=new_poll).is_valid():
            print(json.dumps(new_poll, sort_keys=False, indent=2))
            new_poll = json.loads(request.body, object_hook=lambda d: Namespace(**d))
            q = Question(question_txt=new_poll.question_txt, pub_date=timezone.now())
            print(q.question_txt)
            # [q.choices.create(choice_txt=choice.choice_txt, votes=0) for choice in new_poll.choices]
            # q.save()
            # print(q)

    return JsonResponse(json.loads(request.body), safe=False)


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
