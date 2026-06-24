import json
import os
import urllib.request
import urllib.error
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.mail import send_mail
from django.conf import settings
from .models import ContactMessage

# -------------------------------------------------------------------------
# Fallback Smart Responder in case GEMINI_API_KEY is not set
# -------------------------------------------------------------------------
DEEPANSHU_BIO = """
Deepanshu Chauhan is a B.Tech Computer Science and Engineering student specializing in Artificial Intelligence and Machine Learning (AIML) at KCC Institute of Technology & Management (expected graduation: June 2026).
He is an aspiring Software Engineer and Python Developer passionate about Backend Development, Full-Stack Development, and AI-powered applications.
"""

DEEPANSHU_PROJECTS = """
Deepanshu has built several notable projects:
1. **Team Task Manager**: A full-stack collaborative platform with secure authentication, task assignment, progress tracking, and interactive dashboards.
   - *Live Demo:* https://team-task-manager-n72w.onrender.com/
2. **Real Estate Price Prediction**: A machine learning web application that predicts property prices based on location, size, and amenities.
   - *Live Demo:* https://real-estate-price-prediction-omega.vercel.app/
3. **Virtual Family**: An NLP-based conversational AI application featuring custom personas (Mother, Father, Guardian) with emotion-aware dialogue handling and distinct voice personality traits.
"""

DEEPANSHU_SKILLS = """
Deepanshu's technical stack includes:
- **Languages:** Python, JavaScript, HTML5, CSS3
- **Frameworks:** Django, Flask, FastAPI
- **Databases:** MongoDB, MySQL, PostgreSQL, SQLite
- **Tools & Core CS:** REST APIs, Docker, Git, GitHub, Data Structures & Algorithms (DSA), OOPs, Database Management Systems (DBMS), Operating Systems (OS), Computer Networks (CN), and Machine Learning Basics.
"""

DEEPANSHU_EXPERIENCE = """
**HCL Tech - Trainee (3 Months)**
- Completed an industry-oriented IT training program focusing on practical software engineering skills.
- Developed problem-solving, teamwork, and professional communication skills through structured tasks.
"""

DEEPANSHU_CONTACT = """
You can reach Deepanshu through the following channels:
- **Email:** deepanshuchauhan2244@gmail.com
- **Phone:** +91 8791095450
- **Location:** Greater Noida, India
- **LinkedIn:** https://www.linkedin.com/in/deepanshu-chauhan-179a40252
- **GitHub:** https://github.com/DeepanshuChauhan4422
"""

DEEPANSHU_EDUCATION = """
**KCC Institute of Technology & Management**
- B.Tech in Computer Science and Engineering (Specialization in AIML)
- Duration: August 2022 – June 2026
"""

DEEPANSHU_STRENGTHS = """
Deepanshu's strengths include:
- Strong foundations in computer science core principles (DSA, OOPs, DBMS, OS).
- Hands-on expertise with Python and web frameworks like Django, Flask, and FastAPI.
- Experience building AI-focused projects (Machine Learning models, NLP conversational agents).
- Proven ability to work in team environments (demonstrated during his HCL Trainee experience).
- Quick learner, highly adaptable to new tech stacks and toolsets.
"""

def smart_fallback_response(user_message):
    msg = user_message.lower()
    if any(k in msg for k in ["who", "profile", "deepanshu", "about", "bio"]):
        return f"### Who is Deepanshu Chauhan?\n{DEEPANSHU_BIO}\nWould you like to know more about his skills, projects, or experience?"
    elif any(k in msg for k in ["project", "build", "create", "make", "task manager", "price prediction", "virtual family"]):
        return f"### Projects Built by Deepanshu\n{DEEPANSHU_PROJECTS}"
    elif any(k in msg for k in ["skill", "technology", "technologies", "know", "stack", "language", "python", "django", "fastapi"]):
        return f"### Deepanshu's Technical Skills\n{DEEPANSHU_SKILLS}"
    elif any(k in msg for k in ["experience", "work", "hcl", "job", "intern", "trainee"]):
        return f"### Professional Experience\n{DEEPANSHU_EXPERIENCE}"
    elif any(k in msg for k in ["education", "college", "degree", "university", "btech", "b.tech", "kcc"]):
        return f"### Education & Timeline\n{DEEPANSHU_EDUCATION}"
    elif any(k in msg for k in ["contact", "email", "phone", "linkedin", "github", "hire", "recruit"]):
        return f"### Contact Details\n{DEEPANSHU_CONTACT}"
    elif any(k in msg for k in ["strength", "why hire", "benefit", "good at"]):
        return f"### Deepanshu's Key Strengths\n{DEEPANSHU_STRENGTHS}"
    else:
        return f"Hello! I am Deepanshu Assistant.\n\nI can tell you about his:\n- **Technical Skills**\n- **Projects** (like Team Task Manager)\n- **Experience & Internships** (HCL Trainee)\n- **Education** (B.Tech CSE - AIML)\n- **Strengths & Contact Details**\n\nWhat would you like to know?"

# -------------------------------------------------------------------------
# View Handlers
# -------------------------------------------------------------------------

def home(request):
    """Renders the main landing portfolio page."""
    return render(request, 'index.html')

def ai_assistant(request):
    """Renders the dedicated Deepanshu Assistant page."""
    return render(request, 'ai-assistant.html')

@csrf_exempt
def chat_api(request):
    """
    POST endpoint for the AI Chat Assistant.
    Calls Gemini API using urllib if key is present, otherwise falls back to smart responder.
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        data = json.loads(request.body)
        user_message = data.get('message', '')
        history = data.get('history', [])
    except Exception:
        return JsonResponse({'error': 'Invalid JSON body'}, status=400)
    
    if not user_message:
        return JsonResponse({'error': 'Message cannot be empty'}, status=400)
    
    api_key = os.environ.get("GEMINI_API_KEY")
    
    if not api_key:
        # Fallback to local intelligence engine if key is not configured
        bot_response = smart_fallback_response(user_message)
        return JsonResponse({'reply': bot_response, 'source': 'fallback'})
    
    # Constructing System Instruction and contents for Gemini API
    system_instruction = (
        "You are Deepanshu Assistant. Your goal is to answer questions from recruiters "
        "and hiring managers about Deepanshu. Be professional, enthusiastic, and polite. Highlight his technical strengths, "
        "projects, and readiness for software engineering roles.\n\n"
        "Here is the verified information about Deepanshu:\n"
        f"- Profile: {DEEPANSHU_BIO}\n"
        f"- Skills: {DEEPANSHU_SKILLS}\n"
        f"- Projects: {DEEPANSHU_PROJECTS}\n"
        f"- Experience: {DEEPANSHU_EXPERIENCE}\n"
        f"- Education: {DEEPANSHU_EDUCATION}\n"
        f"- Contact: {DEEPANSHU_CONTACT}\n"
        f"- Strengths: {DEEPANSHU_STRENGTHS}\n\n"
        "Rules:\n"
        "1. Keep responses concise, engaging, and professional. Use markdown list formatting for readability.\n"
        "2. If asked about unrelated things (e.g. general code help, unrelated queries), politely bring the focus back to Deepanshu.\n"
        "3. Offer contact links naturally when recruitment or hiring is mentioned."
    )
    
    # Prepare Gemini API request payload
    # We will format the request matching the Gemini 2.5/1.5 API structure
    contents = []
    
    # Append history to content structure
    for chat in history:
        role = 'user' if chat.get('role') == 'user' else 'model'
        contents.append({
            'role': role,
            'parts': [{'text': chat.get('content', '')}]
        })
        
    # Append current message
    contents.append({
        'role': 'user',
        'parts': [{'text': user_message}]
    })
    
    payload = {
        'contents': contents,
        'systemInstruction': {
            'parts': [{'text': system_instruction}]
        },
        'generationConfig': {
            'temperature': 0.7,
            'maxOutputTokens': 800
        }
    }
    
    # API endpoints for Gemini API
    # Using gemini-1.5-flash as it is extremely fast, highly available, and perfect for simple agent text tasks
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    
    try:
        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        
        with urllib.request.urlopen(req, timeout=10) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            
            # Parse Gemini response structure
            candidates = res_data.get('candidates', [])
            if candidates:
                bot_response = candidates[0].get('content', {}).get('parts', [{}])[0].get('text', '')
            else:
                bot_response = "I apologize, but I received empty content from my AI core. Deepanshu is an excellent Python developer and engineer, please feel free to reach out to him directly at deepanshuchauhan2244@gmail.com!"
            
            return JsonResponse({'reply': bot_response, 'source': 'gemini'})
            
    except urllib.error.URLError as e:
        # Log error locally and return smart fallback so the UI never breaks
        print(f"Gemini API Request failed: {e}")
        bot_response = smart_fallback_response(user_message)
        return JsonResponse({'reply': bot_response, 'source': 'api_error_fallback'})
    except Exception as e:
        print(f"Exception calling Gemini: {e}")
        bot_response = smart_fallback_response(user_message)
        return JsonResponse({'reply': bot_response, 'source': 'exception_fallback'})

def resume(request):
    """Renders the resume page."""
    return render(request, 'resume.html')

@csrf_exempt
def contact_api(request):
    """
    POST endpoint to process the contact form, save messages to database,
    and send emails via SMTP (or log them in debug console backend).
    """
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        if request.content_type == 'application/json':
            data = json.loads(request.body)
        else:
            data = request.POST
            
        name = data.get('name', '').strip()
        email = data.get('email', '').strip()
        subject = data.get('subject', '').strip()
        message = data.get('message', '').strip()
    except Exception:
        return JsonResponse({'error': 'Invalid request body'}, status=400)
        
    if not (name and email and subject and message):
        return JsonResponse({'error': 'All fields are required'}, status=400)
        
    try:
        # 1. Save to SQL Database
        msg = ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )
        
        # 2. Try to Send Email
        email_subject = f"Portfolio Contact Form: {subject}"
        email_body = f"Message from: {name} <{email}>\n\nSubject: {subject}\n\nMessage:\n{message}"
        
        send_mail(
            subject=email_subject,
            message=email_body,
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'webmaster@localhost'),
            recipient_list=['deepanshuchauhan2244@gmail.com'],
            fail_silently=False
        )
        
        return JsonResponse({'success': True, 'message': 'Message saved and sent successfully.'})
    except Exception as e:
        print(f"Exception in contact_api: {e}")
        return JsonResponse({
            'success': True,
            'message': 'Message saved to database successfully (Email delivery fell back to server terminal logs).'
        })
