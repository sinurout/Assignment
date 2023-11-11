from django.db import models
from rest_framework import serializers

class Student(models.Model):
    name = models.CharField(max_length=100)
    roll_no = models.IntegerField(unique=True)
    subject1 = models.CharField(max_length=100)
    subject2 = models.CharField(max_length=100)
    subject3 = models.CharField(max_length=100)
    subject4 = models.CharField(max_length=100)
    subject5 = models.CharField(max_length=100)
    score1 = models.FloatField()
    score2 = models.FloatField()
    score3 = models.FloatField()
    score4 = models.FloatField()
    score5 = models.FloatField()
    image = models.ImageField(upload_to='images/')
    class_level = models.IntegerField(choices=[(i, i) for i in range(1, 13)])

    def __str__(self):
        return self.name
      

class StudentSerializer(serializers.ModelSerializer):
    total_score = serializers.SerializerMethodField()

    class Meta:
        model = Student
        fields = '__all__'

    def get_total_score(self, obj):
        return obj.score1 + obj.score2 + obj.score3 + obj.score4 + obj.score5
