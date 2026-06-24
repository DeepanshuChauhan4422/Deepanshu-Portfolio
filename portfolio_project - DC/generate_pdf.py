import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def generate_resume_pdf():
    # Make sure output directory exists
    output_dir = os.path.join(os.path.dirname(__file__), 'portfolio', 'static')
    os.makedirs(output_dir, exist_ok=True)
    pdf_path = os.path.join(output_dir, 'resume.pdf')
    
    # Page setup
    margin = 40
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=letter,
        leftMargin=margin,
        rightMargin=margin,
        topMargin=margin,
        bottomMargin=margin
    )
    
    story = []
    
    # Palette definitions
    primary_color = colors.HexColor("#1A1A1A")
    secondary_color = colors.HexColor("#444444")
    accent_color = colors.HexColor("#0D47A1")
    line_color = colors.HexColor("#CCCCCC")
    
    # Custom styles
    styles = getSampleStyleSheet()
    
    name_style = ParagraphStyle(
        'ResumeName',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        alignment=1 # Center
    )
    
    contact_style = ParagraphStyle(
        'ResumeContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=secondary_color,
        alignment=1 # Center
    )
    
    section_title_style = ParagraphStyle(
        'ResumeSectionTitle',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=3
    )
    
    body_style = ParagraphStyle(
        'ResumeBody',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=secondary_color
    )
    
    body_bold = ParagraphStyle(
        'ResumeBodyBold',
        parent=body_style,
        fontName='Helvetica-Bold'
    )
    
    bullet_style = ParagraphStyle(
        'ResumeBullet',
        parent=body_style,
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=3
    )
    
    # 1. Header (Name & Contact)
    story.append(Paragraph("DEEPANSHU CHAUHAN", name_style))
    story.append(Spacer(1, 6))
    
    contact_text = (
        "<b>Email:</b> Deepanshuchauhan2244@gmail.com | "
        "<b>Phone:</b> +91 8791095450 | "
        "<b>Location:</b> Greater Noida, India | "
        "<b>LinkedIn:</b> <a href='https://www.linkedin.com/in/deepanshu-chauhan-179a40252' color='#0D47A1'>deepanshu-chauhan</a>"
    )
    story.append(Paragraph(contact_text, contact_style))
    story.append(Spacer(1, 10))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceAfter=8, spaceBefore=4))
    
    # 2. Technologies
    story.append(Paragraph("TECHNOLOGIES", section_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=line_color, spaceAfter=6, spaceBefore=2))
    
    tech_data = [
        [
            Paragraph("<b>Languages:</b> Python, JavaScript", body_style),
            Paragraph("<b>Web Development Tools:</b> HTML, CSS, REST APIs, MongoDB, MySQL, Docker, Git, GitHub", body_style)
        ],
        [
            Paragraph("<b>Frameworks:</b> Django, Flask, FastAPI", body_style),
            Paragraph("<b>Relevant Technologies:</b> DSA, OS, OOPs, DBMS, CN, Software Engineering", body_style)
        ]
    ]
    
    # Table layout for Technologies (2 columns)
    tech_table = Table(tech_data, colWidths=[200, 310])
    tech_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 10),
    ]))
    story.append(tech_table)
    story.append(Spacer(1, 10))
    
    # 3. Projects
    story.append(Paragraph("PROJECTS", section_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=line_color, spaceAfter=6, spaceBefore=2))
    
    # Project 1
    story.append(Paragraph("<b>Team Task Manager</b>", body_bold))
    story.append(Paragraph("&bull; Built a full-stack Team Task Manager web application with interactive dashboards, task assignment, progress tracking, and team collaboration features.", bullet_style))
    story.append(Paragraph("&bull; Developed secure authentication, task status management, deadline tracking, and a responsive UI to improve productivity and workflow management for teams.", bullet_style))
    story.append(Spacer(1, 6))
    
    # Project 2
    story.append(Paragraph("<b>Real Estate Price Prediction</b>", body_bold))
    story.append(Paragraph("&bull; Built an intuitive and responsive UI using HTML, CSS, and JavaScript.", bullet_style))
    story.append(Paragraph("&bull; Designed clean input forms for users to enter property details (location, size, amenities, etc.).", bullet_style))
    story.append(Paragraph("&bull; Integrated JavaScript to send user data to the prediction model API.", bullet_style))
    story.append(Spacer(1, 6))
    
    # Project 3
    story.append(Paragraph("<b>Virtual Family</b>", body_bold))
    story.append(Paragraph("&bull; Developed conversational AI persons (Mother, Father, Guardian) using NLP techniques.", bullet_style))
    story.append(Paragraph("&bull; Integrated emotion-aware dialogue handling and voice personality traits.", bullet_style))
    story.append(Spacer(1, 10))
    
    # 4. Professional Experience
    story.append(Paragraph("PROFESSIONAL EXPERIENCE", section_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=line_color, spaceAfter=6, spaceBefore=2))
    
    story.append(Paragraph("<b>HCL TECH, TRAINEE</b>", body_bold))
    story.append(Paragraph("&bull; Completed a 3-month HCL training program focused on industry-oriented IT skills and practical learning.", bullet_style))
    story.append(Paragraph("&bull; Strengthened problem-solving, teamwork, and professional communication through guided tasks and assignments.", bullet_style))
    story.append(Spacer(1, 10))
    
    # 5. Education
    story.append(Paragraph("EDUCATION", section_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=line_color, spaceAfter=6, spaceBefore=2))
    
    edu_data = [
        [
            Paragraph("<b>KCC Institute of Technology & Management</b><br/><i>B.Tech in Computer Science and Engineering (AIML)</i>", body_style),
            Paragraph("<b>08/2022 &ndash; 06/2026</b>", ParagraphStyle('RightText', parent=body_style, alignment=2))
        ]
    ]
    edu_table = Table(edu_data, colWidths=[380, 130])
    edu_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ('TOPPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(edu_table)
    story.append(Spacer(1, 10))
    
    # 6. Achievements
    story.append(Paragraph("ACHIEVEMENTS", section_title_style))
    story.append(HRFlowable(width="100%", thickness=1, color=line_color, spaceAfter=6, spaceBefore=2))
    
    story.append(Paragraph("&bull; <b>HCL Technologies</b> &mdash; Successfully completed certification from HCL Technologies, gaining knowledge of industry-relevant tools and technologies.", bullet_style))
    story.append(Paragraph("&bull; <b>AICTE-SANKALP</b> &mdash; Completed government-recognized technical skill development program.", bullet_style))
    story.append(Paragraph("&bull; <b>SANKALAN</b> &mdash; Represented and won accolades at SANKALAN (Delhi University computer science festival).", bullet_style))
    
    # Build Document
    doc.build(story)
    print(f"PDF successfully generated at {pdf_path}")

if __name__ == '__main__':
    generate_resume_pdf()
