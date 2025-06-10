from django.core.management.base import BaseCommand
from django.utils import timezone
from elective.models import Student, Subject, Quiz
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data for different scenarios'

    def add_arguments(self, parser):
        parser.add_argument(
            '--scenario',
            type=str,
            default='electives',
            choices=['electives', 'training', 'courses', 'all'],
            help='Choose the scenario to populate: electives, training, courses, or all'
        )

    def handle(self, *args, **options):
        scenario = options['scenario']
        self.stdout.write(f'Creating sample data for scenario: {scenario}...')

        # Create Students first (common for all scenarios)
        self.create_students()

        if scenario == 'electives' or scenario == 'all':
            self.create_elective_scenario()

        if scenario == 'training' or scenario == 'all':
            self.create_training_scenario()

        if scenario == 'courses' or scenario == 'all':
            self.create_course_scenario()

        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data!')
        )
        self.display_credentials()

    def create_students(self):
        """Create sample students"""
        students_data = [
            # Computer Science Students
            {'name': 'Alice Johnson', 'rollno': 'CS2021001', 'email': 'alice.johnson@student.edu', 'dept': 'Computer Science', 'year': 3, 'section': 'A'},
            {'name': 'Bob Smith', 'rollno': 'CS2021002', 'email': 'bob.smith@student.edu', 'dept': 'Computer Science', 'year': 3, 'section': 'A'},
            {'name': 'Charlie Brown', 'rollno': 'CS2021003', 'email': 'charlie.brown@student.edu', 'dept': 'Computer Science', 'year': 3, 'section': 'B'},
            {'name': 'Diana Prince', 'rollno': 'CS2021004', 'email': 'diana.prince@student.edu', 'dept': 'Computer Science', 'year': 3, 'section': 'B'},
            {'name': 'Ethan Hunt', 'rollno': 'CS2021005', 'email': 'ethan.hunt@student.edu', 'dept': 'Computer Science', 'year': 3, 'section': 'A'},
            {'name': 'Fiona Green', 'rollno': 'CS2021006', 'email': 'fiona.green@student.edu', 'dept': 'Computer Science', 'year': 3, 'section': 'B'},

            # IT Students
            {'name': 'George Washington', 'rollno': 'IT2021001', 'email': 'george.washington@student.edu', 'dept': 'Information Technology', 'year': 3, 'section': 'A'},
            {'name': 'Hannah Montana', 'rollno': 'IT2021002', 'email': 'hannah.montana@student.edu', 'dept': 'Information Technology', 'year': 3, 'section': 'A'},
            {'name': 'Ian Fleming', 'rollno': 'IT2021003', 'email': 'ian.fleming@student.edu', 'dept': 'Information Technology', 'year': 3, 'section': 'B'},
            {'name': 'Julia Roberts', 'rollno': 'IT2021004', 'email': 'julia.roberts@student.edu', 'dept': 'Information Technology', 'year': 3, 'section': 'B'},

            # ECE Students
            {'name': 'Kevin Hart', 'rollno': 'ECE2021001', 'email': 'kevin.hart@student.edu', 'dept': 'Electronics', 'year': 3, 'section': 'A'},
            {'name': 'Luna Lovegood', 'rollno': 'ECE2021002', 'email': 'luna.lovegood@student.edu', 'dept': 'Electronics', 'year': 3, 'section': 'A'},
            {'name': 'Mike Tyson', 'rollno': 'ECE2021003', 'email': 'mike.tyson@student.edu', 'dept': 'Electronics', 'year': 3, 'section': 'B'},
            {'name': 'Nina Simone', 'rollno': 'ECE2021004', 'email': 'nina.simone@student.edu', 'dept': 'Electronics', 'year': 3, 'section': 'B'},

            # ME Students
            {'name': 'Oscar Wilde', 'rollno': 'ME2021001', 'email': 'oscar.wilde@student.edu', 'dept': 'Mechanical', 'year': 3, 'section': 'A'},
            {'name': 'Peter Parker', 'rollno': 'ME2021002', 'email': 'peter.parker@student.edu', 'dept': 'Mechanical', 'year': 3, 'section': 'A'},
            {'name': 'Quinn Fabray', 'rollno': 'ME2021003', 'email': 'quinn.fabray@student.edu', 'dept': 'Mechanical', 'year': 3, 'section': 'B'},
            {'name': 'Rachel Green', 'rollno': 'ME2021004', 'email': 'rachel.green@student.edu', 'dept': 'Mechanical', 'year': 3, 'section': 'B'},

            # Civil Students
            {'name': 'Sam Wilson', 'rollno': 'CE2021001', 'email': 'sam.wilson@student.edu', 'dept': 'Civil', 'year': 3, 'section': 'A'},
            {'name': 'Tina Turner', 'rollno': 'CE2021002', 'email': 'tina.turner@student.edu', 'dept': 'Civil', 'year': 3, 'section': 'A'},
        ]

        for student_data in students_data:
            student, created = Student.objects.get_or_create(
                rollno=student_data['rollno'],
                defaults=student_data
            )
            if created:
                # Set default password as 'password123'
                student.set_password('password123')
                student.save()
                self.stdout.write(f'Created student: {student.rollno} - {student.name}')

    def create_elective_scenario(self):
        """Create open elective subjects and quiz"""
        elective_subjects = [
            {'name': 'Machine Learning Fundamentals', 'code': 'CS501', 'max_limit': 30, 'description': 'Introduction to ML algorithms and applications'},
            {'name': 'Web Development with React', 'code': 'CS502', 'max_limit': 25, 'description': 'Modern frontend development using React framework'},
            {'name': 'Data Structures & Algorithms', 'code': 'CS503', 'max_limit': 35, 'description': 'Advanced DSA concepts and problem solving'},
            {'name': 'Mobile App Development', 'code': 'CS504', 'max_limit': 20, 'description': 'Cross-platform mobile development'},
            {'name': 'Cybersecurity Basics', 'code': 'CS505', 'max_limit': 28, 'description': 'Network security and ethical hacking'},
            {'name': 'Cloud Computing', 'code': 'CS506', 'max_limit': 22, 'description': 'AWS, Azure, and cloud architecture'},
        ]

        subjects = []
        for subject_data in elective_subjects:
            subject, created = Subject.objects.get_or_create(
                code=subject_data['code'],
                defaults=subject_data
            )
            if created:
                self.stdout.write(f'Created elective subject: {subject.code} - {subject.name}')
            subjects.append(subject)

        # Create Elective Quiz
        quiz, created = Quiz.objects.get_or_create(
            title='Open Elective Selection - Spring 2025',
            defaults={
                'description': 'Select your preferred open elective subject for the Spring 2025 semester. You can only select one subject.',
                'start_time': timezone.now(),
                'end_time': None,
                'is_active': True,
            }
        )

        if created:
            quiz.subjects.set(subjects)
            # Assign CS and IT students to elective quiz
            cs_it_students = Student.objects.filter(dept__in=['Computer Science', 'Information Technology'])
            quiz.assigned_students.set(cs_it_students)
            self.stdout.write(f'Created elective quiz: {quiz.title}')

    def create_training_scenario(self):
        """Create training programs and quiz"""
        training_subjects = [
            {'name': 'Java Full Stack Development', 'code': 'TRAIN001', 'max_limit': 40, 'description': 'Complete Java development with Spring Boot and React'},
            {'name': '.NET Core Development', 'code': 'TRAIN002', 'max_limit': 40, 'description': 'Microsoft .NET Core web development'},
            {'name': 'Database Administration', 'code': 'TRAIN003', 'max_limit': 80, 'description': 'MySQL, PostgreSQL, and MongoDB administration'},
            {'name': 'Python Data Science', 'code': 'TRAIN004', 'max_limit': 35, 'description': 'Python for data analysis and machine learning'},
            {'name': 'DevOps & Cloud', 'code': 'TRAIN005', 'max_limit': 30, 'description': 'Docker, Kubernetes, and AWS deployment'},
            {'name': 'Frontend Development', 'code': 'TRAIN006', 'max_limit': 45, 'description': 'Modern frontend with Vue.js and Angular'},
        ]

        subjects = []
        for subject_data in training_subjects:
            subject, created = Subject.objects.get_or_create(
                code=subject_data['code'],
                defaults=subject_data
            )
            if created:
                self.stdout.write(f'Created training program: {subject.code} - {subject.name}')
            subjects.append(subject)

        # Create Training Quiz
        quiz, created = Quiz.objects.get_or_create(
            title='Corporate Training Program Selection - 2025',
            defaults={
                'description': 'Choose your training program for professional development. Limited seats available!',
                'start_time': timezone.now(),
                'end_time': timezone.now() + timezone.timedelta(days=7),
                'is_active': True,
            }
        )

        if created:
            quiz.subjects.set(subjects)
            # Assign all students to training quiz
            all_students = Student.objects.all()
            quiz.assigned_students.set(all_students)
            self.stdout.write(f'Created training quiz: {quiz.title}')

    def create_course_scenario(self):
        """Create specialized course subjects and quiz"""
        course_subjects = [
            {'name': 'Advanced Algorithms', 'code': 'CS601', 'max_limit': 25, 'description': 'Advanced algorithmic techniques and complexity analysis'},
            {'name': 'Computer Graphics', 'code': 'CS602', 'max_limit': 20, 'description': '3D graphics programming and visualization'},
            {'name': 'Network Programming', 'code': 'CS603', 'max_limit': 30, 'description': 'Socket programming and distributed systems'},
            {'name': 'Artificial Intelligence', 'code': 'CS604', 'max_limit': 35, 'description': 'AI algorithms and neural networks'},
            {'name': 'Software Architecture', 'code': 'CS605', 'max_limit': 28, 'description': 'Design patterns and system architecture'},
        ]

        subjects = []
        for subject_data in course_subjects:
            subject, created = Subject.objects.get_or_create(
                code=subject_data['code'],
                defaults=subject_data
            )
            if created:
                self.stdout.write(f'Created course: {subject.code} - {subject.name}')
            subjects.append(subject)

        # Create Course Quiz
        quiz, created = Quiz.objects.get_or_create(
            title='Specialized Course Selection - Fall 2025',
            defaults={
                'description': 'Select specialized courses for advanced learning. Prerequisites may apply.',
                'start_time': timezone.now(),
                'end_time': timezone.now() + timezone.timedelta(days=5),
                'is_active': True,
            }
        )

        if created:
            quiz.subjects.set(subjects)
            # Assign only CS students to specialized courses
            cs_students = Student.objects.filter(dept='Computer Science')
            quiz.assigned_students.set(cs_students)
            self.stdout.write(f'Created course quiz: {quiz.title}')

    def display_credentials(self):
        """Display login credentials"""
        self.stdout.write('\n' + '='*50)
        self.stdout.write('SAMPLE LOGIN CREDENTIALS:')
        self.stdout.write('='*50)
        self.stdout.write('🔑 Admin Access:')
        self.stdout.write('   Username: admin')
        self.stdout.write('   Password: admin123')
        self.stdout.write('   URL: http://localhost:8000/admin-dashboard/')
        self.stdout.write('')
        self.stdout.write('👨‍🎓 Student Access (password: password123):')
        self.stdout.write('   alice.johnson@student.edu (CS - Section A)')
        self.stdout.write('   bob.smith@student.edu (CS - Section A)')
        self.stdout.write('   george.washington@student.edu (IT - Section A)')
        self.stdout.write('   kevin.hart@student.edu (ECE - Section A)')
        self.stdout.write('   oscar.wilde@student.edu (ME - Section A)')
        self.stdout.write('   URL: http://localhost:8000/')
        self.stdout.write('='*50)

        # Display quiz information
        quizzes = Quiz.objects.all()
        if quizzes:
            self.stdout.write('\n📋 AVAILABLE QUIZZES:')
            for quiz in quizzes:
                self.stdout.write(f'   • {quiz.title}')
                self.stdout.write(f'     Subjects: {quiz.subjects.count()}, Students: {quiz.assigned_students.count()}')
        self.stdout.write('')
