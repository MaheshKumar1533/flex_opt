from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from django.utils import timezone


class Student(models.Model):
    name = models.CharField(max_length=100)
    rollno = models.CharField(max_length=20, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Will store hashed password
    dept = models.CharField(max_length=50)
    year = models.IntegerField()
    section = models.CharField(max_length=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def set_password(self, raw_password):
        """Hash and set the password"""
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """Check if the provided password matches the stored hashed password"""
        return check_password(raw_password, self.password)

    def __str__(self):
        return f"{self.name} ({self.rollno})"

    class Meta:
        ordering = ['rollno']


class Subject(models.Model):
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=20, unique=True)
    max_limit = models.IntegerField(default=30)
    current_count = models.IntegerField(default=0)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_full(self):
        """Check if the subject has reached its maximum limit"""
        return self.current_count >= self.max_limit

    def available_slots(self):
        """Return the number of available slots"""
        return max(0, self.max_limit - self.current_count)

    def __str__(self):
        return f"{self.code} - {self.name}"

    class Meta:
        ordering = ['code']


class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    subjects = models.ManyToManyField(Subject, related_name='quizzes')
    assigned_students = models.ManyToManyField(Student, related_name='assigned_quizzes')

    def is_available(self):
        """Check if the quiz is currently available for taking"""
        now = timezone.now()
        return (self.is_active and
                self.start_time <= now and
                (self.end_time is None or now <= self.end_time))

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class StudentQuizResponse(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='quiz_responses')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='responses')
    selected_subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='selected_by')
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.name} -> {self.selected_subject.code}"

    class Meta:
        unique_together = ['student', 'quiz']  # Ensure one response per student per quiz
        ordering = ['-submitted_at']
