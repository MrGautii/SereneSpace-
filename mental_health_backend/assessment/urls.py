from django.urls import path
from .views import QuestionListView, AssessmentCreateView, RecommendationsView, InsightsView

urlpatterns = [
    path('questions/', QuestionListView.as_view(), name='question-list'),
    path('submit/', AssessmentCreateView.as_view(), name='assessment-submit'),
    path('recommendations/', RecommendationsView.as_view(), name='personalized-recommendations'),
    path('insights/', InsightsView.as_view(), name='assessment-insights'),
]
