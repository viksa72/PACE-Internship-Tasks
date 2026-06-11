from django.shortcuts import render, get_object_or_404, redirect
from django.http import FileResponse, Http404, JsonResponse
from django.db.models import Q
from .models import Employee, Project, EmployeeProjectMapping
from .forms import EmployeeForm, ProjectForm, EmployeeProjectMappingForm
from .pdf_generator import generate_resume_pdf_buffer


def dashboard(request):
    """
    Main dashboard displaying metrics, all employees, and recent projects.
    Handles standard search queries as well.
    """
    query = request.GET.get('q', '').strip()
    
    if query:
        employees = Employee.objects.filter(
            Q(employee_id__icontains=query) | Q(name__icontains=query)
        )
    else:
        employees = Employee.objects.all()

    # Metrics
    total_employees = Employee.objects.count()
    total_projects = Project.objects.count()
    total_mappings = EmployeeProjectMapping.objects.count()

    context = {
        'employees': employees,
        'query': query,
        'total_employees': total_employees,
        'total_projects': total_projects,
        'total_mappings': total_mappings,
        'recent_projects': Project.objects.all()[:5],
    }
    return render(request, 'resumes/dashboard.html', context)


def search_ajax(request):
    """
    AJAX endpoint for instant search suggestions.
    """
    query = request.GET.get('q', '').strip()
    if len(query) < 1:
        return JsonResponse({'results': []})
        
    employees = Employee.objects.filter(
        Q(employee_id__icontains=query) | Q(name__icontains=query)
    )[:5]
    
    results = []
    for emp in employees:
        results.append({
            'id': emp.id,
            'employee_id': emp.employee_id,
            'name': emp.name,
            'designation': emp.designation,
        })
    return JsonResponse({'results': results})


def employee_detail(request, pk):
    """
    Displays the detailed profile of an employee, including an HTML-based 
    resume preview and mapping tools.
    """
    employee = get_object_or_404(Employee, pk=pk)
    mappings = employee.project_mappings.all().select_related('project')
    
    context = {
        'employee': employee,
        'mappings': mappings,
    }
    return render(request, 'resumes/employee_detail.html', context)


def generate_resume_pdf(request, pk):
    """
    Generates and returns the PDF resume as a file download.
    """
    employee = get_object_or_404(Employee, pk=pk)
    mappings = employee.project_mappings.all().select_related('project')
    
    # Generate the PDF in memory
    buffer = generate_resume_pdf_buffer(employee, mappings)
    
    # Return FileResponse
    filename = f"Resume_{employee.name.replace(' ', '_')}_{employee.employee_id}.pdf"
    return FileResponse(
        buffer,
        as_attachment=True,
        filename=filename,
        content_type='application/pdf'
    )


# --- EMPLOYEE CRUD ---

def add_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            employee = form.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm()
    return render(request, 'resumes/employee_form.html', {'form': form, 'action': 'Add'})


def edit_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        form = EmployeeForm(request.POST, instance=employee)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeForm(instance=employee)
    return render(request, 'resumes/employee_form.html', {'form': form, 'action': 'Edit', 'employee': employee})


def delete_employee(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    if request.method == 'POST':
        employee.delete()
        return redirect('dashboard')
    return render(request, 'resumes/confirm_delete.html', {'object': employee, 'type': 'Employee'})


# --- PROJECT CRUD ---

def list_projects(request):
    projects = Project.objects.all()
    return render(request, 'resumes/project_list.html', {'projects': projects})


def add_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_projects')
    else:
        form = ProjectForm()
    return render(request, 'resumes/project_form.html', {'form': form, 'action': 'Add'})


def edit_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('list_projects')
    else:
        form = ProjectForm(instance=project)
    return render(request, 'resumes/project_form.html', {'form': form, 'action': 'Edit', 'project': project})


def delete_project(request, pk):
    project = get_object_or_404(Project, pk=pk)
    if request.method == 'POST':
        project.delete()
        return redirect('list_projects')
    return render(request, 'resumes/confirm_delete.html', {'object': project, 'type': 'Project'})


# --- EMPLOYEE PROJECT MAPPING ---

def add_mapping(request, employee_pk):
    employee = get_object_or_404(Employee, pk=employee_pk)
    if request.method == 'POST':
        form = EmployeeProjectMappingForm(request.POST, employee=employee)
        if form.is_valid():
            mapping = form.save(commit=False)
            mapping.employee = employee
            mapping.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeProjectMappingForm(employee=employee)
    return render(request, 'resumes/mapping_form.html', {'form': form, 'employee': employee, 'action': 'Add'})


def edit_mapping(request, pk):
    mapping = get_object_or_404(EmployeeProjectMapping, pk=pk)
    employee = mapping.employee
    if request.method == 'POST':
        form = EmployeeProjectMappingForm(request.POST, instance=mapping)
        if form.is_valid():
            form.save()
            return redirect('employee_detail', pk=employee.pk)
    else:
        form = EmployeeProjectMappingForm(instance=mapping)
    return render(request, 'resumes/mapping_form.html', {'form': form, 'employee': employee, 'action': 'Edit', 'mapping': mapping})


def delete_mapping(request, pk):
    mapping = get_object_or_404(EmployeeProjectMapping, pk=pk)
    employee = mapping.employee
    if request.method == 'POST':
        mapping.delete()
        return redirect('employee_detail', pk=employee.pk)
    return render(request, 'resumes/confirm_delete.html', {'object': mapping, 'type': 'Project Mapping'})

