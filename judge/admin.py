from django.contrib import admin
from judge.models import Problem, Solution, TestCase, CodeSubmission

admin.site.register(Problem)
admin.site.register(Solution)
admin.site.register(TestCase)
admin.site.register(CodeSubmission)
