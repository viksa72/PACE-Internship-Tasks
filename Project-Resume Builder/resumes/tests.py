from django.test import TestCase, Client
from django.urls import reverse
from django.db.models import Q
from .models import Employee, Project, EmployeeProjectMapping
from .forms import EmployeeForm

class ResumeBuilderTestCase(TestCase):
    def setUp(self):
        # Setup test data
        self.client = Client()
        self.employee = Employee.objects.create(
            employee_id="PW-TEST",
            name="Test Employee",
            designation="Tester",
            professional_summary="Highly skilled at automated testing.",
            email="tester@test.com",
            phone="1234567890",
            technical_skills={"Languages": ["Python", "HTML", "CSS"]},
            education=[{"degree": "B.Sc.", "institution": "Univ", "year": "2020"}],
            certifications=[{"name": "Cert", "issuer": "Corp", "year": "2021"}]
        )
        self.project = Project.objects.create(
            name="Test System",
            technologies_used="Python, Django, SQLite",
            description="A project used for automated system verification."
        )
        self.mapping = EmployeeProjectMapping.objects.create(
            employee=self.employee,
            project=self.project,
            role_and_responsibilities="Wrote unit tests.\nValidated layouts.",
            order=1
        )

    def test_dashboard_view(self):
        """Test that the dashboard page loads successfully and lists the test employee."""
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Employee")
        self.assertContains(response, "PW-TEST")

    def test_search_view(self):
        """Test the search query parameter filter."""
        # Search for valid name
        response = self.client.get(reverse('dashboard'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "PW-TEST")

        # Search for non-existent name
        response = self.client.get(reverse('dashboard'), {'q': 'DoesNotExist'})
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "PW-TEST")

    def test_search_ajax(self):
        """Test the AJAX search suggestions endpoint."""
        response = self.client.get(reverse('search_ajax'), {'q': 'Test'})
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data['results']), 1)
        self.assertEqual(data['results'][0]['name'], "Test Employee")

    def test_employee_detail_view(self):
        """Test that the profile detail page loads with details and mappings."""
        response = self.client.get(reverse('employee_detail', args=[self.employee.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Test Employee")
        self.assertContains(response, "Test System")

    def test_pdf_generation(self):
        """Test that the PDF generator generates a valid PDF download response."""
        response = self.client.get(reverse('generate_resume_pdf', args=[self.employee.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Content-Type'], 'application/pdf')
        self.assertTrue(response.headers['Content-Disposition'].startswith('attachment; filename='))
        # Ensure there is actual PDF binary data
        pdf_content = b"".join(response.streaming_content)
        self.assertTrue(len(pdf_content) > 1000)

    def test_employee_form_validation(self):
        """Test form validation for skills and education formats."""
        # Test missing colon in skills
        form_data = {
            'employee_id': 'PW-NEW',
            'name': 'New Guy',
            'designation': 'Junior Developer',
            'email': 'new@pacewisdom.com',
            'phone': '9876543210',
            'skills_text': 'Missing colon line here',
            'education_text': 'Degree | Institution | 2020',
            'certifications_text': 'Cert | Issuer | 2021',
            'professional_summary': 'Enthusiastic developer.',
        }
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('skills_text', form.errors)

        # Test missing pipe in education
        form_data['skills_text'] = 'Languages: Python, JS'
        form_data['education_text'] = 'Missing pipe separator here'
        form = EmployeeForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('education_text', form.errors)



