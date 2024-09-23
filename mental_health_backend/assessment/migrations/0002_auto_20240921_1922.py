# Generated by Django 5.1 on 2024-09-21 13:52

from django.db import migrations

def create_default_questions(apps, schema_editor):
    Question = apps.get_model('assessment', 'Question')
    default_questions = [
        {"text": "How often do you feel anxious?", "category": "Anxiety"},
        {"text": "Do you have trouble sleeping?", "category": "Sleep"},
        {"text": "Do you feel hopeless or down?", "category": "Depression"},
        {"text": "Do you experience panic attacks?", "category": "Anxiety"},
        {"text": "Have you lost interest in activities you used to enjoy?", "category": "Depression"},
        {"text": "Do you find it difficult to concentrate?", "category": "Attention"},
        {"text": "Do you feel fatigued often?", "category": "Energy"},
        {"text": "Do you feel stressed frequently?", "category": "Stress"},
        {"text": "Do you have difficulty controlling your emotions?", "category": "Mood"},
        {"text": "Do you avoid social interactions?", "category": "Social Anxiety"},
    ]

    for question in default_questions:
        Question.objects.create(**question)

class Migration(migrations.Migration):
    dependencies = [
        ("assessment", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(create_default_questions),
    ]
