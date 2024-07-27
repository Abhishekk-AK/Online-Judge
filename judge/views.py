from django.shortcuts import render, redirect
from judge.models import Problem, Solution, TestCase
from django.template import loader
from django.http import HttpResponse
#from judge.forms import CodeSubmissionForm
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def problems(request):
    problems = Problem.objects.all()

    context = {
        'problems': problems,
    }
    template = loader.get_template('problems.html')

    return HttpResponse(template.render(context, request))


@login_required
def description(request, problem_id):
    req_problem = Problem.objects.get(id = problem_id)

    context = {
        'req_problem': req_problem,
    }

    template = loader.get_template('description.html')

    return HttpResponse(template.render(context, request))
    
