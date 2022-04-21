import json
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Answer(models.Model):
    answerer = models.ForeignKey(User, on_delete=models.CASCADE)
    answer = models.CharField(max_length=2000)
    image = models.ImageField(
        upload_to='answers/', blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        User, related_name='answer_likes', blank=True, default=None)

    def get_json(self):
        data = {'id': self.id}
        data['answerer'] = self.answerer.username
        data['answer'] = self.answer
        data['image'] = str(self.image)
        data['date_updated'] = self.date_updated
        data['likes'] = [like.username for like in self.likes.all()]
        return data


class Question(models.Model):
    questioner = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.CharField(max_length=200)
    brief = models.CharField(max_length=2000)
    image = models.ImageField(
        upload_to='questions/', blank=True, null=True)
    date_updated = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(
        User, related_name='question_likes', blank=True, default=None)
    answers = models.ManyToManyField(
        Answer, related_name='answers', default=None, blank=True)

    def __str__(self) -> str:
        return self.question

    def likes_count(self):
        return self.likes.all().count()

    def answers_count(self):
        return self.answers.all().count()

    def get_sorted_answers(self):
        return self.answers.all().order_by('likes')

    def get_json(self):
        data = {'id': self.id}
        data['questioner'] = self.questioner.username
        data['question'] = self.question
        data['brief'] = self.brief
        if self.image:
            data['image'] = str(self.image.url)
        data['date_updated'] = self.date_updated
        data['likes'] = [like.username for like in self.likes.all()]
        data['answers'] = [answer.get_json()
                           for answer in self.get_sorted_answers().all()]
        return data


LIKE_CHOICES = (
    ("like", "like"),
    ("Unlike", "Unlike")
)


class Like(models.Model):
    liker = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.CharField(
        max_length=10, choices=LIKE_CHOICES, default='like')

    def __str__(self) -> str:
        return self.liker.username

    def get_json(self):
        data = {'id': self.id}
        data['liker'] = self.liker.username
        data['value'] = self.value
        return data
