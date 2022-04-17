from django.urls import path
from . import views
from ums.views import signin, register, signout
from pms.views import add_question, like_question, question_stream, question_thread

urlpatterns = [
    path('', views.index, name='home'),
    path('signin/', signin, name='signin'),
    path('register/', register, name='register'),
    path('signout/', signout, name='signout'),
    path('add_question/', add_question, name='add_question'),
    path('question/<int:qid>', question_thread, name='view_question_thread'),
    path('like/<int:pk>', like_question, name='like_question'),
    path('question_stream', question_stream, name='question_stream')
]
