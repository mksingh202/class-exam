from django.urls import path
from .views import QuestionView, QuestionDetailView, OptionView, AnswerView, RegisterView, ResultView
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
    path('login', obtain_auth_token, name='api_token_auth'),    # Login for Teachers and Pupils
    path('questions', QuestionView.as_view()),                  # Get/Add questions
    path('questions/<int:pk>', QuestionDetailView.as_view()),   # Get/Delete question on its id
    path('options/<int:question_id>', OptionView.as_view()),    # Get/Add/Delete options for passed question
    path('results/<int:pupil_id>', ResultView.as_view()),       # Get result of specific pupils with their percentage
    path('register', RegisterView.as_view()),                   # Pupils registration, teachers registration will be done through Django Admin
    path('answers', AnswerView.as_view()),                     # Submit answers for questions
]

urlpatterns = format_suffix_patterns(urlpatterns)