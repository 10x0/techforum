from django.http import JsonResponse
from django.shortcuts import render
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch

from search.documents import QuestionDocument


def search(request):
    questions = ''
    q = request.GET.get('q')
    if q:
        query = MultiMatch(
            query=q, fields=['question', 'brief'])
        questions = QuestionDocument.search().query(query)
        return JsonResponse({'data': [question.get_json() for question in questions.to_queryset()]}, safe=False)
    return JsonResponse({'data': []})
