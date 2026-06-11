import os
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'resume_builder.settings')
django.setup()

from resumes.models import Employee, Project, EmployeeProjectMapping

def seed():
    print("Clearing database...")
    EmployeeProjectMapping.objects.all().delete()
    Employee.objects.all().delete()
    Project.objects.all().delete()

    print("Creating employee...")
    employee = Employee.objects.create(
        employee_id="PW-0042",
        name="XXXXX XXXXX",
        designation="Software Developer – L2",
        professional_summary=(
            "Having 4.3 years total and relevant experience on Development of Web Applications.\n"
            "A team player with good communication skills and eagerness to share and gain knowledge.\n"
            "Experience in working with Web Applications Using Laravel and Django.\n"
            "Working Knowledge on Linux and Windows.\n"
            "GIT for code management and version control.\n"
            "integrated Google apis/tools like Geolocation."
        ),
        email="developer@pacewisdom.com",
        phone="+91 9876543210",
        address="123 Corporate Campus, tech Hub, Bangalore, India",
        technical_skills={
            "Programming and Scripting": ["JavaScript", "PHP", "HTML 5", "CSS 3"],
            "Frameworks": ["Vue js", "Laravel", "Django"],
            "Development Tools": ["VsCode"],
            "Web API Tools": ["Postman"],
            "Operating System": ["Linux", "Windows 7/8/10", "MacOS"],
            "Version tool": ["Github", "Gitlab", "Bitbucket"]
        },
        education=[
            {"degree": "B.E. Computer Science & Engineering", "institution": "Visvesvaraya Technological University", "year": "2021"}
        ],
        certifications=[
            {"name": "AWS Certified Cloud Practitioner", "issuer": "Amazon Web Services", "year": "2023"},
            {"name": "Django Developer Certification", "issuer": "Python Institute", "year": "2022"}
        ]
    )

    print("Creating projects master database...")
    projects_data = [
        {
            "name": "Time tag",
            "technologies": "Laravel, Mysql, Javascript, Jquery, Ajax, Html, Css & Bootstrap",
            "description": "Time tag is a website used to fill employee timesheets. Also, the admin has an option to check all employees' timesheets, filtering employees timesheets based on filters and exporting timesheets.",
            "roles": "Laravel developer.\nDeveloped different panels based on user role.\nTimesheet filtration based on date.\nExport timesheet.\nCRUD operations.\nUI implementation."
        },
        {
            "name": "OurShopping",
            "technologies": "Laravel, Mysql, Javascript, Jquery, Ajax, Html, Css & Bootstrap",
            "description": "OurShopping is an e-shopping website with a wide range of customers across UAE, Oman, Qatar, Kuwait, and Bahrain. They have a huge collection of various products so customers can make the earth's biggest selection.",
            "roles": "Laravel developer.\nAdmin panel with backpack(plugin).\nAPI’s for mobile application.\nOption to add products which will be listed in mobile application.\nSending notifications for all the users.\nPush notifications."
        },
        {
            "name": "Swastiks",
            "technologies": "Laravel, Mysql, Javascript, Jquery, Ajax, Html, Css & Bootstrap",
            "description": "Swastiks Masala is a centre for the authentic flavours of India. Today, they are South India’s favourite for our spicy masalas and delicious products!. Users can order various Swastiks masalas from this application.",
            "roles": "Laravel, Ajax, Jquery, HTML developer.\nPayment gateway : Razorpay\nAdmin Panel using AdminLTE\nCRUD Operations\nEmail Functionality."
        },
        {
            "name": "Funskool",
            "technologies": "Laravel, Mysql, Javascript, Jquery, Ajax, Html, Css & Bootstrap",
            "description": "Funskool is an online shopping application where users can order toys for their kids.And its also a leading toy manufacturing company in India.",
            "roles": "Laravel, Ajax, Jquery, HTML developer.\nPayment gateway :PayU.\nEmail functionality.\nSMS functionality : Textlocal.\nImport products through csv.\nExport products."
        },
        {
            "name": "Vidyawin",
            "technologies": "Laravel, Mysql",
            "description": "Vidyawin is an online Edu-Tech platform start-up launched in 2020 with an objective of imparting education to students across India. Vidyawin offers simple & easy to understand learning programs for Classes 5th to 12th",
            "roles": "Laravel developer.\nCreated APIs\nPayment Gateway : Razorpay\nSMS functionality : TextLocal"
        },
        {
            "name": "Agriapp",
            "technologies": "Laravel, Mysql, Javascript, Jquery, Ajax, Html, Css & Bootstrap",
            "description": "Agriapp is a platform which gives farmers a latest technique for farming and farmers can order required products from nearby agricultural stores through this application.",
            "roles": "Laravel, Ajax, Jquery, HTML developer.\nCreated APIs.\nCRUD operations.\nMail functionality : SMTP."
        },
        {
            "name": "Otter Platform",
            "technologies": "Laravel, Mysql, Javascript, Jquery, Ajax, Html, Css & Bootstrap",
            "description": "Otter Platform is an application which helps NGOs to get required tools and other services for their website which makes their job easier. Tool makers will be signing up and posting all their tools and NGOs will be checking and can purchase required tools and also they can get mentorship help through this application.",
            "roles": "Laravel, Ajax, Jquery, HTML developer.\nAdmin panel using AdminLTE.\nCRUD operations.\nCreated APIs.\nDB Design."
        },
        {
            "name": "Arpitha Exports",
            "technologies": "Core PHP",
            "description": "Arpitha Exports is the website where users can check for construction materials and can get clear ideas on those materials.",
            "roles": "Core PHP developer\nMail functionality : SMTP"
        },
        {
            "name": "Pangaea X",
            "technologies": "Core PHP",
            "description": "Pangaea is a platform which helps freelancers to get new projects and one can hire a freelancer for his project.",
            "roles": "Core PHP developer\nMail functionality : Sendgrid."
        },
        {
            "name": "Dhishan Global Spaces",
            "technologies": "Core PHP",
            "description": "Worked on map functionality and email functionality using Sendinblue.",
            "roles": "Core PHP developer.\nGoogle map functionlity.\nMail functionality: Sendinblue."
        },
        {
            "name": "Cohome",
            "technologies": "Core PHP, Wordpress",
            "description": "Cohome is a platform where users can book a room. I have worked on 3rd party API’s to fetch required details from other websites and google maps.",
            "roles": "Core PHP developer.\nCreated APIs.\nGoogle map functionality."
        },
        {
            "name": "Essae",
            "technologies": "Angular Js",
            "description": "Essae is a stand alone application which weighs calculate-managing applications.",
            "roles": "Angular Js developer.\nWorked on APIs.\nUI Implementation."
        },
        {
            "name": "Otter Platform (React)",
            "technologies": "Laravel, React",
            "description": "Otter Platform is a platform which helps NGO by offering mentors, tools that help to grow their org.",
            "roles": "Laravel developer.\nWorked on APIs.\nUI Implementation."
        },
        {
            "name": "1m1b Future Leaders",
            "technologies": "Laravel, Vuejs",
            "description": "1m1b Future Leaders is a platform which helps Students to improve their skill by conducting various activities.",
            "roles": "Laravel and Vuejs developer.\nWorked on APIs.\nUI Implementation."
        },
        {
            "name": "Lead Z",
            "technologies": "Laravel, Vuejs",
            "description": "Leadz is a new age platform that provides young leaders in high schools - the Generation Z, opportunities to solve challenges, develop innovative solutions towards a better future and in the process develop their leadership capabilities.",
            "roles": "Laravel and Vuejs developer.\nWorked on APIs.\nUI Implementation."
        },
        {
            "name": "Timesheet and Projects Portal",
            "technologies": "Django",
            "description": "An Employee management application is an internal tool that helps in resource management and utilization. Also helps the management to track and download the timesheet for every employee.",
            "roles": "Django developer.\nWorked on APIs.\nUI Implementation."
        }
    ]

    for idx, p_data in enumerate(projects_data):
        proj = Project.objects.create(
            name=p_data["name"],
            technologies_used=p_data["technologies"],
            description=p_data["description"]
        )
        EmployeeProjectMapping.objects.create(
            employee=employee,
            project=proj,
            role_and_responsibilities=p_data["roles"],
            order=idx + 1
        )
        print(f"Mapped Project: {proj.name}")

    # Add 4 additional employees
    print("Creating additional employees...")
    
    # 1. Aditi Sharma - Lead Frontend Engineer
    emp1 = Employee.objects.create(
        employee_id="PW-0105",
        name="Aditi Sharma",
        designation="Lead Frontend Engineer",
        professional_summary=(
            "Result-oriented Lead Frontend Engineer with 6+ years of experience specializing in building highly interactive web applications.\n"
            "Expertise in React, Vue.js, TypeScript, and modern state management libraries.\n"
            "Passionate about optimizing web performance, UI accessibility, and mentoring junior engineers."
        ),
        email="aditi.sharma@pacewisdom.com",
        phone="+91 9988776655",
        address="Flat 402, Elite Residency, Whitefield, Bangalore, India",
        technical_skills={
            "Programming & Scripting": ["JavaScript (ES6+)", "TypeScript", "HTML5", "CSS3 / Sass"],
            "Frameworks & Libraries": ["React.js", "Redux Toolkit", "Vue.js", "Vuex", "Next.js"],
            "Build & Tooling": ["Webpack", "Vite", "ESLint", "NPM / Yarn"],
            "Testing": ["Jest", "React Testing Library", "Cypress"],
            "Design Systems": ["Tailwind CSS", "Bootstrap", "Material UI", "Figma"]
        },
        education=[
            {"degree": "B.Tech in Information Technology", "institution": "Delhi Technological University", "year": "2020"}
        ],
        certifications=[
            {"name": "Frontend Web Developer Nanodegree", "issuer": "Udacity", "year": "2021"},
            {"name": "Certified ScrumMaster (CSM)", "issuer": "Scrum Alliance", "year": "2023"}
        ]
    )
    
    # 2. Rahul Verma - Senior Backend Engineer
    emp2 = Employee.objects.create(
        employee_id="PW-0112",
        name="Rahul Verma",
        designation="Senior Backend Engineer",
        professional_summary=(
            "Senior Backend Developer with 5 years of experience designing, developing, and deploying scalable RESTful APIs and microservices.\n"
            "Strong command over Python, Django, and database optimization.\n"
            "Experienced in cloud migrations, system architecture, and implementing secure authentication mechanisms."
        ),
        email="rahul.verma@pacewisdom.com",
        phone="+91 8877665544",
        address="Suite 12, Sobha Apartments, Indiranagar, Bangalore, India",
        technical_skills={
            "Programming Languages": ["Python", "SQL", "Go (Golang)", "Bash Scripting"],
            "Frameworks": ["Django", "Django REST Framework", "FastAPI", "Flask"],
            "Databases": ["PostgreSQL", "MySQL", "Redis (Caching)", "MongoDB"],
            "DevOps & Deployments": ["Docker", "AWS (EC2, RDS, S3)", "Nginx", "GitHub Actions"],
            "Security & Auth": ["OAuth 2.0", "JWT", "HTTPS / SSL"]
        },
        education=[
            {"degree": "M.Tech in Software Engineering", "institution": "BITS Pilani", "year": "2021"}
        ],
        certifications=[
            {"name": "AWS Certified Solutions Architect – Associate", "issuer": "Amazon Web Services", "year": "2024"}
        ]
    )

    # 3. Priya Nair - Full Stack Developer
    emp3 = Employee.objects.create(
        employee_id="PW-0128",
        name="Priya Nair",
        designation="Full Stack Developer",
        professional_summary=(
            "Versatile Full Stack Developer with 3.5 years of experience developing clean, maintainable code across the entire stack.\n"
            "Proficient in Vue.js, Node.js, Express, and Laravel PHP framework.\n"
            "Skilled in relational database modeling, responsive UI integration, and writing automated test cases."
        ),
        email="priya.nair@pacewisdom.com",
        phone="+91 7766554433",
        address="Greenwood Layout, Sarjapur Road, Bangalore, India",
        technical_skills={
            "Languages": ["JavaScript (ES6)", "PHP", "HTML5 / CSS3", "Python"],
            "Frontend Frameworks": ["Vue.js", "React.js", "Bootstrap", "Tailwind CSS"],
            "Backend Frameworks": ["Node.js / Express", "Laravel PHP", "Django"],
            "Databases": ["MySQL", "PostgreSQL", "SQLite"],
            "Version Control & Tools": ["Git / GitHub", "Postman API client", "Jira"]
        },
        education=[
            {"degree": "B.E. in Computer Science", "institution": "VTU Karnataka", "year": "2022"}
        ],
        certifications=[
            {"name": "Full Stack Web Developer Certificate", "issuer": "FreeCodeCamp", "year": "2022"}
        ]
    )

    # 4. Vikram Malhotra - DevOps & Cloud Engineer
    emp4 = Employee.objects.create(
        employee_id="PW-0140",
        name="Vikram Malhotra",
        designation="DevOps & Cloud Engineer",
        professional_summary=(
            "AWS Certified DevOps Engineer with 4 years of experience building and automating scalable infrastructure.\n"
            "Expertise in Containerization, Infrastructure as Code (IaC), and setting up continuous integration/delivery (CI/CD) pipelines.\n"
            "Committed to improving software delivery speed, infrastructure reliability, and cloud cost management."
        ),
        email="vikram.malhotra@pacewisdom.com",
        phone="+91 9900112233",
        address="10th Cross, Koramangala, Bangalore, India",
        technical_skills={
            "Cloud Platforms": ["Amazon Web Services (AWS)", "Google Cloud Platform (GCP)"],
            "Containerization & Orchestration": ["Docker", "Kubernetes (EKS, GKE)"],
            "Infrastructure as Code": ["Terraform", "CloudFormation"],
            "CI/CD Tools": ["Jenkins", "GitHub Actions", "GitLab CI"],
            "Monitoring & Logging": ["Prometheus", "Grafana", "ELK Stack"],
            "Scripting & OS": ["Linux (Ubuntu, CentOS)", "Bash", "Python"]
        },
        education=[
            {"degree": "B.Sc. in Computer Science", "institution": "St. Joseph's College, Bangalore", "year": "2022"}
        ],
        certifications=[
            {"name": "AWS Certified DevOps Engineer – Professional", "issuer": "Amazon Web Services", "year": "2025"},
            {"name": "Certified Kubernetes Administrator (CKA)", "issuer": "The Linux Foundation", "year": "2024"}
        ]
    )

    # Map projects to these employees to build a rich graph
    print("Mapping projects to new employees...")
    
    # Helper lists of projects
    p_ourshopping = Project.objects.get(name="OurShopping")
    p_otter = Project.objects.get(name="Otter Platform")
    p_leadz = Project.objects.get(name="Lead Z")
    p_vidyawin = Project.objects.get(name="Vidyawin")
    p_timesheet = Project.objects.get(name="Timesheet and Projects Portal")
    p_swastiks = Project.objects.get(name="Swastiks")
    p_timetag = Project.objects.get(name="Time tag")
    p_agriapp = Project.objects.get(name="Agriapp")

    # Map Aditi (Lead Frontend)
    EmployeeProjectMapping.objects.create(
        employee=emp1, project=p_ourshopping, order=1,
        role_and_responsibilities="Frontend Team Lead.\nRefactored legacy UI components using Vue.js for higher rendering speed.\nDesigned responsive catalog pages with optimal mobile device support.\nConfigured backpack templates for administrative management panels."
    )
    EmployeeProjectMapping.objects.create(
        employee=emp1, project=p_otter, order=2,
        role_and_responsibilities="Lead UI Developer.\nBuilt dynamic react panels for NGO dashboard and mentor search.\nIntegrated responsive forms and tables using Bootstrap.\nCollaborated on REST API integration and component state management."
    )
    EmployeeProjectMapping.objects.create(
        employee=emp1, project=p_leadz, order=3,
        role_and_responsibilities="Lead Frontend Developer.\nDeveloped the gamified challenge interface using Vue.js.\nIntegrated interactive drag-and-drop components.\nOptimized layout paint times and reduced bundle size by 35%."
    )

    # Map Rahul (Senior Backend)
    EmployeeProjectMapping.objects.create(
        employee=emp2, project=p_vidyawin, order=1,
        role_and_responsibilities="Senior Python Developer.\nDesigned scalable REST APIs using Django for classes 5 to 12 platform.\nIntegrated SMS gateway (TextLocal) for real-time OTP verification.\nIntegrated Razorpay payment systems for smooth subscriptions."
    )
    EmployeeProjectMapping.objects.create(
        employee=emp2, project=p_timesheet, order=2,
        role_and_responsibilities="Django Developer.\nDeveloped internal resource mapping and timesheet tracking algorithms.\nDesigned export services for XLS and PDF formats.\nOptimized SQL queries to handle complex timesheet calculations across 500+ employees."
    )
    EmployeeProjectMapping.objects.create(
        employee=emp2, project=p_swastiks, order=3,
        role_and_responsibilities="Backend Engineer.\nImplemented payment flow checks using Razorpay APIs.\nCreated asynchronous email delivery tasks for invoice dispatch.\nConfigured AdminLTE templates for store management panels."
    )

    # Map Priya (Full Stack)
    EmployeeProjectMapping.objects.create(
        employee=emp3, project=p_timetag, order=1,
        role_and_responsibilities="Full Stack Engineer.\nIntegrated Laravel controller actions with jQuery/AJAX calls.\nDeveloped timesheet filter modules based on employee and date.\nDesigned responsive user roles configuration panel."
    )
    EmployeeProjectMapping.objects.create(
        employee=emp3, project=p_swastiks, order=2,
        role_and_responsibilities="Laravel & Web Developer.\nImplemented CRUD operations for product inventory.\nDeveloped user-facing cart and checkout components using AJAX.\nDesigned transaction confirmation email notifications."
    )
    EmployeeProjectMapping.objects.create(
        employee=emp3, project=p_agriapp, order=3,
        role_and_responsibilities="Full Stack Developer.\nCreated REST APIs for product search and localized store queries.\nConfigured mail settings using SMTP protocols.\nIntegrated responsive store layouts matching design mockups."
    )

    # Map Vikram (DevOps & Cloud)
    EmployeeProjectMapping.objects.create(
        employee=emp4, project=p_otter, order=1,
        role_and_responsibilities="DevOps Architect.\nDockerized application components for rapid deployment.\nConfigured CI/CD pipelines in GitLab CI to automate testing and code scans.\nProvisioned secure Kubernetes clusters using Terraform on GCP."
    )
    EmployeeProjectMapping.objects.create(
        employee=emp4, project=p_vidyawin, order=2,
        role_and_responsibilities="DevOps Engineer.\nDeployed staging environments on AWS EC2 behind Nginx reverse proxies.\nConfigured RDS instances with automatic daily backup plans.\nCreated Prometheus monitoring scripts and alerts for backend latency."
    )

    print("Database seeding completed successfully!")

if __name__ == "__main__":
    seed()
