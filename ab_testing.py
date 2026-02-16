#!/usr/bin/env python3
"""
A/B Testing System für Email Subject Lines
Automatische Optimierung basierend auf Performance
"""
import random
from automated_email_sender import SBSEmailAutomation
import pandas as pd
from datetime import datetime

class ABTestingEmailAutomation(SBSEmailAutomation):
    """Erweiterte Automation mit A/B Testing"""
    
    def __init__(self):
        super().__init__(use_resend=True)
        self.ab_results = []
    
    def select_subject_variant(self, template):
        """Wählt zufällig eine Subject-Variante für A/B Test"""
        variant = random.choice(template['subject_variants'])
        variant_index = template['subject_variants'].index(variant)
        return variant, f"variant_{variant_index}"
    
    def send_campaign_with_ab_test(self, contacts, delay_seconds=120):
        """Sendet Kampagne mit A/B Testing"""
        templates = self.load_templates()
        
        results = {
            'timestamp': datetime.now().isoformat(),
            'sent': 0,
            'failed': 0,
            'total': len(contacts),
            'details': []
        }
        
        print(f"\n🧪 A/B Testing aktiviert - {len(contacts)} Kontakte")
        print(f"📊 Jeder Kontakt erhält zufällige Subject-Variante\n")
        
        for idx, contact in enumerate(contacts, 1):
            template = self.select_template(contact.get('role', 'CEO'), templates)
            
            # A/B Test: Zufällige Subject-Variante
            subject_variant, variant_id = self.select_subject_variant(template)
            
            # Rest der Nachricht personalisieren
            msg_parts = template['message']
            sections = []
            for key in ['opening', 'value_proposition', 'pain_point', 
                       'technical_specs', 'business_case', 'social_proof', 'cta', 'signature']:
                if key in msg_parts:
                    sections.append(msg_parts[key])
            
            body = "\n\n".join(sections)
            
            # Personalisierung
            replacements = {
                'first_name': contact.get('first_name', ''),
                'company_name': contact.get('company_name', ''),
                'sender_name': self.sender_name,
                'sender_title': self.sender_title,
            }
            
            for key, value in replacements.items():
                subject_variant = subject_variant.replace(f"{{{{{key}}}}}", str(value))
                body = body.replace(f"{{{{{key}}}}}", str(value))
            
            print(f"[{idx}/{len(contacts)}] {contact['email']}")
            print(f"   Variante: {variant_id}")
            print(f"   Subject: {subject_variant}")
            
            success = self.send_email(contact['email'], subject_variant, body)
            
            result_entry = {
                'email': contact['email'],
                'company': contact.get('company_name', 'Unknown'),
                'status': 'sent' if success else 'failed',
                'timestamp': datetime.now().isoformat(),
                'template': template['id'],
                'ab_variant': variant_id,
                'subject': subject_variant
            }
            
            results['details'].append(result_entry)
            
            if success:
                results['sent'] += 1
            else:
                results['failed'] += 1
            
            if idx < len(contacts):
                print(f"   ⏳ Warte {delay_seconds}s...\n")
                time.sleep(delay_seconds)
        
        return results
    
    def export_ab_results(self, results, filename='ab_test_results.csv'):
        """Exportiert A/B Test Ergebnisse"""
        df = pd.DataFrame(results['details'])
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"\n📊 A/B Test Ergebnisse: {filename}")


# Test mit 3 Kontakten
if __name__ == "__main__":
    contacts = [
        {
            'email': 'test1@example.de',
            'first_name': 'Test',
            'company_name': 'Test GmbH',
            'role': 'CFO'
        }
    ]
    
    ab_automation = ABTestingEmailAutomation()
    results = ab_automation.send_campaign_with_ab_test(contacts)
    ab_automation.export_ab_results(results)
    
    print("\n✅ A/B Testing System aktiviert!")
