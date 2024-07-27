from django.urls import path
from judge.views import problems, description

urlpatterns = [
    path('problems/', all_polls, name='problems'),
    path('problems/<int:problem_id>/', poll_detail, name='description'),
]