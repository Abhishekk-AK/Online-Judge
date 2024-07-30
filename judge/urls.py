from django.urls import path
from judge.views import problems, description, submit

urlpatterns = [
    path('problems/', problems, name='problems'),
    path('problems/<int:problem_id>/', description, name='description'),
  #  path('problems/<int:problem_id>/run/', run, name='run'),
    path('problems/<int:problem_id>/submit/', submit, name='submit'),
]
