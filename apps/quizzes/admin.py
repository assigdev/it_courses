from django.contrib import admin
from .models import Quiz, Question, AnswerVar
import nested_admin


class AnswerVarInline(nested_admin.NestedTabularInline):
    model = AnswerVar
    extra = 0
    sortable_field_name = "position"


class QuestionInline(nested_admin.NestedStackedInline):
    model = Question
    extra = 1
    inlines = [AnswerVarInline]
    sortable_field_name = "position"


@admin.register(Quiz)
class QuizAdmin(nested_admin.NestedModelAdmin):
    inlines = [QuestionInline]

