from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Question, Assessment
from .serializers import QuestionSerializer, AssessmentSerializer
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db import models


# View for fetching all questions
class QuestionListView(generics.ListAPIView):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


# Custom method to get the user by email from the request
def get_user_from_email(request):
    email = request.data.get('email') or request.headers.get('Email') or  request.query_params.get('email')
    if not email:
        return None
    return get_object_or_404(User, email=email)


# View for submitting an assessment and calculating scores
class AssessmentCreateView(APIView):
    # Remove IsAuthenticated permission

    def post(self, request, *args, **kwargs):
        # Custom email-based authentication
        user = get_user_from_email(request)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        
        # Attach user to the request data
        request.data['user'] = user.id

        # Serialize and create assessment
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            assessment = serializer.save()
            return Response(AssessmentSerializer(assessment).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for generating personalized recommendations based on the assessment
class RecommendationsView(APIView):
    def get(self, request, *args, **kwargs):
        email = request.query_params.get('email')  # Get email from query parameters
        if not email:
            return Response({"error": "Email is required"}, status=400)
        
        try:
            user = User.objects.get(email=email)  # Find user by email
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)
        
        assessment = Assessment.objects.filter(user=user).last()
        if not assessment:
            return Response({"error": "No assessments found"}, status=400)

        recommendations = self.get_recommendations(assessment.score, assessment.category_scores)

        return Response({
            'assessment': AssessmentSerializer(assessment).data,
            'recommendations': recommendations
        })

    def get_recommendations(self, score, category_scores):
        recommendations = []
        if score < 10:
            recommendations.append("Maintain a healthy lifestyle, exercise regularly.")
        elif 10 <= score < 20:
            recommendations.append("Consider relaxation techniques like meditation and yoga.")
        else:
            recommendations.append("Seek professional help as soon as possible.")
        
        # Add category-specific recommendations
        for category, cat_score in category_scores.items():
            if cat_score > 5:
                recommendations.append(f"Focus on improving your mental well-being in the {category} category.")
        
        return recommendations


# View for fetching insights from past assessments
class InsightsView(APIView):
    def get(self, request, *args, **kwargs):
        # Custom email-based authentication
        user = get_user_from_email(request)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get user assessments
        assessments = Assessment.objects.filter(user=user)
        if not assessments.exists():
            return Response({"error": "No assessments found"}, status=status.HTTP_400_BAD_REQUEST)

        # Calculate insights
        avg_score = assessments.aggregate(models.Avg('score'))['score__avg']
        high_score_count = assessments.filter(score__gt=20).count()

        return Response({
            'average_score': avg_score,
            'high_score_count': high_score_count,
        })


# View for submitting assessment answers
class AssessmentSubmitView(APIView):
    def post(self, request, *args, **kwargs):
        # Custom email-based authentication
        user = get_user_from_email(request)
        if not user:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Attach user to the request data
        request.data['user'] = user.id

        # Serialize and save the assessment
        serializer = AssessmentSerializer(data=request.data)
        if serializer.is_valid():
            assessment = serializer.save()
            return Response(AssessmentSerializer(assessment).data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
