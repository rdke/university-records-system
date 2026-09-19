from datetime import date
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction

from records.models import (
    Committee,
    Course,
    CourseMaterial,
    Department,
    DepartmentResearchArea,
    DisciplinaryRecord,
    Enrollment,
    Lecturer,
    LecturerExpertise,
    LecturerQualification,
    LecturerResearchInterest,
    ProjectFunding,
    ProjectOutcome,
    Programme,
    Publication,
    ResearchGroup,
    ResearchProject,
    Society,
    Staff,
    Student,
)


class Command(BaseCommand):
    help = 'Populate the database with university sample data'

    @transaction.atomic
    def handle(self, *args, **options):
        computing, _ = Department.objects.update_or_create(
            name='Computer Science',
            defaults={'faculty': 'Science and Engineering'},
        )
        mathematics, _ = Department.objects.update_or_create(
            name='Mathematics',
            defaults={'faculty': 'Science and Engineering'},
        )

        computer_science, _ = Programme.objects.update_or_create(
            name='Computer Science',
            defaults={'degree_awarded': 'BSc (Hons)', 'duration_years': 3},
        )
        data_science, _ = Programme.objects.update_or_create(
            name='Data Science',
            defaults={'degree_awarded': 'MSc', 'duration_years': 1},
        )

        lecturer_one, _ = Lecturer.objects.update_or_create(
            email='a.okafor@example.ac.uk',
            defaults={'name': 'Dr Amara Okafor', 'department': computing},
        )
        lecturer_two, _ = Lecturer.objects.update_or_create(
            email='j.whitfield@example.ac.uk',
            defaults={'name': 'Prof James Whitfield', 'department': computing},
        )
        lecturer_three, _ = Lecturer.objects.update_or_create(
            email='p.nair@example.ac.uk',
            defaults={'name': 'Dr Priya Nair', 'department': mathematics},
        )
        teaching_committee, _ = Committee.objects.get_or_create(
            name='Teaching and Learning Committee'
        )
        ethics_committee, _ = Committee.objects.get_or_create(
            name='Research Ethics Committee'
        )
        lecturer_one.committees.set([teaching_committee])
        lecturer_two.committees.set([teaching_committee, ethics_committee])
        lecturer_three.committees.set([ethics_committee])

        data_systems, _ = ResearchGroup.objects.update_or_create(
            name='Data Systems Group',
            defaults={'head_lecturer': lecturer_one},
        )
        machine_intelligence, _ = ResearchGroup.objects.update_or_create(
            name='Machine Intelligence Group',
            defaults={'head_lecturer': lecturer_two},
        )

        student_one, _ = Student.objects.update_or_create(
            email='a.turner@example.ac.uk',
            defaults={
                'name': 'Alice Turner',
                'birth_date': date(2004, 5, 12),
                'phone': '07700 900101',
                'programme': computer_science,
                'year_of_study': 3,
                'advisor': lecturer_one,
            },
        )
        student_two, _ = Student.objects.update_or_create(
            email='b.osei@example.ac.uk',
            defaults={
                'name': 'Ben Osei',
                'birth_date': date(2004, 1, 30),
                'phone': '07700 900102',
                'programme': computer_science,
                'year_of_study': 3,
                'advisor': lecturer_one,
            },
        )
        student_three, _ = Student.objects.update_or_create(
            email='d.kowalski@example.ac.uk',
            defaults={
                'name': 'Daniel Kowalski',
                'birth_date': date(2001, 3, 21),
                'programme': data_science,
                'year_of_study': 1,
                'advisor': lecturer_three,
            },
        )
        computing_society, _ = Society.objects.get_or_create(name='Computing Society')
        chess_society, _ = Society.objects.get_or_create(name='Chess Society')
        student_one.societies.set([computing_society, chess_society])
        student_two.societies.set([computing_society])

        Staff.objects.update_or_create(
            name='Fatima Hassan',
            defaults={
                'job_title': 'Department Administrator',
                'department': computing,
                'employment_type': Staff.EmploymentType.FULL_TIME,
                'salary': Decimal('29500.00'),
                'emergency_contact_name': 'Omar Hassan',
                'emergency_contact_phone': '07700 900201',
            },
        )
        Staff.objects.update_or_create(
            name='Gareth Price',
            defaults={
                'job_title': 'IT Technician',
                'department': computing,
                'employment_type': Staff.EmploymentType.PART_TIME,
                'contract_end_date': date(2027, 8, 31),
                'salary': Decimal('18200.00'),
                'emergency_contact_name': 'Sian Price',
                'emergency_contact_phone': '07700 900202',
            },
        )

        programming, _ = Course.objects.update_or_create(
            course_code='CS101',
            defaults={
                'name': 'Programming Fundamentals',
                'description': 'Introduction to programming in Python.',
                'department': computing,
                'level': 4,
                'credits': 20,
                'schedule': 'Monday 09:00',
            },
        )
        databases, _ = Course.objects.update_or_create(
            course_code='CS301',
            defaults={
                'name': 'Database Systems',
                'description': 'Relational design, SQL and transactions.',
                'department': computing,
                'level': 6,
                'credits': 20,
                'schedule': 'Wednesday 10:00',
            },
        )
        statistics, _ = Course.objects.update_or_create(
            course_code='MA501',
            defaults={
                'name': 'Statistics for Data Science',
                'department': mathematics,
                'level': 7,
                'credits': 30,
                'schedule': 'Friday 09:00',
            },
        )

        programming.programmes.set([computer_science])
        programming.lecturers.set([lecturer_one])
        databases.programmes.set([computer_science])
        databases.lecturers.set([lecturer_two])
        databases.prerequisites.set([programming])
        statistics.programmes.set([data_science])
        statistics.lecturers.set([lecturer_three])
        CourseMaterial.objects.get_or_create(
            course=databases,
            material='Lecture slides weeks 1-10',
        )

        Enrollment.objects.update_or_create(
            student=student_one,
            course=programming,
            defaults={'grade': Decimal('82.00')},
        )
        Enrollment.objects.update_or_create(
            student=student_two,
            course=programming,
            defaults={'grade': Decimal('65.00')},
        )
        Enrollment.objects.update_or_create(
            student=student_three,
            course=statistics,
            defaults={'grade': None},
        )

        project_one, _ = ResearchProject.objects.update_or_create(
            title='Scalable Query Processing',
            defaults={
                'lead_lecturer': lecturer_one,
                'research_group': data_systems,
            },
        )
        project_two, _ = ResearchProject.objects.update_or_create(
            title='Explainable Machine Learning',
            defaults={
                'lead_lecturer': lecturer_two,
                'research_group': machine_intelligence,
            },
        )
        project_one.students.set([student_one])
        project_two.students.set([student_one, student_two])
        ProjectFunding.objects.get_or_create(
            project=project_one,
            funding_source='EPSRC',
        )
        ProjectFunding.objects.get_or_create(
            project=project_two,
            funding_source='UKRI',
        )
        ProjectFunding.objects.get_or_create(
            project=project_two,
            funding_source='NHS England',
        )
        ProjectOutcome.objects.get_or_create(
            project=project_one,
            outcome='Open-source prototype query engine',
        )
        Publication.objects.get_or_create(
            lecturer=lecturer_one,
            project=project_one,
            title='Adaptive Indexing for Sensor Streams',
            published_date=date(2026, 3, 10),
        )

        LecturerQualification.objects.get_or_create(
            lecturer=lecturer_one,
            qualification='PhD Computer Science',
        )
        LecturerQualification.objects.get_or_create(
            lecturer=lecturer_three,
            qualification='PhD Statistics',
        )
        LecturerExpertise.objects.get_or_create(
            lecturer=lecturer_one,
            expertise='Databases',
        )
        LecturerResearchInterest.objects.get_or_create(
            lecturer=lecturer_two,
            research_interest='Machine Learning',
        )
        DepartmentResearchArea.objects.get_or_create(
            department=computing,
            research_area='Data Systems',
        )
        DisciplinaryRecord.objects.get_or_create(
            student=student_two,
            incident_date=date(2025, 11, 14),
            defaults={'description': 'Formal warning for coursework conduct.'},
        )

        self.stdout.write(self.style.SUCCESS('University sample data created.'))