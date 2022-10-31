from django.contrib import admin
from .models import Question, Choice, AdvUser, Vote

admin.site.register(AdvUser)
admin.site.register(Vote)


class ChoiceInLine(admin.TabularInline):
    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    inlines = [ChoiceInLine]


admin.site.register(Question, QuestionAdmin)
