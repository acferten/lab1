from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
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

    def get_object(self, queryset=None):
        question = super(DetailView, self).get_object(queryset)
        if question.was_published_recently or self.request.user.is_staff:
            return question
        else:
            raise PermissionDenied()


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


@login_required
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
            question.question_votes += 1
            question.save()
            selected_choice.votes += 1
            selected_choice.save()
            user_voted = Vote.objects.create(question=question, user=request.user)
            user_voted.save()

            return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))


class SignUpView(generic.CreateView):
    model = AdvUser
    template_name = 'polls/register.html'
    success_url = reverse_lazy('login')
    form_class = UserRegisterForm
    success_page = "polls"


class UserDetailView(LoginRequiredMixin, generic.DetailView):
    model = AdvUser
    template_name = 'polls/profile.html'


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = AdvUser
    success_url = '/'
    fields = ['username', 'avatar']
    template_name = 'polls/profile_update.html'

    def get_object(self, queryset=None):
        obj = super(UserUpdateView, self).get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied()
        else:
            return self.request.user


class UserDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = AdvUser
    success_url = reverse_lazy('polls:index')
    template_name = 'polls/confirm_delete.html'

    def get_object(self, queryset=None):
        obj = super(UserDeleteView, self).get_object(queryset)
        if obj != self.request.user:
            raise PermissionDenied()
