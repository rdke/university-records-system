from datetime import date
from decimal import Decimal

from django.core.management import call_command
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .models import Course, Department, Enrollment, Lecturer, Programme, Student
from .queries import (
    completed_course_grades,
    courses_with_lecturers,
    courses_with_prerequisites,
    enrolled_students,
    funded_research_projects,
    lecturer_qualifications,
    pending_course_grades,
    projects_with_leads,
    staff_with_departments,
    students_with_programmes,
)


class PageTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'University Records')

    def test_all_database_query_pages_load(self):
        query_names = {
            'students': 'Students with programmes and advisors',
            'courses': 'Courses with departments and lecturers',
            'grades': 'Completed course grades',
            'projects': 'Research projects with leads and students',
            'staff': 'Staff grouped by department',
            'enrolled': 'Enrolled students by programme',
            'pending-grades': 'Course enrollments with pending grades',
            'prerequisites': 'Courses with prerequisites',
            'qualifications': 'Lecturer qualifications',
            'funding': 'Funded research projects',
        }

        for query_name, title in query_names.items():
            response = self.client.get(
                reverse('database-queries'),
                {'query': query_name},
            )

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response.context['results'])
            self.assertContains(response, title)


class DataTests(TestCase):
    def test_seed_command_creates_core_data(self):
        call_command('seed_data')

        self.assertTrue(Department.objects.exists())
        self.assertTrue(Programme.objects.exists())
        self.assertTrue(Lecturer.objects.exists())
        self.assertTrue(Student.objects.exists())
        self.assertTrue(Course.objects.exists())

    def test_grade_above_hundred_is_rejected(self):
        department = Department.objects.create(name='Computing', faculty='Science')
        programme = Programme.objects.create(
            name='Computer Science',
            degree_awarded='BSc',
            duration_years=3,
        )
        lecturer = Lecturer.objects.create(
            name='Alex Morgan',
            email='alex@example.ac.uk',
            department=department,
        )
        student = Student.objects.create(
            name='Sam Lee',
            birth_date=date(2004, 1, 1),
            email='sam@example.ac.uk',
            programme=programme,
            year_of_study=1,
            advisor=lecturer,
        )
        course = Course.objects.create(
            course_code='CS100',
            name='Introduction to Computing',
            department=department,
            level=4,
            credits=20,
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Enrollment.objects.create(
                    student=student,
                    course=course,
                    grade=Decimal('101.00'),
                )


class QueryTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command('seed_data')

    def test_students_with_programmes(self):
        self.assertEqual(
            list(students_with_programmes().values_list('name', flat=True)),
            ['Alice Turner', 'Ben Osei', 'Daniel Kowalski'],
        )

    def test_courses_with_lecturers(self):
        self.assertEqual(
            list(courses_with_lecturers().values_list('course_code', flat=True)),
            ['CS101', 'CS301', 'MA501'],
        )

    def test_completed_course_grades(self):
        self.assertEqual(
            list(
                completed_course_grades().values_list(
                    'student__name',
                    'course__course_code',
                    'grade',
                )
            ),
            [
                ('Alice Turner', 'CS101', Decimal('82.00')),
                ('Ben Osei', 'CS101', Decimal('65.00')),
            ],
        )

    def test_projects_with_leads(self):
        self.assertEqual(
            list(projects_with_leads().values_list('title', flat=True)),
            ['Explainable Machine Learning', 'Scalable Query Processing'],
        )

    def test_staff_with_departments(self):
        self.assertEqual(
            list(staff_with_departments().values_list('name', flat=True)),
            ['Fatima Hassan', 'Gareth Price'],
        )

    def test_enrolled_students(self):
        self.assertEqual(
            list(enrolled_students().values_list('name', flat=True)),
            ['Alice Turner', 'Ben Osei', 'Daniel Kowalski'],
        )

    def test_pending_course_grades(self):
        self.assertEqual(
            list(
                pending_course_grades().values_list(
                    'student__name',
                    'course__course_code',
                )
            ),
            [('Daniel Kowalski', 'MA501')],
        )

    def test_courses_with_prerequisites(self):
        self.assertEqual(
            list(courses_with_prerequisites().values_list('course_code', flat=True)),
            ['CS301'],
        )

    def test_lecturer_qualifications(self):
        self.assertEqual(
            list(
                lecturer_qualifications().values_list(
                    'lecturer__name',
                    'qualification',
                )
            ),
            [
                ('Dr Amara Okafor', 'PhD Computer Science'),
                ('Dr Priya Nair', 'PhD Statistics'),
            ],
        )

    def test_funded_research_projects(self):
        self.assertEqual(
            list(
                funded_research_projects().values_list(
                    'project__title',
                    'funding_source',
                )
            ),
            [
                ('Explainable Machine Learning', 'NHS England'),
                ('Explainable Machine Learning', 'UKRI'),
                ('Scalable Query Processing', 'EPSRC'),
            ],
        )