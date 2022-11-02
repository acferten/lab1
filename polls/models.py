import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone


class AdvUser(AbstractUser):
    avatar = models.ImageField(upload_to='polls/media/avatars', blank=False)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    question_votes = models.IntegerField(default=0)

    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    percent_votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.question.question_text


@receiver(pre_save, sender=Choice)
def percent_votes(sender, **kwargs):
    choice = kwargs['instance']
    question = Question.objects.get(pk=choice.question.id)
    if question.question_votes != 0:
        for choice in Choice.objects.filter(question=question):
            choice.percent_votes = (choice.votes / question.question_votes) * 100
    # if question.question_votes != 0:
    #     choice.percent_votes = (choice.votes / question.question_votes) * 100
    else:
        choice.percent_votes = 0

