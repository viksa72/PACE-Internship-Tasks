import json
from django import forms
from .models import Employee, Project, EmployeeProjectMapping

class EmployeeForm(forms.ModelForm):
    # Form fields that will present JSON fields as human-readable text areas
    skills_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5, 'placeholder': 'Category Name: Skill 1, Skill 2, Skill 3\nExample:\nFrameworks: Vue js, Laravel, Django\nOperating System: Linux, Windows'}),
        required=False,
        label="Technical Skills",
        help_text="Enter one category per line, followed by a colon, then comma-separated skills."
    )
    education_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Degree/Course | Institution/University | Year\nExample:\nB.E. Computer Science | VTU | 2020\nHigher Secondary | CBSE | 2016'}),
        required=False,
        label="Education",
        help_text="Enter one entry per line, using '|' as a separator."
    )
    certifications_text = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4, 'placeholder': 'Certification Name | Issuing Organization | Year\nExample:\nAWS Certified Developer | Amazon Web Services | 2021'}),
        required=False,
        label="Certifications",
        help_text="Enter one certification per line, using '|' as a separator."
    )

    class Meta:
        model = Employee
        fields = ['employee_id', 'name', 'designation', 'email', 'phone', 'address', 'professional_summary']
        widgets = {
            'professional_summary': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter professional summary...'}),
            'address': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter address...'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Pre-populate the text areas with formatted values if editing an existing instance
        if self.instance and self.instance.pk:
            # Format skills
            skills_lines = []
            if isinstance(self.instance.technical_skills, dict):
                for cat, skills in self.instance.technical_skills.items():
                    if isinstance(skills, list):
                        skills_str = ", ".join(skills)
                    else:
                        skills_str = str(skills)
                    skills_lines.append(f"{cat}: {skills_str}")
            self.fields['skills_text'].initial = "\n".join(skills_lines)
            
            # Format education
            edu_lines = []
            if isinstance(self.instance.education, list):
                for edu in self.instance.education:
                    degree = edu.get('degree', '')
                    inst = edu.get('institution', '')
                    year = edu.get('year', '')
                    edu_lines.append(f"{degree} | {inst} | {year}")
            self.fields['education_text'].initial = "\n".join(edu_lines)

            # Format certifications
            cert_lines = []
            if isinstance(self.instance.certifications, list):
                for cert in self.instance.certifications:
                    name = cert.get('name', '')
                    issuer = cert.get('issuer', '')
                    year = cert.get('year', '')
                    cert_lines.append(f"{name} | {issuer} | {year}")
            self.fields['certifications_text'].initial = "\n".join(cert_lines)

    def clean_skills_text(self):
        data = self.cleaned_data.get('skills_text', '')
        skills_dict = {}
        if data:
            for idx, line in enumerate(data.split('\n')):
                line = line.strip()
                if not line:
                    continue
                if ':' not in line:
                    raise forms.ValidationError(
                        f"Line {idx+1}: Format must be 'Category: Skill 1, Skill 2'. Missing colon ':'."
                    )
                cat, skills_str = line.split(':', 1)
                cat = cat.strip()
                skills = [s.strip() for s in skills_str.split(',') if s.strip()]
                if not cat:
                    raise forms.ValidationError(
                        f"Line {idx+1}: Category name cannot be empty."
                    )
                if not skills:
                    raise forms.ValidationError(
                        f"Line {idx+1}: Skills list cannot be empty for category '{cat}'."
                    )
                skills_dict[cat] = skills
        return skills_dict

    def clean_education_text(self):
        data = self.cleaned_data.get('education_text', '')
        edu_list = []
        if data:
            for idx, line in enumerate(data.split('\n')):
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split('|')]
                if len(parts) < 2 or not parts[0] or not parts[1]:
                    raise forms.ValidationError(
                        f"Line {idx+1}: Format must be 'Degree | Institution | Year' (at least 1 pipe separator '|' is required)."
                    )
                degree = parts[0]
                inst = parts[1]
                year = parts[2] if len(parts) > 2 else ''
                edu_list.append({
                    'degree': degree,
                    'institution': inst,
                    'year': year
                })
        return edu_list

    def clean_certifications_text(self):
        data = self.cleaned_data.get('certifications_text', '')
        cert_list = []
        if data:
            for idx, line in enumerate(data.split('\n')):
                line = line.strip()
                if not line:
                    continue
                parts = [p.strip() for p in line.split('|')]
                if len(parts) < 2 or not parts[0] or not parts[1]:
                    raise forms.ValidationError(
                        f"Line {idx+1}: Format must be 'Cert Name | Issuer | Year' (at least 1 pipe separator '|' is required)."
                    )
                name = parts[0]
                issuer = parts[1]
                year = parts[2] if len(parts) > 2 else ''
                cert_list.append({
                    'name': name,
                    'issuer': issuer,
                    'year': year
                })
        return cert_list


    def save(self, commit=True):
        instance = super().save(commit=False)
        # Save the parsed data to the JSON fields
        instance.technical_skills = self.cleaned_data['skills_text']
        instance.education = self.cleaned_data['education_text']
        instance.certifications = self.cleaned_data['certifications_text']
        if commit:
            instance.save()
        return instance


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'description', 'technologies_used', 'client', 'duration']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Enter project description...'}),
            'technologies_used': forms.TextInput(attrs={'placeholder': 'e.g. Laravel, Mysql, Javascript'}),
        }


class EmployeeProjectMappingForm(forms.ModelForm):
    class Meta:
        model = EmployeeProjectMapping
        fields = ['project', 'role_and_responsibilities', 'duration', 'client', 'order']
        widgets = {
            'role_and_responsibilities': forms.Textarea(attrs={'rows': 5, 'placeholder': 'Enter responsibilities, one per line.\nExample:\nLaravel developer.\nDeveloped different panels based on user role.'}),
            'duration': forms.TextInput(attrs={'placeholder': 'Leave blank to use project duration'}),
            'client': forms.TextInput(attrs={'placeholder': 'Leave blank to use project client'}),
        }

    def __init__(self, *args, **kwargs):
        employee = kwargs.pop('employee', None)
        super().__init__(*args, **kwargs)
        if employee:
            # Exclude projects that are already mapped to this employee (if we are creating a new mapping)
            if not self.instance.pk:
                mapped_project_ids = employee.project_mappings.values_list('project_id', flat=True)
                self.fields['project'].queryset = Project.objects.exclude(id__in=mapped_project_ids)
