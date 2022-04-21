import json
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


# def search(request):
#     q = request.GET.get('q')
#     if q:
#         query = MultiMatch(
#             query=q, fields=['question', 'brief'])
#         s = Search(index='questions').query(query)
#         questions = s.execute()
#     else:
#         questions = ''
#     if len(questions['hits']['hits']) > 0:
#         data = questions.hits.hits
#         response = [res.to_dict() for res in data]
#     else:
#         response = []
#     return JsonResponse({'data': response}, safe=False)
