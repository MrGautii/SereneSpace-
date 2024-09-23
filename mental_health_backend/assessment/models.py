from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    text = models.TextField()

    category = models.CharField(max_length=100, null=True, blank=True)  # Category (e.g., Depression, Anxiety)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text

class Assessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Removed default=1
    score = models.IntegerField(null=True, blank=True)  # Allow null or blank during creation
    category_scores = models.JSONField(null=True, blank=True)
    interpretation = models.TextField(null=True, blank=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Assessment by {self.user} with score {self.score}"

class Answer(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='answers')
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    response = models.CharField(max_length=255)

    def __str__(self):
        return f"Answer to {self.question.text}"
