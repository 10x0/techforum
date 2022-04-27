import json
import time
from django.http import Http404, JsonResponse, StreamingHttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
import language_tool_python

# import language_tool_python
from notification.models import Notification
from pms.models import Answer, Question


@login_required(login_url='signin')
def check_question(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode("utf-8"))
        question = data['question']
        brief = data['brief']
        tool = language_tool_python.LanguageToolPublicAPI('en-US')
        question_matches = tool.check(question)
        brief_matches = tool.check(brief)
        cq = language_tool_python.utils.correct(question, question_matches)
        cb = language_tool_python.utils.correct(brief, brief_matches)
        return JsonResponse({
            'question': question,
            'corrected_question': cq,
            'brief': brief,
            'corrected_brief': cb
        })


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
        return JsonResponse({'success': True})
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


def thread_stream(qid):
    initial_data = ""
    while True:
        data = json.dumps(get_object_or_404(Question, id=qid).get_json(),
                          cls=DjangoJSONEncoder
                          )
        if not initial_data == data:
            yield "\ndata: {}\n\n".format(data)
            initial_data = data
        time.sleep(1)


def question_thread_stream(request, qid):
    response = StreamingHttpResponse(thread_stream(qid=qid))
    response['Content-Type'] = 'text/event-stream'
    return response


def question_thread(request, qid):
    question = get_object_or_404(Question, id=qid)
    return render(request, 'user/question_thread.html', {'question': question})


@ login_required()
def like_question(request, id):
    question = get_object_or_404(Question, id=id)
    if request.user not in question.likes.all():
        question.likes.add(request.user)
        if not request.user == question.questioner:
            notify = Notification()
            notify.question = question
            notify.actor = request.user
            notify.recipient = question.questioner
            notify.notification_type = 1
            notify.notification_text = "@{} liked your question.".format(
                request.user)
            notify.save()
    else:
        question.likes.remove(request.user)
        if not request.user == question.questioner:
            notify = Notification.objects.filter(
                question=question, actor=request.user, notification_type=1)
            notify.delete()
    return JsonResponse({'status': 'Success'})


@login_required()
def like_answer(request, id):
    answer = get_object_or_404(Answer, id=id)
    question = Question.objects.get(answers=answer)
    if request.user not in answer.likes.all():
        answer.likes.add(request.user)
        if not request.user == answer.answerer:
            notify = Notification()
            notify.question = question
            notify.actor = request.user
            notify.recipient = answer.answerer
            notify.notification_type = 1
            notify.notification_text = "@{} liked your answer.".format(
                request.user)
            notify.save()
    else:
        answer.likes.remove(request.user)
        if not request.user == answer.answerer:
            notify = Notification.objects.filter(
                question=question, actor=request.user, notification_type=1)
            notify.delete()
    return JsonResponse({'status': 'Success'})


@login_required()
def add_answer(request, qid):
    question = get_object_or_404(Question, id=qid)
    ans = Answer()
    ans.answerer = request.user
    data = json.loads(request.body.decode("utf-8"))
    ans.answer = data['answer']
    ans.save()
    question.answers.add(ans)
    if not request.user == question.questioner:
        notify = Notification()
        notify.question = question
        notify.actor = request.user
        notify.recipient = question.questioner
        notify.notification_type = 2
        notify.notification_text = "@{} responded on your question.".format(
            request.user)
        notify.save()
    return JsonResponse({'status': "Success"})


def notification_event_stream(request):
    initial_data = ""
    while True:
        notifications = list(Notification.objects.filter(recipient=request.user, seen=False).order_by(
            "-date_updated"))
        data = json.dumps([notification.get_json() for notification in notifications],
                          cls=DjangoJSONEncoder
                          )

        if not initial_data == data:
            yield "\ndata: {}\n\n".format(data)
            initial_data = data
        time.sleep(1)


def notification_stream(request):
    response = StreamingHttpResponse(notification_event_stream(request))
    response['Content-Type'] = 'text/event-stream'
    return response


@login_required()
def delete_question(request, id):
    if request.method == "DELETE":
        question = get_object_or_404(Question, id=id)
        if question.questioner == request.user:
            question.delete()
            return JsonResponse({'status': 'Success'})
    return JsonResponse({'status': 'Failure'})


@login_required()
def delete_answer(request, id):
    if request.method == "DELETE":
        answer = get_object_or_404(Answer, id=id)
        print(answer)
        if answer.answerer == request.user:
            answer.delete()
            return JsonResponse({'status': 'Success'})
    return JsonResponse({'status': 'Failure'})


@login_required()
def view_notification(request, id):
    if request.method == "POST":
        notification = get_object_or_404(Notification, id=id)
        if notification.recipient == request.user:
            notification.seen = True
            notification.save()
            # notification.delete()
            return JsonResponse({'status': 'Success'})
    return JsonResponse({'status': 'Failure'})
