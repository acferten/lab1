import datetime
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class AdvUser(AbstractUser):
    avatar = models.ImageField(upload_to='polls/media/avatars', blank=False)


class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    question_votes = models.IntegerField(default=0)
    short_description = models.CharField(max_length=400)
    description = models.CharField(max_length=3000)
    image = models.ImageField(upload_to='media/questions', blank=True)

    @property
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)

    def __str__(self):
        return self.question_text


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    def get_percentage(self):
        percents = self.votes * 100 / self.question.question_votes
        return percents


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(AdvUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.question.question_text
