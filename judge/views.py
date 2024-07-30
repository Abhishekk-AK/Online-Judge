from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings
from pathlib import Path
import uuid
import subprocess 
import os
import tempfile


from judge.models import Problem, Solution, TestCase, CodeSubmission
from judge.forms import CodeSubmissionForm

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
    req_problem = Problem.objects.get(id=problem_id)
    form = CodeSubmissionForm()
    context = {
        'req_problem': req_problem,
        'form': form,
    }
    template = loader.get_template('description.html')
    return HttpResponse(template.render(context, request))

'''@login_required
def run(request, problem_id):
    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem_id = problem_id
            submission.save()
            
            problem = Problem.objects.get(id=problem_id)
            user_input = form.cleaned_data.get('input_data')
            
            if user_input:
                # Run the code with user input
                user_output = run_code(submission.language, submission.code, user_input)
                submission.output_data = user_output
                submission.save()
                return render(request, 'runresult.html', {'submission': submission, 'user_output': user_output})
    else:
        form = CodeSubmissionForm()
    return render(request, 'description.html', {'form': form})'''

@login_required
def submit(request, problem_id):
    if request.method == 'POST':
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.problem_id = problem_id
            submission.save()
            
            problem = Problem.objects.get(id=problem_id)
            user_input = form.cleaned_data.get('input_data')
            
            if 'run' in request.POST:
                #if user_input:
                    # Run the code with user input
                    user_output = run_code(submission.language, submission.code, user_input)
                    submission.output_data = user_output
                    submission.save()
                    return render(request, 'runresult.html', {'submission': submission, 'user_output': user_output})
    
            elif 'submit' in request.POST:
                # Run the code with test cases
                test_cases = TestCase.objects.filter(problem=problem)
                correct = True
                failed_test_cases = []
                all_outputs = []

                for index, test_case in enumerate(test_cases):
                    output = run_code(submission.language, submission.code, test_case.input)
                    all_outputs.append(f'Input: {test_case.input}\nOutput: {output.strip()}')
                    if output.strip() != test_case.output.strip():
                        correct = False
                        failed_test_cases.append(index + 1)
                
                if correct:
                    verdict = 'Correct'
                else:
                    verdict = f'Wrong'
                
                Solution.objects.create(problem=problem, verdict=verdict)
                submission.output_data = "\n\n".join(all_outputs)
                submission.save()
                return render(request, 'subresult.html', {'submission': submission, 'verdict': verdict, 'failed_test_cases': failed_test_cases})
    else:
        form = CodeSubmissionForm()
    return render(request, 'description.html', {'form': form})

def run_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ['codes', 'inputs', 'outputs']

    for directory in directories:
        dir_path = project_path / 'media' / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / 'media' / 'codes'
    inputs_dir = project_path / 'media' / 'inputs'
    outputs_dir = project_path / 'media' / 'outputs'

    unique = str(uuid.uuid4())

    code_file_name = f'{unique}.{language}'
    input_file_name = f'{unique}.txt'
    output_file_name = f'{unique}.txt'

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    with open(code_file_path, 'w') as code_file:
        code_file.write(code)

    with open(input_file_path, 'w') as input_file:
        input_file.write(input_data)

    with open(output_file_path, 'w') as output_file:
        pass  # create an empty file

    if language == 'cpp':
        executable_path = codes_dir / unique
        compile_result = subprocess.run(
            ['g++', str(code_file_path), '-o', str(executable_path)]
        )
        if compile_result.returncode == 0:
            with open(input_file_path, 'r') as input_file:
                with open(output_file_path, 'w') as output_file:
                    subprocess.run(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                    )

    elif language == 'c':
        executable_path = codes_dir / unique
        compile_result = subprocess.run(
            ['gcc', str(code_file_path), '-o', str(executable_path)]
        )
        if compile_result.returncode == 0:
            with open(input_file_path, 'r') as input_file:
                with open(output_file_path, 'w') as output_file:
                    subprocess.run(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                    )

    elif language == 'py':
        with open(input_file_path, 'r') as input_file:
            with open(output_file_path, 'w') as output_file:
                subprocess.run(
                    ['python', str(code_file_path)],
                    stdin=input_file,
                    stdout=output_file,
                )

    # read output from output file
    with open(output_file_path, 'r') as output_file:
        output_data = output_file.read()

    return output_data
