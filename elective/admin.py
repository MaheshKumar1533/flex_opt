from django.contrib import admin
from .models import Student, Subject, Quiz, StudentQuizResponse


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['rollno', 'name', 'email', 'dept', 'year', 'section', 'created_at']
    list_filter = ['dept', 'year', 'section', 'created_at']
    search_fields = ['rollno', 'name', 'email']
    ordering = ['rollno']

    fieldsets = (
        ('Personal Information', {
            'fields': ('name', 'rollno', 'email')
        }),
        ('Academic Information', {
            'fields': ('dept', 'year', 'section')
        }),
        ('Authentication', {
            'fields': ('password',),
            'description': 'Enter plain text password. It will be automatically hashed.'
        })
    )

    def save_model(self, request, obj, form, change):
        if not change or 'password' in form.changed_data:
            # Only hash password if it's a new object or password was changed
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['code', 'name', 'max_limit', 'current_count', 'available_slots', 'created_at']
    list_filter = ['created_at']
    search_fields = ['code', 'name']
    ordering = ['code']

    readonly_fields = ['current_count']

    def available_slots(self, obj):
        return obj.available_slots()
    available_slots.short_description = 'Available Slots'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'start_time', 'end_time', 'subjects_count', 'assigned_students_count', 'responses_count', 'created_at']
    list_filter = ['is_active', 'created_at', 'start_time']
    search_fields = ['title', 'description']
    ordering = ['-created_at']

    filter_horizontal = ['subjects', 'assigned_students']

    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'is_active')
        }),
        ('Schedule', {
            'fields': ('start_time', 'end_time')
        }),
        ('Configuration', {
            'fields': ('subjects', 'assigned_students')
        })
    )

    def subjects_count(self, obj):
        return obj.subjects.count()
    subjects_count.short_description = 'Subjects'

    def assigned_students_count(self, obj):
        return obj.assigned_students.count()
    assigned_students_count.short_description = 'Assigned Students'

    def responses_count(self, obj):
        return obj.responses.count()
    responses_count.short_description = 'Responses'


@admin.register(StudentQuizResponse)
class StudentQuizResponseAdmin(admin.ModelAdmin):
    list_display = ['student', 'quiz', 'selected_subject', 'submitted_at']
    list_filter = ['quiz', 'selected_subject', 'submitted_at']
    search_fields = ['student__name', 'student__rollno', 'quiz__title', 'selected_subject__name']
    ordering = ['-submitted_at']

    readonly_fields = ['submitted_at']

    def has_change_permission(self, request, obj=None):
        # Prevent editing of responses after submission
        return False
