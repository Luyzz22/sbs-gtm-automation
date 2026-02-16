#!/usr/bin/env python3
"""
Automatisches Follow-up System - 3/7/14 Tage nach Erstkontakt
Author: Luis Schenk
"""
import pandas as pd
from datetime import datetime, timedelta
from automated_email_sender import SBSEmailAutomation
import os
from dotenv import load_dotenv
import resend

load_dotenv()

# Follow-up Templates
FOLLOW_UP_TEMPLATES = {
    'day_3': {
        'subject': '{first_name}, kurze Nachfrage zu {company_name}',
        'body': """Hallo {first_name},

ich wollte nur kurz nachhaken – hatten Sie Gelegenheit, über meine Nachricht nachzudenken?

Falls der Zeitpunkt gerade ungünstig ist: Wann wäre ein besserer Moment für ein kurzes Gespräch?

Beste Grüße,
Luis Schenk
Innovation Manager
SBS Deutschland GmbH"""
    },
    'day_7': {
        'subject': '{first_name}, konkretes Angebot für {company_name}',
        'body': """Hallo {first_name},

ich verstehe – Sie haben viel um die Ohren.

Lassen Sie mich konkret werden: Ich schicke Ihnen einen 2-Minuten-ROI-Rechner, den Sie selbst ausfüllen können.

Für {company_name} bedeutet das typischerweise:
• 15+ Stunden Zeitersparnis pro Monat
• 40% Kostenreduktion in der Verwaltung
• ROI in 6-9 Monaten

Interesse? Einfach mit "Ja" antworten.

Grüße,
Luis Schenk
ki@sbsdeutschland.de"""
    },
    'day_14': {
        'subject': 'Letzte Nachricht: {company_name}',
        'body': """Hallo {first_name},

ich möchte nicht drängeln – dies ist meine letzte Nachricht zu diesem Thema.

Falls sich in Zukunft etwas ändert und das Thema Prozessautomatisierung relevant wird, melden Sie sich gerne.

Alles Gute für {company_name}!

Luis Schenk
Innovation Manager
SBS Deutschland GmbH"""
    }
}

def send_follow_up(contact_email, company, days_ago):
    """Sendet Follow-up basierend auf Tagen seit Erstkontakt"""
    
    # Template auswählen
    if days_ago >= 14:
        template = FOLLOW_UP_TEMPLATES['day_14']
    elif days_ago >= 7:
        template = FOLLOW_UP_TEMPLATES['day_7']
    else:
        template = FOLLOW_UP_TEMPLATES['day_3']
    
    # Personalisieren
    first_name = contact_email.split('@')[0].split('.')[0].title()
    subject = template['subject'].format(first_name=first_name, company_name=company)
    body = template['body'].format(first_name=first_name, company_name=company)
    
    # Senden via Resend
    resend.api_key = os.getenv('RESEND_API_KEY')
    
    try:
        params = {
            "from": "Luis Schenk <ki@sbsdeutschland.de>",
            "to": [contact_email],
            "subject": subject,
            "html": body.replace('\n', '<br>'),
            "reply_to": "ki@sbsdeutschland.de",
        }
        
        email = resend.Emails.send(params)
        print(f"✓ Follow-up gesendet an {contact_email} (Tag {days_ago}) - ID: {email['id']}")
        return True
    except Exception as e:
        print(f"✗ Fehler bei {contact_email}: {str(e)}")
        return False

def main():
    """Hauptfunktion für Follow-up Automation"""
    print("="*60)
    print("SBS FOLLOW-UP AUTOMATION")
    print(f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print("="*60)
    
    # Lade vorherige Kampagnen
    try:
        df = pd.read_csv('campaign_results.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    except FileNotFoundError:
        print("✗ Keine campaign_results.csv gefunden")
        return
    
    now = datetime.now()
    follow_ups_sent = 0
    
    # Prüfe jeden Kontakt
    for _, row in df.iterrows():
        if row['status'] != 'sent':
            continue
        
        days_ago = (now - row['timestamp']).days
        
        # Follow-up Logik
        if days_ago == 3:
            print(f"\n📧 Tag 3 Follow-up: {row['email']}")
            if send_follow_up(row['email'], row['company'], 3):
                follow_ups_sent += 1
        elif days_ago == 7:
            print(f"\n📧 Tag 7 Follow-up: {row['email']}")
            if send_follow_up(row['email'], row['company'], 7):
                follow_ups_sent += 1
        elif days_ago == 14:
            print(f"\n📧 Tag 14 Follow-up (letzte Nachricht): {row['email']}")
            if send_follow_up(row['email'], row['company'], 14):
                follow_ups_sent += 1
    
    print(f"\n{'='*60}")
    print(f"✓ {follow_ups_sent} Follow-ups versendet")
    print(f"{'='*60}")

if __name__ == "__main__":
    main()
