#!/usr/bin/env python3
"""
SBS GTM Email Automation - Vollautomatischer Email-Versand
Author: Luis Schenk
Date: 16.02.2026
Description: Automatisiertes Email-System für B2B Enterprise SaaS Marketing
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
    """Enterprise Email Automation für SBS Deutschland GTM"""
    
    def __init__(self, use_resend: bool = True):
        self.use_resend = use_resend
        self.sender_email = os.getenv('SENDER_EMAIL')
        self.sender_name = os.getenv('SENDER_NAME', 'Luis Schenk')
        self.sender_title = os.getenv('SENDER_TITLE', 'Board of Directors')
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
        """Lädt Templates aus config/message_templates.yaml"""
        with open('config/message_templates.yaml', 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)
    
    def select_template(self, role: str, templates: Dict) -> Dict:
        """Wählt Template basierend auf Zielrolle"""
        role_lower = role.lower()
        
        if any(x in role_lower for x in ['cfo', 'finanz', 'controller']):
            return templates['templates']['cfo_template']
        elif any(x in role_lower for x in ['cto', 'it', 'technical']):
            return templates['templates']['cto_template']
        else:
            return templates['templates']['ceo_template']
    
    def personalize_message(self, template: Dict, contact: Dict) -> Tuple[str, str]:
        """Erstellt vollständig personalisierte Email"""
        subject = template['subject_variants'][0]
        msg_parts = template['message']
        sections = []
        
        for key in ['opening', 'value_proposition', 'pain_point', 
                    'technical_specs', 'business_case', 'social_proof', 'cta', 'signature']:
            if key in msg_parts:
                sections.append(msg_parts[key])
        
        body = "\n\n".join(sections)
        
        replacements = {
            'first_name': contact.get('first_name', ''),
            'last_name': contact.get('last_name', ''),
            'job_title': contact.get('job_title', ''),
            'company_name': contact.get('company_name', ''),
            'industry': contact.get('industry', 'Maschinenbau'),
            'company_size': str(contact.get('company_size', 100)),
            'current_system': contact.get('current_system', 'SAP'),
            'current_erp_system': contact.get('current_erp_system', 'DATEV'),
            'sender_name': self.sender_name,
            'sender_title': self.sender_title,
            'competitor_or_similar': contact.get('competitor', 'führende Unternehmen'),
            'estimated_revenue': contact.get('estimated_revenue', '50M EUR'),
            'tech_stack_known': contact.get('tech_stack', 'moderne Systeme'),
            'cloud_vs_onprem': contact.get('deployment', 'Hybrid')
        }
        
        for key, value in replacements.items():
            subject = subject.replace(f"{{{{{key}}}}}", str(value))
            body = body.replace(f"{{{{{key}}}}}", str(value))
        
        return subject, body
    
    def generate_ai_email(self, contact: Dict, template_type: str = 'professional') -> Tuple[str, str]:
        """Generiert personalisierte Email mit OpenAI GPT-4"""
        openai.api_key = os.getenv('OPENAI_API_KEY')
        
        prompt = f"""Erstelle eine professionelle B2B Cold Email für SBS Deutschland:

EMPFÄNGER:
- Name: {contact['first_name']} {contact['last_name']}
- Position: {contact['job_title']}
- Unternehmen: {contact['company_name']}
- Branche: {contact.get('industry', 'Maschinenbau')}

SENDER:
- Name: {self.sender_name}
- Position: {self.sender_title}
- Unternehmen: {self.company}

KONTEXT:
SBS ist führender ERP-Anbieter für deutschen Mittelstand. 
Branchenspezifische Lösungen mit SAP-Integration.

STIL: Professionell, konkret, 250-350 Wörter, Deutsche Business-Etikette

STRUKTUR:
1. Persönliche Ansprache mit Branchenbezug
2. Konkrete Pain Points
3. SBS Lösung mit messbaren Vorteilen
4. Subtiler CTA
5. Signatur

Schreibe NUR die Email, keine Metakommentare."""
        
        try:
            response = openai.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "Du bist Experte für deutsche B2B Enterprise Sales Emails im Mittelstand."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=800
            )
            
            body = response.choices[0].message.content.strip()
            
            subject_prompt = f"Erstelle professionellen Email-Betreff für {contact['first_name']} {contact['last_name']} bei {contact['company_name']}. Thema: SBS ERP. Max 60 Zeichen, Deutsch."
            
            subject_response = openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": subject_prompt}],
                temperature=0.6,
                max_tokens=50
            )
            
            subject = subject_response.choices[0].message.content.strip()
            
            print(f"   ✓ AI-Email generiert ({len(body)} Zeichen)")
            return subject, body
            
        except Exception as e:
            print(f"   ✗ AI-Fehler: {str(e)}")
            templates = self.load_templates()
            template = self.select_template(contact.get('role', 'CEO'), templates)
            return self.personalize_message(template, contact)
    
    def send_via_resend(self, to_email: str, subject: str, body: str) -> bool:
        """Sendet Email via Resend API"""
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
        """Sendet Email via Strato SMTP"""
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
            
            print(f"✓ Email via Strato SMTP gesendet an {to_email}")
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
        """Sendet vollautomatische Email-Kampagne"""
        templates = self.load_templates()
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'sent': 0,
            'failed': 0,
            'total': len(contacts),
            'details': []
        }
        
        print(f"\n🚀 Starte Email-Kampagne für {len(contacts)} Kontakte...")
        print(f"📧 Sender: {self.sender_name} <{self.sender_email}>")
        print(f"⚙️  Methode: {'Resend API' if self.use_resend else 'Strato SMTP'}\n")
        
        for idx, contact in enumerate(contacts, 1):
            print(f"\n[{idx}/{len(contacts)}] Verarbeite: {contact['email']}")
            
            # AI vs Template Toggle
            USE_AI = os.getenv('USE_AI_GENERATION', 'True') == 'True'
            
            if USE_AI and os.getenv('OPENAI_API_KEY'):
                print(f"   🤖 Generiere AI-Email...")
                subject, body = self.generate_ai_email(contact)
            else:
                print(f"   📄 Nutze Template-System...")
                template = self.select_template(contact.get('role', 'CEO'), templates)
                subject, body = self.personalize_message(template, contact)
            
            print(f"   Subject: {subject}")
            print(f"   Template: {template['id']}")
            
            success = self.send_email(contact['email'], subject, body)
            
            result_entry = {
                'email': contact['email'],
                'company': contact.get('company_name', 'Unknown'),
                'status': 'sent' if success else 'failed',
                'timestamp': datetime.now().isoformat(),
                'template': template['id']
            }
            
            results['details'].append(result_entry)
            
            if success:
                results['sent'] += 1
            else:
                results['failed'] += 1
            
            if idx < len(contacts):
                print(f"   ⏳ Warte {delay_seconds}s...")
                time.sleep(delay_seconds)
        
        return results
    
    def export_results(self, results: Dict, filename: str = 'campaign_results.csv'):
        """Exportiert Kampagnen-Ergebnisse"""
        df = pd.DataFrame(results['details'])
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\n📊 Ergebnisse exportiert nach: {filename}")


# Kontaktliste
TARGET_CONTACTS = [
    {
        'email': 'max.mustermann@hahn-automation.de',
        'first_name': 'Max',
        'last_name': 'Mustermann',
        'job_title': 'CFO',
        'role': 'CFO',
        'company_name': 'Hahn Automation GmbH',
        'industry': 'Maschinenbau',
        'company_size': 180,
        'current_erp_system': 'SAP',
        'estimated_revenue': '55M EUR',
        'competitor': 'Precision Tools AG'
    },
    {
        'email': 'claudia.meyer@techmach.de',
        'first_name': 'Claudia',
        'last_name': 'Meyer',
        'job_title': 'CFO',
        'role': 'CFO',
        'company_name': 'TechMach Industries',
        'industry': 'Werkzeugmaschinenbau',
        'company_size': 150,
        'current_erp_system': 'DATEV',
        'estimated_revenue': '45M EUR'
    },
    {
        'email': 'julia.richter@machinevision.de',
        'first_name': 'Julia',
        'last_name': 'Richter',
        'job_title': 'CTO',
        'role': 'CTO',
        'company_name': 'MachineVision GmbH',
        'industry': 'Werkzeugmaschinenbau',
        'company_size': 120,
        'current_system': 'SAP',
        'tech_stack': 'Python, Docker, PostgreSQL',
        'deployment': 'Cloud-first'
    }
]


if __name__ == "__main__":
    print("="*60)
    print("SBS GTM EMAIL AUTOMATION SYSTEM")
    print(f"Sender: Luis Schenk - Board of Directors")
    print(f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print("="*60)
    
    automation = SBSEmailAutomation(use_resend=True)
    
    print(f"\n📋 {len(TARGET_CONTACTS)} Kontakte geladen:")
    for contact in TARGET_CONTACTS:
        print(f"   • {contact['company_name']} - {contact['first_name']} {contact['last_name']} ({contact['role']})")
    
    confirm = input(f"\n✓ Kampagne starten? (ja/nein): ").strip().lower()
    
    if confirm in ['ja', 'j', 'yes', 'y']:
        results = automation.send_campaign(
            contacts=TARGET_CONTACTS,
            delay_seconds=120
        )
        
        print("\n" + "="*60)
        print("📊 KAMPAGNEN-ERGEBNIS")
        print("="*60)
        print(f"✓ Erfolgreich gesendet: {results['sent']}/{results['total']}")
        print(f"✗ Fehlgeschlagen: {results['failed']}/{results['total']}")
        print(f"📅 Timestamp: {results['timestamp']}")
        
        automation.export_results(results)
        print("\n✅ Kampagne abgeschlossen!")
    else:
        print("\n❌ Kampagne abgebrochen.")
