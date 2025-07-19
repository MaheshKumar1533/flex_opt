from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.utils import timezone
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
import csv
import io
from django.contrib.auth.hashers import make_password

from .models import Student, Quiz, Subject, StudentQuizResponse


def student_login(request):
    """Student login view"""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            student = Student.objects.get(email=email)
            if student.check_password(password):
                # Store student info in session
                request.session['student_id'] = student.id
                request.session['student_name'] = student.name
                return redirect('student_dashboard')
            else:
                messages.error(request, 'Invalid email or password.')
        except Student.DoesNotExist:
            messages.error(request, 'Invalid email or password.')

    return render(request, 'elective/login.html')


def student_logout(request):
    """Student logout view"""
    request.session.flush()
    messages.success(request, 'You have been logged out successfully.')
    return redirect('student_login')


def student_required(view_func):
    """Decorator to ensure student is logged in"""
    def wrapper(request, *args, **kwargs):
        if 'student_id' not in request.session:
            return redirect('student_login')
        return view_func(request, *args, **kwargs)
    return wrapper


@student_required
def student_dashboard(request):
    """Student dashboard showing assigned quizzes"""
    student_id = request.session['student_id']
    student = get_object_or_404(Student, id=student_id)

    # Get assigned and available quizzes
    assigned_quizzes = student.assigned_quizzes.filter(
        is_active=True,
        start_time__lte=timezone.now()
    )

    # Check which quizzes the student has already completed
    completed_quiz_ids = student.quiz_responses.values_list('quiz_id', flat=True)
    available_quizzes = assigned_quizzes.exclude(id__in=completed_quiz_ids)

    context = {
        'student': student,
        'available_quizzes': available_quizzes,
        'completed_responses': student.quiz_responses.select_related('quiz', 'selected_subject')
    }

    return render(request, 'elective/student_dashboard.html', context)


@student_required
def quiz_detail(request, quiz_id):
    """Quiz detail page where student can select subjects"""
    student_id = request.session['student_id']
    student = get_object_or_404(Student, id=student_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)

    # Check if student is assigned to this quiz
    if not quiz.assigned_students.filter(id=student_id).exists():
        messages.error(request, 'You are not assigned to this quiz.')
        return redirect('student_dashboard')

    # Check if student has already submitted response for this quiz
    if StudentQuizResponse.objects.filter(student=student, quiz=quiz).exists():
        messages.info(request, 'You have already submitted your response for this quiz.')
        return redirect('student_dashboard')

    # Check if quiz is available
    if not quiz.is_available():
        messages.error(request, 'This quiz is not currently available.')
        return redirect('student_dashboard')

    subjects = quiz.subjects.all().order_by('code')

    context = {
        'student': student,
        'quiz': quiz,
        'subjects': subjects,
    }

    return render(request, 'elective/quiz_detail.html', context)


@student_required
@csrf_exempt
def submit_quiz_response(request, quiz_id):
    """Submit quiz response via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request method'})

    student_id = request.session['student_id']
    student = get_object_or_404(Student, id=student_id)
    quiz = get_object_or_404(Quiz, id=quiz_id)

    try:
        data = json.loads(request.body)
        subject_id = data.get('subject_id')

        # Validate subject
        subject = get_object_or_404(Subject, id=subject_id)

        # Check if subject is in this quiz
        if not quiz.subjects.filter(id=subject_id).exists():
            return JsonResponse({'success': False, 'error': 'Invalid subject selection'})

        # Check if student already submitted response
        if StudentQuizResponse.objects.filter(student=student, quiz=quiz).exists():
            return JsonResponse({'success': False, 'error': 'You have already submitted your response'})

        # Check if subject is full
        if subject.is_full():
            return JsonResponse({'success': False, 'error': 'This subject is already full'})

        # Create response and update subject count
        response = StudentQuizResponse.objects.create(
            student=student,
            quiz=quiz,
            selected_subject=subject
        )

        # Update subject count
        subject.current_count += 1
        subject.save()

        # Send real-time update via WebSocket
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f'quiz_{quiz_id}',
            {
                'type': 'subject_update',
                'data': {
                    'subject_id': subject.id,
                    'current_count': subject.current_count,
                    'is_full': subject.is_full()
                }
            }
        )

        return JsonResponse({
            'success': True,
            'message': f'Successfully selected {subject.name}',
            'redirect_url': '/dashboard/'
        })

    except json.JSONDecodeError:
        return JsonResponse({'success': False, 'error': 'Invalid JSON data'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@staff_member_required
def add_students(request):
    """Add students individually or via CSV upload"""
    success_count = 0
    error_messages = []

    if request.method == 'POST':
        if 'csv_file' in request.FILES:
            # Handle CSV upload
            csv_file = request.FILES['csv_file']

            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'Please upload a valid CSV file.')
                return render(request, 'elective/add_students.html')

            try:
                # Read CSV file
                file_data = csv_file.read().decode('utf-8')
                io_string = io.StringIO(file_data)
                csv_reader = csv.DictReader(io_string)

                # Expected CSV columns: name,rollno,email,dept,year,section,password
                required_fields = ['name', 'rollno', 'email', 'dept', 'year', 'section']

                for row_num, row in enumerate(csv_reader, start=2):  # Start at 2 to account for header
                    try:
                        # Validate required fields
                        missing_fields = [field for field in required_fields if not row.get(field, '').strip()]
                        if missing_fields:
                            error_messages.append(f'Row {row_num}: Missing required fields: {", ".join(missing_fields)}')
                            continue

                        # Clean and validate data
                        name = row['name'].strip()
                        rollno = row['rollno'].strip()
                        email = row['email'].strip().lower()
                        dept = row['dept'].strip()
                        year = row['year'].strip()
                        section = row['section'].strip()
                        password = row.get('password', '').strip() or 'password123'  # Default password

                        # Validate year is numeric
                        try:
                            year_int = int(year)
                            if year_int < 1 or year_int > 10:
                                error_messages.append(f'Row {row_num}: Year must be between 1-10')
                                continue
                        except ValueError:
                            error_messages.append(f'Row {row_num}: Year must be a number')
                            continue

                        # Check for duplicates
                        if Student.objects.filter(Q(email=email) | Q(rollno=rollno)).exists():
                            error_messages.append(f'Row {row_num}: Student with email {email} or roll number {rollno} already exists')
                            continue

                        # Create student
                        student = Student.objects.create(
                            name=name,
                            rollno=rollno,
                            email=email,
                            password=make_password(password),
                            dept=dept,
                            year=year_int,
                            section=section
                        )
                        success_count += 1

                    except Exception as e:
                        error_messages.append(f'Row {row_num}: Error processing student - {str(e)}')

                if success_count > 0:
                    messages.success(request, f'Successfully added {success_count} students!')
                if error_messages:
                    for error in error_messages[:10]:  # Show first 10 errors
                        messages.error(request, error)
                    if len(error_messages) > 10:
                        messages.warning(request, f'... and {len(error_messages) - 10} more errors.')

            except Exception as e:
                messages.error(request, f'Error processing CSV file: {str(e)}')

        else:
            # Handle individual student addition
            name = request.POST.get('name', '').strip()
            rollno = request.POST.get('rollno', '').strip()
            email = request.POST.get('email', '').strip().lower()
            dept = request.POST.get('dept', '').strip()
            year = request.POST.get('year', '').strip()
            section = request.POST.get('section', '').strip()
            password = request.POST.get('password', '').strip() or 'password123'

            # Validate required fields
            if not all([name, rollno, email, dept, year, section]):
                messages.error(request, 'All fields are required.')
            else:
                try:
                    year_int = int(year)
                    if year_int < 1 or year_int > 10:
                        messages.error(request, 'Year must be between 1-10.')
                    elif Student.objects.filter(Q(email=email) | Q(rollno=rollno)).exists():
                        messages.error(request, 'Student with this email or roll number already exists.')
                    else:
                        student = Student.objects.create(
                            name=name,
                            rollno=rollno,
                            email=email,
                            password=make_password(password),
                            dept=dept,
                            year=year_int,
                            section=section
                        )
                        messages.success(request, f'Student {name} added successfully!')
                        return redirect('add_students')  # Redirect to clear form
                except ValueError:
                    messages.error(request, 'Year must be a valid number.')
                except Exception as e:
                    messages.error(request, f'Error adding student: {str(e)}')

    # Get some statistics for the template
    total_students = Student.objects.count()
    departments = Student.objects.values_list('dept', flat=True).distinct().order_by('dept')
    years = Student.objects.values_list('year', flat=True).distinct().order_by('year')
    sections = Student.objects.values_list('section', flat=True).distinct().order_by('section')

    context = {
        'total_students': total_students,
        'departments': departments,
        'years': years,
        'sections': sections,
    }

    return render(request, 'elective/add_students.html', context)


@staff_member_required
def admin_dashboard(request):
    """Admin dashboard for managing quizzes"""
    quizzes = Quiz.objects.all().order_by('-created_at')
    students = Student.objects.all().order_by('rollno')
    subjects = Subject.objects.all().order_by('code')

    # Create quiz-wise subject overview
    quiz_subject_overview = []
    for quiz in quizzes:
        quiz_subjects = quiz.subjects.all().order_by('code')
        quiz_data = {
            'quiz': quiz,
            'subjects': [],
            'total_capacity': 0,
            'total_filled': 0,
        }

        for subject in quiz_subjects:
            # Get current selections for this subject in this quiz
            selections = subject.selected_by.filter(quiz=quiz).count()
            availability = subject.max_limit - selections

            subject_data = {
                'subject': subject,
                'current_selections': selections,
                'availability': availability,
                'utilization_percent': round((selections / subject.max_limit) * 100, 1) if subject.max_limit > 0 else 0,
                'is_full': selections >= subject.max_limit,
            }

            quiz_data['subjects'].append(subject_data)
            quiz_data['total_capacity'] += subject.max_limit
            quiz_data['total_filled'] += selections

        if quiz_data['total_capacity'] > 0:
            quiz_data['overall_utilization'] = round((quiz_data['total_filled'] / quiz_data['total_capacity']) * 100, 1)
        else:
            quiz_data['overall_utilization'] = 0

        quiz_subject_overview.append(quiz_data)

    context = {
        'quizzes': quizzes,
        'students': students,
        'subjects': subjects,
        'quiz_subject_overview': quiz_subject_overview,
    }

    return render(request, 'elective/admin_dashboard.html', context)


@staff_member_required
def create_quiz(request):
    """Create a new quiz"""
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        start_time = request.POST.get('start_time')
        end_time = request.POST.get('end_time')
        subject_ids = request.POST.getlist('subjects')

        # Create quiz
        quiz = Quiz.objects.create(
            title=title,
            description=description,
            start_time=start_time if start_time else timezone.now(),
            end_time=end_time if end_time else None,
        )

        # Add subjects
        if subject_ids:
            quiz.subjects.set(subject_ids)

        messages.success(request, f'Quiz "{title}" created successfully.')
        return redirect('admin_dashboard')

    subjects = Subject.objects.all().order_by('code')
    context = {'subjects': subjects}

    return render(request, 'elective/create_quiz.html', context)


@staff_member_required
def assign_students(request, quiz_id):
    """Assign students to a quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)

    if request.method == 'POST':
        # Filter students based on criteria
        dept = request.POST.get('dept')
        year = request.POST.get('year')
        section = request.POST.get('section')
        student_ids = request.POST.getlist('students')

        if student_ids:
            # Assign specific students
            quiz.assigned_students.set(student_ids)
        else:
            # Filter students by criteria
            students = Student.objects.all()
            if dept:
                students = students.filter(dept=dept)
            if year:
                students = students.filter(year=year)
            if section:
                students = students.filter(section=section)

            quiz.assigned_students.set(students)

        messages.success(request, f'Students assigned to quiz "{quiz.title}" successfully.')
        return redirect('admin_dashboard')

    # Get filter options
    departments = Student.objects.values_list('dept', flat=True).distinct()
    years = Student.objects.values_list('year', flat=True).distinct()
    sections = Student.objects.values_list('section', flat=True).distinct()
    students = Student.objects.all().order_by('rollno')

    context = {
        'quiz': quiz,
        'departments': departments,
        'years': sorted(years),
        'sections': sections,
        'students': students,
        'assigned_students': quiz.assigned_students.all(),
    }

    return render(request, 'elective/assign_students.html', context)


@staff_member_required
def quiz_results(request, quiz_id):
    """View quiz results"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    responses = quiz.responses.select_related('student', 'selected_subject').order_by('-submitted_at')

    # Subject-wise statistics
    subject_stats = {}
    for subject in quiz.subjects.all():
        subject_responses = responses.filter(selected_subject=subject)
        subject_stats[subject] = {
            'count': subject_responses.count(),
            'students': subject_responses.values_list('student__name', 'student__rollno')
        }

    context = {
        'quiz': quiz,
        'responses': responses,
        'subject_stats': subject_stats,
        'total_responses': responses.count(),
        'total_assigned': quiz.assigned_students.count(),
    }

    return render(request, 'elective/quiz_results.html', context)


@staff_member_required
def quiz_non_attendees(request, quiz_id):
    """View students who did not attend the quiz"""
    quiz = get_object_or_404(Quiz, id=quiz_id)
    
    # Get all assigned students
    assigned_students = quiz.assigned_students.all()
    
    # Get students who have submitted responses
    responded_student_ids = quiz.responses.values_list('student_id', flat=True)
    
    # Get students who didn't attend (assigned but no response)
    non_attendees = assigned_students.exclude(id__in=responded_student_ids).order_by('rollno')
    
    # Group non-attendees by department for better organization
    non_attendees_by_dept = {}
    for student in non_attendees:
        dept = student.dept
        if dept not in non_attendees_by_dept:
            non_attendees_by_dept[dept] = []
        non_attendees_by_dept[dept].append(student)
    
    # Calculate statistics
    total_assigned = assigned_students.count()
    total_responded = len(responded_student_ids)
    total_non_attendees = non_attendees.count()
    response_rate = round((total_responded / total_assigned * 100), 1) if total_assigned > 0 else 0
    non_attendance_rate = round((total_non_attendees / total_assigned * 100), 1) if total_assigned > 0 else 0

    context = {
        'quiz': quiz,
        'non_attendees': non_attendees,
        'non_attendees_by_dept': non_attendees_by_dept,
        'total_assigned': total_assigned,
        'total_responded': total_responded,
        'total_non_attendees': total_non_attendees,
        'response_rate': response_rate,
        'non_attendance_rate': non_attendance_rate,
    }

    return render(request, 'elective/quiz_non_attendees.html', context)


@staff_member_required
def subject_overview(request):
    """Detailed quiz-wise subject overview page"""
    quizzes = Quiz.objects.all().order_by('-created_at')

    # Build comprehensive overview data
    overview_data = []
    overall_stats = {
        'total_quizzes': quizzes.count(),
        'total_subjects': 0,
        'total_capacity': 0,
        'total_filled': 0,
        'active_quizzes': 0,
    }

    for quiz in quizzes:
        if quiz.is_active:
            overall_stats['active_quizzes'] += 1

        quiz_subjects = quiz.subjects.all().order_by('code')
        quiz_data = {
            'quiz': quiz,
            'subjects': [],
            'stats': {
                'total_capacity': 0,
                'total_filled': 0,
                'total_subjects': quiz_subjects.count(),
                'full_subjects': 0,
                'empty_subjects': 0,
            }
        }

        for subject in quiz_subjects:
            selections = subject.selected_by.filter(quiz=quiz).count()
            availability = subject.max_limit - selections
            utilization = (selections / subject.max_limit * 100) if subject.max_limit > 0 else 0

            subject_info = {
                'subject': subject,
                'current_selections': selections,
                'availability': availability,
                'utilization_percent': round(utilization, 1),
                'is_full': selections >= subject.max_limit,
                'is_empty': selections == 0,
            }

            quiz_data['subjects'].append(subject_info)
            quiz_data['stats']['total_capacity'] += subject.max_limit
            quiz_data['stats']['total_filled'] += selections

            if selections >= subject.max_limit:
                quiz_data['stats']['full_subjects'] += 1
            if selections == 0:
                quiz_data['stats']['empty_subjects'] += 1

        # Calculate quiz utilization
        if quiz_data['stats']['total_capacity'] > 0:
            quiz_data['stats']['utilization_percent'] = round(
                (quiz_data['stats']['total_filled'] / quiz_data['stats']['total_capacity']) * 100, 1
            )
        else:
            quiz_data['stats']['utilization_percent'] = 0

        overview_data.append(quiz_data)

        # Add to overall stats
        overall_stats['total_subjects'] += quiz_data['stats']['total_subjects']
        overall_stats['total_capacity'] += quiz_data['stats']['total_capacity']
        overall_stats['total_filled'] += quiz_data['stats']['total_filled']

    # Calculate overall utilization
    if overall_stats['total_capacity'] > 0:
        overall_stats['utilization_percent'] = round(
            (overall_stats['total_filled'] / overall_stats['total_capacity']) * 100, 1
        )
    else:
        overall_stats['utilization_percent'] = 0

    context = {
        'overview_data': overview_data,
        'overall_stats': overall_stats,
    }

    return render(request, 'elective/subject_overview.html', context)


@staff_member_required
def get_quiz_stats_api(request):
    """API endpoint to get real-time quiz statistics"""
    quizzes = Quiz.objects.all()

    stats = {
        'total_quizzes': quizzes.count(),
        'active_quizzes': quizzes.filter(is_active=True).count(),
        'total_responses': 0,
        'total_capacity': 0,
        'total_filled': 0,
        'quiz_details': []
    }

    for quiz in quizzes:
        quiz_responses = quiz.responses.count()
        quiz_capacity = sum(subject.max_limit for subject in quiz.subjects.all())
        quiz_filled = sum(subject.selected_by.filter(quiz=quiz).count() for subject in quiz.subjects.all())

        quiz_detail = {
            'id': quiz.id,
            'title': quiz.title,
            'is_active': quiz.is_active,
            'responses': quiz_responses,
            'capacity': quiz_capacity,
            'filled': quiz_filled,
            'utilization': round((quiz_filled / quiz_capacity * 100), 1) if quiz_capacity > 0 else 0
        }

        stats['quiz_details'].append(quiz_detail)
        stats['total_responses'] += quiz_responses
        stats['total_capacity'] += quiz_capacity
        stats['total_filled'] += quiz_filled

    if stats['total_capacity'] > 0:
        stats['overall_utilization'] = round((stats['total_filled'] / stats['total_capacity'] * 100), 1)
    else:
        stats['overall_utilization'] = 0

    return JsonResponse(stats)


def home(request):
    """Home page redirect"""
    if 'student_id' in request.session:
        return redirect('student_dashboard')
    return redirect('student_login')
