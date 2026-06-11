from django.db import models

class Employee(models.Model):
    employee_id = models.CharField(max_length=50, unique=True, verbose_name="Employee ID")
    name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    professional_summary = models.TextField(verbose_name="Professional Summary")
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    
    # JSON field for technical skills
    # Expected structure: {"Programming and Scripting": ["JS", "PHP"], "Frameworks": ["Django"]}
    technical_skills = models.JSONField(default=dict, blank=True, verbose_name="Technical Skills")
    
    # JSON fields for Education and Certifications
    # Expected structure: [{"degree": "B.E.", "institution": "VTU", "year": "2020"}]
    education = models.JSONField(default=list, blank=True, verbose_name="Education")
    # Expected structure: [{"name": "AWS Certified Developer", "issuer": "Amazon", "year": "2021"}]
    certifications = models.JSONField(default=list, blank=True, verbose_name="Certifications")

    def __str__(self):
        return f"{self.name} ({self.employee_id})"

class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    technologies_used = models.CharField(max_length=500, verbose_name="Technologies Used (comma separated)")
    client = models.CharField(max_length=200, blank=True, null=True)
    duration = models.CharField(max_length=100, blank=True, null=True, help_text="e.g. 3 Months, Jan 2021 - Apr 2021")

    def __str__(self):
        return self.name

class EmployeeProjectMapping(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name="project_mappings")
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name="employee_mappings")
    role_and_responsibilities = models.TextField(
        verbose_name="Role & Responsibilities",
        help_text="Enter roles/responsibilities, one per line (each will become a bullet point)"
    )
    duration = models.CharField(
        max_length=100, 
        blank=True, 
        null=True, 
        help_text="Override project duration if different for this employee"
    )
    client = models.CharField(
        max_length=200, 
        blank=True, 
        null=True, 
        help_text="Override project client if different for this employee"
    )
    order = models.PositiveIntegerField(
        default=0, 
        help_text="Display order in the resume (lower values first)"
    )

    class Meta:
        ordering = ['order', 'id']
        unique_together = ('employee', 'project')

    def __str__(self):
        return f"{self.employee.name} - {self.project.name}"

