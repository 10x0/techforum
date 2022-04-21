from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.conf.urls import handler404
from .views import index, error404
from search.views import search
from ums.views import signin, register, signout
from pms.views import add_answer, add_question, delete_answer, delete_question, like_answer, like_question, notification_stream, question_stream, question_thread, question_thread_stream, view_notification

urlpatterns = [
    path('', index, name='home'),
    path('signin/', signin, name='signin'),
    path('register/', register, name='register'),
    path('signout/', signout, name='signout'),
    path('add_question/', add_question, name='add_question'),
    path('add_answer/<int:qid>', add_answer, name='add_answer'),
    path('question/<int:qid>', question_thread,
         name='view_question_thread'),
    path('like_question/<int:id>', like_question, name='like_question'),
    path('like_answer/<int:id>', like_answer, name='like_answer'),
    path('question_stream', question_stream, name='question_stream'),
    path('question_thread_stream/<int:qid>', question_thread_stream,
         name='question_thread_stream'),
    path('notification_stream', notification_stream, name='notification_stream'),
    path('search/', search, name='search'),
    path('delete_question/<int:id>', delete_question, name='delete_question'),
    path('delete_answer/<int:id>', delete_answer, name='delete_answer'),
    path('view_notification/<int:id>',
         view_notification, name='view_notification'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


handler404 = error404
