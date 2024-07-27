from django.urls import path
from judge.views import problems, description

urlpatterns = [
    path('problems/', problems, name='Problems'),
    path('problems/<int:problem_id>/', description, name='description'),
]