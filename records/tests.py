from django.core.management import call_command
from django.test import TestCase
from django.urls import reverse

from .models import Course, Department, Lecturer, Programme, Staff, Student


class HomeViewTests(TestCase):
    def test_home_page_loads(self):
        response = self.client.get(reverse('home'))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'University Records')


class DatabaseQueryTests(TestCase):
    def test_query_page_offers_ten_queries(self):
        response = self.client.get(reverse('database-queries'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['options']), 10)

    def test_each_query_is_executed(self):
        query_names = [
            'students',
            'courses',
            'grades',
            'projects',
            'staff',
            'enrolled',
            'pending-grades',
            'prerequisites',
            'qualifications',
            'funding',
        ]

        for query_name in query_names:
            response = self.client.get(
                reverse('database-queries'),
                {'query': query_name},
            )

            self.assertEqual(response.status_code, 200)
            self.assertIsNotNone(response.context['results'])


class SeedDataTests(TestCase):
    def test_seed_command_populates_main_tables(self):
        call_command('seed_data')

        self.assertTrue(Department.objects.exists())
        self.assertTrue(Programme.objects.exists())
        self.assertTrue(Lecturer.objects.exists())
        self.assertTrue(Student.objects.exists())
        self.assertTrue(Staff.objects.exists())
        self.assertTrue(Course.objects.exists())
