#!/usr/bin/env python3
"""Hunter.io Demo - Email Search"""

import os
from dotenv import load_dotenv
import requests

load_dotenv()

def search_domain_emails(domain):
    """Suche Email-Adressen für eine Domain"""
    api_key = os.getenv('HUNTER_API_KEY')
    
    print(f"🔍 Suche Emails für: {domain}\n")
    
    url = "https://api.hunter.io/v2/domain-search"
    params = {
        "domain": domain,
        "api_key": api_key,
        "limit": 10
    }
    
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        
        data = response.json()
        
        if 'data' in data:
            emails = data['data'].get('emails', [])
            
            # Zeige verfügbare Requests
            if 'meta' in data and 'requests' in data['meta']:
                meta = data['meta']
                used = meta['requests']['used']
                available = meta['requests']['available']
                print(f"📊 API Requests: {used} verwendet, {available} verfügbar\n")
            
            print(f"✅ {len(emails)} Email-Adressen gefunden\n")
            
            if emails:
                print("📧 Gefundene Emails:")
                for i, email_info in enumerate(emails[:5], 1):
                    email = email_info.get('value', 'N/A')
                    first = email_info.get('first_name', '?')
                    last = email_info.get('last_name', '?')
                    position = email_info.get('position', 'N/A')
                    
                    print(f"\n{i}. {email}")
                    print(f"   Name: {first} {last}")
                    print(f"   Position: {position}")
            else:
                print("⚠️  Keine öffentlichen Emails in Hunter-Datenbank")
                print("\nℹ️  Mögliche Gründe:")
                print("   • Domain ist zu klein/neu")
                print("   • Keine öffentlichen Team-Seiten")
                print("   • Emails sind nicht indexiert")
                
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 422:
            print("❌ Domain nicht gefunden oder ungültig")
        elif e.response.status_code == 429:
            print("❌ Rate Limit erreicht - zu viele Requests")
        else:
            print(f"❌ HTTP Error: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")

def test_with_known_domain():
    """Teste mit einer bekannten Domain (Stripe als Beispiel)"""
    print("="*60)
    print("🧪 Test mit bekannter Domain (Stripe)")
    print("="*60 + "\n")
    search_domain_emails("stripe.com")

if __name__ == "__main__":
    # Teste zuerst mit sbsdeutschland.com
    print("="*60)
    print("🎯 SBS Deutschland Email Search")
    print("="*60 + "\n")
    search_domain_emails("sbsdeutschland.com")
    
    print("\n" + "="*60)
    
    # Dann mit bekannter Domain zum Vergleich
    print("\n")
    test_with_known_domain()
    
    print("\n" + "="*60)
    print("\n💡 Tipp: Für kleine Unternehmen verwenden Sie Email Finder")
    print("   mit Namen von bekannten Mitarbeitern")
