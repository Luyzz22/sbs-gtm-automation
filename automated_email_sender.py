#!/usr/bin/env python3
"""
SBS Nexus GTM Email Automation
KI-personalisierte Outreach-Emails für Steuerberater & Kanzleien
Produkt: SBS Nexus – KI-gestützte Rechnungsverarbeitung mit DATEV-Integration
Website: https://sbsdeutschland.com/sbshomepage/ | https://www.sbsnexus.de
"""

import os
import resend
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import yaml
from typing import Dict, List, Tuple
import time
from datetime import datetime
import pandas as pd
import openai

load_dotenv()


class SBSEmailAutomation:
    """Enterprise Email Automation für SBS Nexus Steuerberater-Outreach"""

    def __init__(self, use_resend: bool = True):
        self.use_resend = use_resend
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_name = os.getenv('SENDER_NAME', 'Luis Orozco')
        self.sender_title = os.getenv('SENDER_TITLE', 'Gründer & CEO')
        self.company = os.getenv('COMPANY_NAME', 'SBS Deutschland GmbH')

        if use_resend:
            resend.api_key = os.getenv('RESEND_API_KEY')
            print("✓ Resend API initialisiert")
        else:
            self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.strato.de')
            self.smtp_port = int(os.getenv('SMTP_PORT', 465))
            self.smtp_username = os.getenv('SMTP_USERNAME')
            self.smtp_password = os.getenv('SMTP_PASSWORD')
            self.smtp_use_ssl = os.getenv('SMTP_USE_SSL', 'True') == 'True'
            print("✓ Strato SMTP initialisiert")

    def load_templates(self) -> Dict:
        with open('config/message_templates.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def select_template(self, role: str, templates: Dict) -> Dict:
        role_lower = role.lower()

        if any(x in role_lower for x in ['steuerberater', 'kanzleiinhaber', 'partner', 'wirtschaftsprüfer']):
            return templates['templates']['steuerberater_template']
        elif any(x in role_lower for x in ['cfo', 'finanz', 'buchhal']):
            return templates['templates']['kmu_template']
        elif 'digital' in role_lower:
            return templates['templates']['digital_kanzlei_template']
        else:
            return templates['templates']['steuerberater_template']

    def personalize_message(self, template: Dict, contact: Dict) -> Tuple[str, str]:
        subject = template['subject_variants'][0]
        msg_parts = template['message']
        sections = []

        for key in ['opening', 'value_proposition', 'pain_point', 'differentiator',
                    'social_proof', 'partnership', 'cta', 'signature']:
            if key in msg_parts:
                sections.append(msg_parts[key])

        body = "\n\n".join(sections)

        replacements = {
            'first_name': contact.get('first_name', ''),
            'last_name': contact.get('last_name', ''),
            'job_title': contact.get('job_title', ''),
            'company_name': contact.get('company_name', ''),
            'datev_status': contact.get('datev_status', 'DATEV Mitglied'),
            'datev_label_count': str(contact.get('datev_label_count', '')),
            'mandanten_count': str(contact.get('mandanten_count', '80-120')),
            'team_size': str(contact.get('company_size', '15')),
            'personalization_hook': contact.get('personalization_hook', f"als {contact.get('job_title', 'Steuerberater')} bei {contact.get('company_name', '')} setzen Sie digitale Maßstäbe."),
            'sender_name': self.sender_name,
            'sender_title': self.sender_title,
            'sender_phone': os.getenv('SENDER_PHONE', ''),
            'calendly_link': os.getenv('CALENDLY_LINK', 'https://calendly.com/sbs-nexus/demo'),
        }

        for key, value in replacements.items():
            subject = subject.replace(f"{{{{{key}}}}}", str(value))
            body = body.replace(f"{{{{{key}}}}}", str(value))

        return subject, body

    def generate_ai_email(self, contact: Dict) -> Tuple[str, str]:
        """Generiert personalisierte SBS Nexus Email mit OpenAI GPT-4"""
        openai.api_key = os.getenv('OPENAI_API_KEY')

        prompt = f"""Erstelle eine professionelle B2B Cold Email für SBS Nexus:

EMPFÄNGER:
- Name: {contact.get('first_name', '')} {contact.get('last_name', '')}
- Position: {contact.get('job_title', 'Steuerberater')}
- Unternehmen: {contact.get('company_name', '')}
- Segment: {contact.get('segment', 'Digital-affin')}
- DATEV-Status: {contact.get('datev_status', 'DATEV Mitglied')}

PERSONALISIERUNG: {contact.get('personalization_hook', 'Digital-affine Kanzlei')}

SENDER:
- Name: {self.sender_name}
- Position: {self.sender_title}
- Unternehmen: SBS Deutschland GmbH

PRODUKT - SBS NEXUS:
- KI-gestützte Rechnungsverarbeitung
- 8 Sekunden Verarbeitungszeit pro Rechnung
- 99,2% Erkennungsgenauigkeit
- Automatischer DATEV-konformer Export
- Unterstützt: XRechnung, ZUGFeRD, PDF
- Multimodale KI (nicht regelbasierte OCR)
- DSGVO-konform, Server in Frankfurt
- E-Rechnungspflicht 2025 Compliance

PARTNERPROGRAMM:
- 15-25% Revenue Share (3 Tiers)
- Dauerhaft pro vermitteltem Mandant
- Keine Vorabkosten
- 14-Tage-Onboarding
- Details: www.sbsnexus.de/partner

MARKT:
- 89.000 Steuerberater in Deutschland
- €21,3 Mrd. Marktvolumen
- DATEV 90%+ Marktanteil
- E-Rechnungspflicht seit Januar 2025

STIL:
- Professionell, konkret, Enterprise-Standard (Apple/SAP Niveau)
- Deutsche Business-Etikette (Sehr geehrte/r)
- Max. 250-300 Wörter
- Personalisierungs-Hook nutzen!
- Kein generisches Marketing
- Konkrete Zahlen

STRUKTUR:
1. Persönliche Ansprache mit Bezug auf Kanzlei
2. Konkretes Pain Point (Rechnungsverarbeitung, E-Rechnung)
3. SBS Nexus als Lösung mit messbaren Vorteilen
4. Partnerprogramm erwähnen (Revenue Share)
5. Subtiler CTA (20-Min Demo)
6. Professionelle Signatur

Schreibe NUR die Email, keine Metakommentare."""

        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Du bist Experte für deutsche B2B Enterprise Sales Emails im Steuerberater-Markt. Du schreibst auf dem Niveau von Apple, SAP und NVIDIA Corporate Communications. Produkt: SBS Nexus KI-Rechnungsverarbeitung."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )

            body = response.choices[0].message.content.strip()

            subject_prompt = f"""Erstelle einen professionellen Email-Betreff für:
- Empfänger: {contact.get('first_name', '')} {contact.get('last_name', '')} bei {contact.get('company_name', '')}
- Thema: SBS Nexus KI-Rechnungsverarbeitung für Steuerberater
- Max 60 Zeichen, Deutsch, konkret mit Zahlen
- Beispiele: "70% weniger Zeitaufwand bei der Rechnungsverarbeitung" oder "8 Sekunden statt 8 Minuten: KI für Ihre Kanzlei"
Schreibe NUR den Betreff."""

            subject_response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": subject_prompt}],
                temperature=0.6,
                max_tokens=50
            )

            subject = subject_response.choices[0].message.content.strip().strip('"')

            print(f"   ✓ AI-Email generiert ({len(body)} Zeichen)")
            return subject, body

        except Exception as e:
            print(f"   ✗ AI-Fehler: {str(e)}")
            templates = self.load_templates()
            template = self.select_template(contact.get('role', 'Steuerberater'), templates)
            return self.personalize_message(template, contact)

    def send_via_resend(self, to_email: str, subject: str, body: str) -> bool:
        try:
            params: resend.Emails.SendParams = {
                "from": f"{self.sender_name} <{self.sender_email}>",
                "to": [to_email],
                "subject": subject,
                "html": body.replace('\n', '<br>'),
                "reply_to": self.sender_email,
            }
            email = resend.Emails.send(params)
            print(f"✓ Email via Resend gesendet an {to_email} (ID: {email['id']})")
            return True
        except Exception as e:
            print(f"✗ Resend Fehler bei {to_email}: {str(e)}")
            return False

    def send_via_smtp(self, to_email: str, subject: str, body: str) -> bool:
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = to_email
            msg['Subject'] = subject
            msg['Reply-To'] = self.sender_email

            text_part = MIMEText(body, 'plain', 'utf-8')
            html_part = MIMEText(body.replace('\n', '<br>'), 'html', 'utf-8')
            msg.attach(text_part)
            msg.attach(html_part)

            if self.smtp_use_ssl:
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)

            print(f"✓ Email via SMTP gesendet an {to_email}")
            return True
        except Exception as e:
            print(f"✗ SMTP Fehler bei {to_email}: {str(e)}")
            return False

    def send_email(self, to_email: str, subject: str, body: str) -> bool:
        if self.use_resend:
            return self.send_via_resend(to_email, subject, body)
        else:
            return self.send_via_smtp(to_email, subject, body)

    def send_campaign(self, contacts: List[Dict], delay_seconds: int = 120) -> Dict:
        templates = self.load_templates()
        results = {
            'timestamp': datetime.now().isoformat(),
            'sent': 0, 'failed': 0, 'total': len(contacts),
            'details': []
        }

        print(f"\n🚀 SBS Nexus Email-Kampagne für {len(contacts)} Steuerberater...")
        print(f"📧 Sender: {self.sender_name} <{self.sender_email}>")
        print(f"⚙️  Methode: {'Resend API' if self.use_resend else 'SMTP'}\n")

        for idx, contact in enumerate(contacts, 1):
            print(f"\n[{idx}/{len(contacts)}] {contact.get('company_name', '')} – {contact['email']}")

            USE_AI = os.getenv('USE_AI_GENERATION', 'True') == 'True'

            if USE_AI and os.getenv('OPENAI_API_KEY'):
                subject, body = self.generate_ai_email(contact)
            else:
                template = self.select_template(contact.get('role', 'Steuerberater'), templates)
                subject, body = self.personalize_message(template, contact)

            success = self.send_email(contact['email'], subject, body)

            results['details'].append({
                'email': contact['email'],
                'company': contact.get('company_name', ''),
                'status': 'sent' if success else 'failed',
                'timestamp': datetime.now().isoformat()
            })

            if success:
                results['sent'] += 1
            else:
                results['failed'] += 1

            if idx < len(contacts):
                print(f"   ⏳ Warte {delay_seconds}s...")
                time.sleep(delay_seconds)

        return results

    def export_results(self, results: Dict, filename: str = 'campaign_results.csv'):
        df = pd.DataFrame(results['details'])
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\n📊 Ergebnisse: {filename}")


# Steuerberater Prio-A Kontaktliste
TARGET_CONTACTS = [
    {
        'email': 'info@stbstaat.de',
        'first_name': 'Tobias',
        'last_name': 'Staat',
        'job_title': 'Steuerberater',
        'role': 'Steuerberater',
        'company_name': 'Steuerberater Tobias Staat',
        'segment': 'Digital-affin',
        'company_size': 15,
        'datev_status': 'DATEV UO aktiv',
        'personalization_hook': 'als mehrfach ausgezeichnete digitale Steuerkanzlei in Weinheim und Heidelberg setzen Sie Maßstäbe. Ihr Ansatz "Steuern gestalten, nicht verwalten" passt perfekt zu unserem Produkt.'
    },
    {
        'email': 'kanzlei@hrsteuer.de',
        'first_name': '',
        'last_name': '',
        'job_title': 'Kanzleiinhaber',
        'role': 'Steuerberater',
        'company_name': 'HR Steuerberatung',
        'segment': 'Digital-affin',
        'company_size': 10,
        'datev_status': 'DATEV UO aktiv',
        'personalization_hook': 'auf Ihrer Website ist mir Ihre Sektion "KI-Tools" aufgefallen – das zeigt, dass Sie Technologie nicht nur nutzen, sondern aktiv vorantreiben.'
    },
    {
        'email': 'kanzlei@steuba.de',
        'first_name': 'Michael',
        'last_name': 'Jonas',
        'job_title': 'Wirtschaftsprüfer',
        'role': 'Steuerberater',
        'company_name': 'STEUBA GmbH',
        'segment': 'Digital-affin',
        'company_size': 20,
        'datev_status': 'DATEV UO aktiv + Digitale Kanzlei Label',
        'personalization_hook': 'Sie setzen bereits auf DATEV Unternehmen Online und beschreiben sich als Steuerberatung mit Hands-on-Mentalität. Genau da setzt SBS Nexus an.'
    },
    {
        'email': 'info@luebeckonline.com',
        'first_name': '',
        'last_name': '',
        'job_title': 'Kanzleiinhaber',
        'role': 'Steuerberater',
        'company_name': 'Steuerkanzlei LÜBECK',
        'segment': 'Digital-affin',
        'company_size': 10,
        'datev_status': 'Digitale DATEV-Kanzlei seit 2019',
        'personalization_hook': 'Ihre Kanzlei trägt das Label Digitale DATEV-Kanzlei seit 2019 – damit gehören Sie zu den absoluten Vorreitern in Frankfurt.'
    },
]


if __name__ == "__main__":
    print("=" * 60)
    print("SBS NEXUS GTM EMAIL AUTOMATION")
    print(f"Sender: Luis Orozco – Gründer & CEO")
    print(f"Produkt: SBS Nexus – KI-Rechnungsverarbeitung")
    print(f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print("=" * 60)

    automation = SBSEmailAutomation(use_resend=True)

    print(f"\n📋 {len(TARGET_CONTACTS)} Steuerberater-Kontakte (Prio A):")
    for contact in TARGET_CONTACTS:
        print(f"   • {contact['company_name']} – {contact['email']}")

    confirm = input(f"\n✓ Kampagne starten? (ja/nein): ").strip().lower()

    if confirm in ['ja', 'j', 'yes', 'y']:
        results = automation.send_campaign(contacts=TARGET_CONTACTS, delay_seconds=120)

        print("\n" + "=" * 60)
        print("📊 KAMPAGNEN-ERGEBNIS")
        print("=" * 60)
        print(f"✓ Gesendet: {results['sent']}/{results['total']}")
        print(f"✗ Fehler: {results['failed']}/{results['total']}")

        automation.export_results(results)
        print("\n✅ SBS Nexus Kampagne abgeschlossen!")
    else:
        print("\n❌ Kampagne abgebrochen.")
