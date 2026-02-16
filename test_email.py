#!/usr/bin/env python3
import os
from dotenv import load_dotenv
import resend

load_dotenv()
resend.api_key = os.getenv('RESEND_API_KEY')

print("Sende Test-Email...")

params = {
    "from": "Luis Schenk <ki@sbsdeutschland.de>",
    "to": ["ki@sbsdeutschland.de"],
    "subject": "✓ SBS GTM Automation - System Test",
    "html": """
    <h1>✓ Email-System funktioniert!</h1>
    <p>Ihre SBS GTM Automation ist einsatzbereit.</p>
    <p><strong>Sender:</strong> Luis Schenk - Innovation Manager<br>
    <strong>Company:</strong> SBS Deutschland GmbH</p>
    """
}

try:
    email = resend.Emails.send(params)
    print(f"✓ Test-Email erfolgreich gesendet!")
    print(f"   Email ID: {email['id']}")
    print(f"   Prüfen Sie Ihr Postfach: ki@sbsdeutschland.de")
except Exception as e:
    print(f"✗ Fehler: {str(e)}")
    print("   Mögliche Ursachen:")
    print("   - Domain noch nicht verifiziert")
    print("   - API Key falsch")
