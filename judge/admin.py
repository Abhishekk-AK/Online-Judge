from django.contrib import admin
from judge.models import Problem, Solution, TestCase

admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(TestCase)