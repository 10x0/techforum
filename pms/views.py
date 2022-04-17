import json
import time
from django.http import HttpResponse, JsonResponse, StreamingHttpResponse
from django.shortcuts import redirect, render
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from pms.models import Question


@login_required(login_url='signin')
def add_question(request):
    if request.method == 'POST':
        q = Question()
        if len(request.FILES) != 0:
            q.image = request.FILES['image']
        q.questioner = request.user
        q.question = request.POST['question']
        q.brief = request.POST['brief']
        q.save()
        return redirect('home')

    return render(request, 'user/add_question.html')


def event_stream():
    initial_data = ""
    while True:
        questions = list(Question.objects.order_by(
            "-date_updated"))
        data = json.dumps([question.get_json() for question in questions],
                          cls=DjangoJSONEncoder
                          )

        if not initial_data == data:
            yield "\ndata: {}\n\n".format(data)
            initial_data = data
        time.sleep(1)


def question_stream(request):
    response = StreamingHttpResponse(event_stream())
    response['Content-Type'] = 'text/event-stream'
    return response


def question_thread(request, qid):
    question = get_object_or_404(Question, pk=qid)
    return render(request, 'user/question_thread.html', {'question': question})


@login_required()
def like_question(request, pk):
    question = get_object_or_404(Question, id=pk)
    if request.user not in question.likes.all():
        question.likes.add(request.user)
    else:
        question.likes.remove(request.user)
    return JsonResponse({'a': 'Success'})


# @login_required()
# def add_answer(request, pk):
#     question = get_object_or_404(Question, id=pk)
#     a = Answer()
#     a.answer = request.POST['answer']
#     a.user_a = request.user
#     a.save()
#     question.answers.add(a)
#     return redirect('home')


# @login_required()
# def delete_question(request, pk):
#     question = get_object_or_404(Question, id=pk)
#     if question.user_q == request.user:
#         question.delete()
#     return redirect('home')
