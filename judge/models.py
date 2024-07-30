from django.db import models
from django.contrib.auth.models import User

class Problem(models.Model):
    statement = models.CharField(max_length=200)
    name = models.CharField(max_length=3000)
    code = models.CharField(max_length=20)
    difficulty = models.CharField(
        max_length=10,
        blank=True,
        choices=[('Hard', 'Hard'), ('Easy', 'Easy'), ('Medium', 'Medium')],
    )

    def __str__(self):
        return self.statement

class Solution(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    verdict = models.CharField(max_length=50)
    submitted_at = models.DateTimeField(auto_now_add=True)

class TestCase(models.Model):
    input = models.CharField(max_length=255)
    output = models.CharField(max_length=255)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

class CodeSubmission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
    language = models.CharField(max_length=100)
    code = models.TextField()
    input_data = models.TextField(null=True, blank=True)
    output_data = models.TextField(null=True, blank=True)
    result = models.CharField(max_length=10, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)
