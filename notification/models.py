from django.db import models
from django.contrib.auth.models import User
# Create your models here.
from pms.models import Answer, Question


NOTIFICATION_TYPES = ((1, 'like'), (2, 'reply'), (3, 'follow'))


class Notification(models.Model):
    question = models.ForeignKey(
        Question, on_delete=models.CASCADE, blank=True)
    actor = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='sender')
    recipient = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='receiver')
    notification_type = models.IntegerField(choices=NOTIFICATION_TYPES)
    notification_text = models.CharField(max_length=75, blank=True)
    date_updated = models.DateTimeField(auto_now_add=True)
    seen = models.BooleanField(default=False)

    def __str__(self) -> str:
        return '{} -> {}'.format(self.actor, self.recipient)

    def get_json(self):
        data = {}
        data['id'] = self.id
        data['question'] = self.question.get_json()
        data['actor'] = self.actor.username
        data['recipient'] = self.recipient.username
        data['notification_type'] = self.notification_type
        data['notification_text'] = self.notification_text
        data['date_updated'] = self.date_updated
        data['seen'] = self.seen
        return data
