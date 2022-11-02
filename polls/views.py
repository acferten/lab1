from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import CreateView

from .forms import UserRegisterForm
from .models import Question, Choice, AdvUser, Vote
from django.urls import reverse, reverse_lazy
from django.views import generic


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        return Question.objects.order_by('-pub_date')


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': 'вы не сделали выбор'
        })
    else:
        if Vote.objects.filter(question=question, user=request.user).exists():
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': 'вы уже приняли участие в голосовании'
            })
        else:
            user_voted = Vote.objects.create(question=question, user=request.user)
            selected_choice.votes += 1
            question.question_votes += 1
            question.save()
            selected_choice.save()
            user_voted.save()

            # percent_choices = []
            # allchoices = Choice.objects.filter(question=question).aggregate(Sum('votes'))
            #
            # for choice in Choice.objects.filter(question=question):
            #     percent_choices.append((choice.votes/allchoices)*100)

            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class SignUpView(CreateView):
    model = AdvUser
    template_name = 'polls/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_page = "polls"


class UserDetailView(LoginRequiredMixin, DetailView):
    model = AdvUser
    template_name = 'polls/profile.html'


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = AdvUser
    success_url = '/'
    fields = ['username', 'password', 'avatar']
    template_name = 'polls/profile_update.html'


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = AdvUser
    success_url = reverse_lazy('polls:index')
    template_name = 'polls/confirm_delete.html'
