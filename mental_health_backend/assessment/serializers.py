from rest_framework import serializers
from .models import Question, Assessment, Answer
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['id', 'text', 'category']


class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'response']


class AssessmentSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True)  # Accept email during POST request
    answers = AnswerSerializer(many=True)
    score = serializers.IntegerField(read_only=True)  # Score is read-only

    class Meta:
        model = Assessment
        fields = ['email', 'score', 'category_scores', 'interpretation', 'answers']

    def validate_email(self, email):
        """Check if user with the provided email exists."""
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError("User with this email does not exist.")
        return email

    def create(self, validated_data):
        email = validated_data.pop('email')  # Get email from request
        user = User.objects.get(email=email)  # Find the user by email

        # Create the assessment object for the user
        assessment = Assessment.objects.create(user=user)

        # Process answers, calculate scores, etc.
        answers_data = validated_data.pop('answers')
        total_score = 0
        category_scores = {}

        for answer_data in answers_data:
            question = Question.objects.get(id=answer_data['question'].id)
            response = answer_data['response']

            # Custom scoring logic
            if response.lower() == "yes":
                total_score += 1

            # Calculate category scores
            if question.category in category_scores:
                category_scores[question.category] += 1
            else:
                category_scores[question.category] = 1

            # Create the answer for each question
            Answer.objects.create(assessment=assessment, question=question, response=response)

        # Update assessment score and category scores
        assessment.score = total_score
        assessment.category_scores = category_scores
        assessment.interpretation = self.get_interpretation(total_score)
        assessment.save()

        return assessment

    def get_interpretation(self, score):
        """Generate interpretation based on the total score."""
        if score < 5:
            return "Your mental health seems stable. Keep monitoring."
        elif score < 10:
            return "Mild signs of stress or anxiety detected."
        else:
            return "Signs of severe stress or anxiety. Consider consulting a professional."
