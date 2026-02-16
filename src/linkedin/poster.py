#!/usr/bin/env python3
"""
LinkedIn Poster - WARNUNG: Inoffizielle API!
Nutzt linkedin-api Package (gegen LinkedIn ToS)
Nur für Entwicklung/Testing - produktiv manuell posten!
"""

import os
from dotenv import load_dotenv
from linkedin_api import Linkedin
import time

load_dotenv()

class LinkedInPoster:
    """LinkedIn Post Automation (VORSICHT: Gegen ToS!)"""
    
    def __init__(self):
        self.email = os.getenv('LINKEDIN_EMAIL')
        self.password = os.getenv('LINKEDIN_PASSWORD')
        self.api = None
        
    def login(self):
        """Login zu LinkedIn (kann Account-Risiko bedeuten!)"""
        print("⚠️  WARNUNG: Inoffizielle LinkedIn API")
        print("   → Kann zu Account-Sperrung führen")
        print("   → Nur für Testing geeignet")
        
        try:
            self.api = Linkedin(self.email, self.password)
            print("✅ LinkedIn Login erfolgreich")
            return True
        except Exception as e:
            print(f"❌ Login fehlgeschlagen: {e}")
            return False
    
    def post_update(self, text: str, dry_run: bool = True):
        """
        Postet ein Status-Update
        
        Args:
            text: Post-Content
            dry_run: Wenn True, nur simulieren (EMPFOHLEN!)
        """
        if dry_run:
            print("\n🧪 DRY RUN MODE (kein echter Post)")
            print("─" * 60)
            print(text)
            print("─" * 60)
            print("✅ Post würde gesendet werden")
            return
        
        if not self.api:
            print("❌ Nicht eingeloggt!")
            return
        
        try:
            # VORSICHT: Echter Post!
            self.api.post_update(text)
            print("✅ Post erfolgreich auf LinkedIn")
            time.sleep(5)  # Rate limiting
        except Exception as e:
            print(f"❌ Post fehlgeschlagen: {e}")


def safe_demo():
    """Sichere Demo - nur Anzeige"""
    print("🔒 SICHERE ALTERNATIVE: Manuelle Posts")
    print("\n1. Content mit KI generieren ✅")
    print("2. Post in generated_content/ speichern ✅")
    print("3. Auf LinkedIn kopieren und manuell posten")
    print("\nVorteile:")
    print("• Kein Account-Risiko")
    print("• Volle Kontrolle")
    print("• Bilder/Medien hinzufügen")


if __name__ == "__main__":
    safe_demo()
