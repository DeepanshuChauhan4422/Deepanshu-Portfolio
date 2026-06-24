import os
import django
import json

def test_portfolio_application():
    print("Initializing Django test client...")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "portfolio_project.settings")
    django.setup()
    
    from django.test import Client
    client = Client()
    
    # 1. Test Home page
    print("Testing Home page GET request...")
    response = client.get('/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Home page status code: OK (200)")
    
    # 2. Test AI Assistant page
    print("Testing AI Assistant page GET request...")
    response = client.get('/ai-assistant/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("AI Assistant page status code: OK (200)")
    
    # 2b. Test Resume page
    print("Testing Resume page GET request...")
    response = client.get('/resume/')
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Resume page status code: OK (200)")
    
    # 3. Test Chat API Endpoint
    print("Testing Chat API endpoint POST request...")
    chat_payload = {
        "message": "Who is Deepanshu Chauhan?",
        "history": []
    }
    response = client.post(
        '/api/chat/',
        data=json.dumps(chat_payload),
        content_type='application/json'
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    print("Chat API status code: OK (200)")
    
    # 4. Verify API response content
    res_data = json.loads(response.content.decode('utf-8'))
    assert 'reply' in res_data, "Expected 'reply' key in JSON response"
    print("Chat API returned valid reply key: OK")
    print(f"Sample response: {res_data['reply'][:100]}...")
    
    # 5. Test Contact API Endpoint
    print("Testing Contact API endpoint POST request...")
    contact_payload = {
        "name": "Jane Recruiter",
        "email": "jane@company.com",
        "subject": "Interview Request",
        "message": "We would love to discuss a developer role."
    }
    response = client.post(
        '/api/contact/',
        data=json.dumps(contact_payload),
        content_type='application/json'
    )
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    contact_data = json.loads(response.content.decode('utf-8'))
    assert contact_data.get('success') is True, "Expected success to be True"
    print("Contact API status code: OK (200)")
    print(f"Sample response: {contact_data}")
    
    print("\n--- ALL TESTS COMPLETED SUCCESSFULLY! ---")

if __name__ == '__main__':
    test_portfolio_application()
