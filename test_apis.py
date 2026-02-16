#!/usr/bin/env python3
import os
from dotenv import load_dotenv

load_dotenv()

def test_openai():
    print("\n🤖 OpenAI Test...")
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Sage: OK"}],
            max_tokens=10
        )
        print(f"   ✅ OpenAI funktioniert: {response.choices[0].message.content}")
        return True
    except Exception as e:
        print(f"   ❌ OpenAI Error: {e}")
        return False

def test_anthropic():
    print("\n🧠 Anthropic Test...")
    try:
        from anthropic import Anthropic
        client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        message = client.messages.create(
            model="claude-3-5-haiku-20241022",
            max_tokens=10,
            messages=[{"role": "user", "content": "Sage: OK"}]
        )
        print(f"   ✅ Claude funktioniert: {message.content[0].text}")
        return True
    except Exception as e:
        print(f"   ❌ Claude Error: {e}")
        return False

def test_linkedin():
    print("\n💼 LinkedIn Test...")
    email = os.getenv('LINKEDIN_EMAIL')
    password = os.getenv('LINKEDIN_PASSWORD')
    if email and password:
        print(f"   ✅ Email: {email}")
        print(f"   ✅ Password: {'*' * len(password)}")
        return True
    return False

def test_hunter():
    print("\n🔍 Hunter.io Test...")
    api_key = os.getenv('HUNTER_API_KEY')
    if not api_key or api_key == 'your-hunter-api-key-here':
        print("   ⚠️  Noch nicht konfiguriert")
        print("   📝 Setup: https://hunter.io/users/sign_up")
        return False
    
    try:
        import requests
        r = requests.get("https://api.hunter.io/v2/account", params={"api_key": api_key})
        if r.status_code == 200:
            data = r.json()
            avail = data['data']['requests']['searches']['available']
            print(f"   ✅ Hunter.io verbunden ({avail} requests)")
            return True
    except Exception as e:
        print(f"   ❌ Error: {e}")
    return False

def test_company():
    print("\n🏢 Company Config...")
    company = os.getenv('COMPANY_NAME')
    domain = os.getenv('COMPANY_DOMAIN')
    print(f"   ✅ {company}")
    print(f"   ✅ {domain}")
    return True

if __name__ == "__main__":
    print("="*50)
    print("🧪 SBS GTM Automation - API Test")
    print("="*50)
    
    results = {
        "OpenAI": test_openai(),
        "Anthropic": test_anthropic(),
        "LinkedIn": test_linkedin(),
        "Hunter.io": test_hunter(),
        "Company": test_company()
    }
    
    print("\n" + "="*50)
    print(f"📊 {sum(results.values())}/{len(results)} APIs konfiguriert")
    print("="*50)
