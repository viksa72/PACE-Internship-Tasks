import os
from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

# A4 dimensions in points
A4_WIDTH, A4_HEIGHT = A4

class NumberedCanvas(canvas.Canvas):
    """
    Custom canvas that performs two-pass rendering to draw static headers, 
    footers, and page numbers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        # Save page state for the second pass
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_header_footer(num_pages)
            super().showPage()
        super().save()

    def draw_header_footer(self, page_count):
        self.saveState()
        
        # --- HEADER ---
        # Draw logo: extracted_logo_0.png on the left
        logo_path = os.path.join(settings.BASE_DIR, 'extracted_logo_0.png')
        if os.path.exists(logo_path):
            # Drawing the logo: x=36, y=A4_HEIGHT - 55, width=170, height=20 (maintaining ratio)
            self.drawImage(logo_path, 36, A4_HEIGHT - 65, width=170, height=20, mask='auto')
        else:
            # Fallback if logo is missing (e.g. text placeholder)
            self.setFont("Helvetica-Bold", 14)
            self.setFillColor(colors.HexColor('#1e40af'))
            self.drawString(36, A4_HEIGHT - 55, "pacewisdom")
            
        # Draw header text: PACE WISDOM SOLUTIONS PVT. LTD. on the right
        self.setFont("Helvetica-Bold", 10)
        self.setFillColor(colors.HexColor('#1e40af'))
        self.drawRightString(A4_WIDTH - 36, A4_HEIGHT - 55, "PACE WISDOM SOLUTIONS PVT. LTD.")
        
        # Draw teal line below header
        self.setStrokeColor(colors.HexColor('#1e40af'))
        self.setLineWidth(1.5)
        self.line(36, A4_HEIGHT - 72, A4_WIDTH - 36, A4_HEIGHT - 72)


        # --- FOOTER ---
        # Draw footer line
        self.setStrokeColor(colors.HexColor('#cccccc'))
        self.setLineWidth(0.5)
        self.line(36, 45, A4_WIDTH - 36, 45)
        
        # Draw page number centered in the footer area
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor('#555555'))
        text = f"Page {self._pageNumber}"
        self.drawCentredString(A4_WIDTH / 2.0, 25, text)
        
        self.restoreState()


def get_hr_flowable(width, color=colors.HexColor('#cccccc'), thickness=0.5):
    """
    Returns a horizontal line flowable using a single-cell ReportLab Table.
    """
    t = Table([['']], colWidths=[width], rowHeights=[1])
    t.setStyle(TableStyle([
        ('LINEABOVE', (0, 0), (-1, -1), thickness, color),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    return t


def generate_resume_pdf_buffer(employee, mappings):
    """
    Generates a PDF using ReportLab and writes it to an in-memory buffer.
    """
    import io
    buffer = io.BytesIO()
    
    # 0.5 inch (36pt) margins, leaving topMargin and bottomMargin to accommodate header/footer
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=90,  # leaves space below the header line (y=770)
        bottomMargin=65  # leaves space above the footer line (y=45)
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Styles
    normal_style = styles['Normal']
    
    # Text alignments and sizes matching sample
    text_style = ParagraphStyle(
        'ResumeText',
        parent=normal_style,
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.black
    )
    
    bold_text_style = ParagraphStyle(
        'ResumeBoldText',
        parent=text_style,
        fontName='Helvetica-Bold'
    )
    
    title_section_style = ParagraphStyle(
        'TitleSection',
        parent=text_style,
        fontSize=10.5,
        leading=14,
        spaceAfter=15
    )
    
    heading_style = ParagraphStyle(
        'SectionHeading',
        parent=normal_style,
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        spaceBefore=12,
        spaceAfter=8,
        textColor=colors.black,
        keepWithNext=True
    )
    
    bullet_style = ParagraphStyle(
        'ResumeBullet',
        parent=text_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=5
    )
    
    project_title_style = ParagraphStyle(
        'ProjectTitle',
        parent=normal_style,
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=15,
        spaceBefore=8,
        spaceAfter=6,
        textColor=colors.black,
        keepWithNext=True
    )
    
    project_meta_style = ParagraphStyle(
        'ProjectMeta',
        parent=text_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    project_desc_style = ParagraphStyle(
        'ProjectDesc',
        parent=text_style,
        leftIndent=15,
        spaceAfter=6
    )
    
    project_roles_heading_style = ParagraphStyle(
        'ProjectRolesHeading',
        parent=bold_text_style,
        leftIndent=15,
        spaceAfter=4,
        keepWithNext=True
    )
    
    project_role_bullet_style = ParagraphStyle(
        'ProjectRoleBullet',
        parent=text_style,
        leftIndent=28,
        firstLineIndent=-10,
        spaceAfter=3
    )

    story = []
    content_width = A4_WIDTH - 72 # 595.27 - 72 = 523.27
    
    # 1. Employee Name & Designation Header
    name_designation_text = f"<b>Name: {employee.name}</b><br/><b>Designation: {employee.designation}</b>"
    story.append(Paragraph(name_designation_text, title_section_style))
    
    # 2. Professional Summary
    story.append(Paragraph("Professional Summary:", heading_style))
    summary_lines = employee.professional_summary.split('\n')
    for line in summary_lines:
        line = line.strip()
        if line:
            # Strip any manual bullet characters
            if line.startswith('●') or line.startswith('•') or line.startswith('-'):
                line = line[1:].strip()
            story.append(Paragraph(f"&bull;&nbsp;&nbsp;{line}", bullet_style))
            
    # 3. Technical Skill Set
    if employee.technical_skills:
        story.append(Paragraph("Technical Skill Set", heading_style))
        
        # Build skills table matching column layout
        table_data = []
        for cat, skills in employee.technical_skills.items():
            if isinstance(skills, list):
                skills_str = ", ".join(skills)
            else:
                skills_str = str(skills)
                
            bullet_p = Paragraph("&bull;", text_style)
            cat_p = Paragraph(f"<b>{cat}</b>", text_style)
            colon_p = Paragraph(":", text_style)
            skills_p = Paragraph(skills_str, text_style)
            
            table_data.append([bullet_p, cat_p, colon_p, skills_p])
            
        if table_data:
            # Col widths: bullet(12pt), category(160pt), colon(10pt), skills(341pt)
            skills_table = Table(table_data, colWidths=[12, 160, 10, 341])
            skills_table.setStyle(TableStyle([
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('TOPPADDING', (0, 0), (-1, -1), 2),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 2),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))
            story.append(skills_table)

    # 4. Professional Projects
    if mappings.exists():
        story.append(Paragraph("Professional Projects", heading_style))
        
        for idx, mapping in enumerate(mappings):
            proj = mapping.project
            duration = mapping.duration if mapping.duration else (proj.duration if proj.duration else "")
            client = mapping.client if mapping.client else (proj.client if proj.client else "")
            
            # Project title
            story.append(Paragraph(f"Project {idx + 1}: {proj.name}", project_title_style))
            
            # Technologies used
            tech_str = f"&bull;&nbsp;&nbsp;<b>Technology used:</b>&nbsp;&nbsp;{proj.technologies_used}."
            story.append(Paragraph(tech_str, project_meta_style))
            
            # Description
            desc_str = f"<b>Description:</b> {proj.description}"
            story.append(Paragraph(desc_str, project_desc_style))
            
            # Roles & Responsibilities
            story.append(Paragraph("Role and Responsibilities:", project_roles_heading_style))
            resp_lines = mapping.role_and_responsibilities.split('\n')
            for resp in resp_lines:
                resp = resp.strip()
                if resp:
                    if resp.startswith('●') or resp.startswith('•') or resp.startswith('-'):
                        resp = resp[1:].strip()
                    story.append(Paragraph(f"&bull;&nbsp;&nbsp;{resp}", project_role_bullet_style))
                    
            # Separator line between projects (not after the last one)
            if idx < len(mappings) - 1:
                story.append(Spacer(1, 4))
                story.append(get_hr_flowable(content_width))
                story.append(Spacer(1, 4))

    # 5. Education (Optional - only if data exists)
    if employee.education:
        story.append(Spacer(1, 8))
        story.append(Paragraph("Education", heading_style))
        for edu in employee.education:
            degree = edu.get('degree', '')
            inst = edu.get('institution', '')
            year = edu.get('year', '')
            edu_str = f"&bull;&nbsp;&nbsp;<b>{degree}</b> - {inst}"
            if year:
                edu_str += f" ({year})"
            story.append(Paragraph(edu_str, bullet_style))

    # 6. Certifications (Optional - only if data exists)
    if employee.certifications:
        story.append(Spacer(1, 8))
        story.append(Paragraph("Certifications", heading_style))
        for cert in employee.certifications:
            name = cert.get('name', '')
            issuer = cert.get('issuer', '')
            year = cert.get('year', '')
            cert_str = f"&bull;&nbsp;&nbsp;<b>{name}</b>"
            if issuer:
                cert_str += f" - {issuer}"
            if year:
                cert_str += f" ({year})"
            story.append(Paragraph(cert_str, bullet_style))

    # Build document
    doc.build(story, canvasmaker=NumberedCanvas)
    
    buffer.seek(0)
    return buffer
