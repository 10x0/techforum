from pms.models import Question
from django_elasticsearch_dsl import Document, Index, fields

questions = Index('questions')


@questions.doc_type
class QuestionDocument(Document):

    class Index:
        name = 'questions'

        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0
        }

    class Django:
        model = Question

        fields = [
            'id',
            'question',
            'brief',
        ]

        search_fields = ['id', 'question', 'brief']
        multi_match_search_fields = ['id', 'question', 'brief']
