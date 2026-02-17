#!/usr/bin/env python3
"""
Enterprise Content Generator V2
Optimiert für CFO/C-Level LinkedIn Posts
- Professioneller Ton
- Datengetrieben
- Optimale Länge (1300-2000 Zeichen für maximales Engagement)
- Strukturierter Aufbau
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from typing import Literal, Optional

load_dotenv()

class EnterpriseContentGenerator:
    """
    Enterprise-Grade LinkedIn Content Generator
    Spezialisiert auf C-Level B2B Content
    """
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.company_name = os.getenv('COMPANY_NAME', 'SBS Deutschland GmbH')
        self.company_domain = os.getenv('COMPANY_DOMAIN', 'sbsdeutschland.com')
        
    def generate_cfo_post(
        self,
        topic: str,
        target_length: Literal["optimal", "short", "long"] = "optimal",
        include_data: bool = True,
        ai_provider: Literal["openai", "claude"] = "openai"
    ) -> dict:
        """
        Generiert Enterprise-optimierten LinkedIn Post
        
        Args:
            topic: Thema des Posts
            target_length: 
                - "optimal": 1300-1700 Zeichen (beste Engagement)
                - "short": 800-1000 Zeichen
                - "long": 2000-2500 Zeichen
            include_data: Fügt Statistiken/Zahlen hinzu
            ai_provider: KI-Anbieter
            
        Returns:
            dict mit strukturiertem Content
        """
        
        prompt = self._build_enterprise_prompt(topic, target_length, include_data)
        
        if ai_provider == "openai":
            response = self._generate_with_openai_enterprise(prompt)
        else:
            response = self._generate_with_claude_enterprise(prompt)
            
        return self._parse_enterprise_response(response, topic)
    
    def _build_enterprise_prompt(
        self, 
        topic: str, 
        target_length: str,
        include_data: bool
    ) -> str:
        """Erstellt optimierten Prompt für Enterprise Content"""
        
        length_specs = {
            "optimal": "1300-1700 Zeichen (optimal für LinkedIn Engagement)",
            "short": "800-1000 Zeichen (kompakt, schnell lesbar)",
            "long": "2000-2500 Zeichen (ausführlich, thought leadership)"
        }
        
        return f"""Du bist Luis Orozco, Gründer & CEO von {self.company_name}, einem Enterprise-SaaS-Anbieter für KI-gestützte Dokumentenverarbeitung.

**AUFGABE:** Erstelle einen LinkedIn Post für ein B2B-Publikum.

**THEMA:** {topic}

**UNTERNEHMEN – SBS Deutschland GmbH & Co. KG:**
- Plattform: SBS Nexus – Das operative OS für den Mittelstand
- Modul 1: Finance Intelligence (KI-Rechnungsverarbeitung, 8 Sek, 99,2%, DATEV + SAP Export)
- Modul 2: Contract Intelligence (KI-Vertragsanalyse, Klauselerkennung, Fristenmanagement)
- Modul 3: Technical Intelligence / HydraulikDoc AI (Technische Dokumenten-KI, RAG)
- Partnerprogramm: 15-25% Revenue Share für Steuerberater → www.sbsnexus.de/partner
- Websites: www.sbsnexus.de | sbsdeutschland.com/sbshomepage/ | contract.sbsdeutschland.com
- Demo: calendly.com/ki-sbsdeutschland/sbs-nexus-30-minuten-discovery-call
- Compliance: DSGVO-konform, Server in Frankfurt
- LinkedIn: /sbs-deutschland-gmbh-co-kg/ | /hydraulikdoc-ai/

**ZIELGRUPPE:**
- Steuerberater & Kanzleiinhaber (89.000 in Deutschland, €21,3 Mrd. Markt)
- CFOs, CTOs, Geschäftsführer im fertigenden Mittelstand
- 50-5.000 Mitarbeiter, DACH-Region
- DATEV 90%+ Marktanteil, E-Rechnungspflicht seit Januar 2025

**TON & STIL:**
- Enterprise-Standard (Apple, SAP, NVIDIA Niveau)
- Thought Leadership mit konkreten Zahlen
- Lösungsorientiert, authentisch und glaubwürdig
- Persönliche Perspektive als Gründer
- SBS Nexus und Module aktiv nennen

**STRUKTUR:**

[HOOK]
Aufmerksamkeitsstarke erste Zeile (max 65 Zeichen)
→ Provokante These oder überraschende Zahl

[CONTEXT]
2-3 Sätze Kontext zum Thema
→ Warum ist das relevant? Welches Problem?
{\"→ Nutze konkrete Zahlen/Statistiken aus dem SBS Nexus Markt\" if include_data else \"\"}

[INSIGHT]
Deine Perspektive als SBS Deutschland Gründer
→ Was hast du beim Aufbau von SBS Nexus gelernt?
→ Praktische Erkenntnis aus dem Steuerberater-Markt

[VALUE]
Mehrwert für den Leser
→ Was kann der Leser konkret mitnehmen?
→ Actionable Insight mit Bezug zu SBS Nexus Modulen

[CTA]
Call-to-Action
→ Link zu sbsnexus.de, Partner-Seite oder Calendly Demo

[HASHTAGS]
3-5 Hashtags: #SBSNexus #ERechnung #Steuerberater #DATEV #KI #Mittelstand #HydraulikDoc

**LÄNGE:** {length_specs[target_length]}

Liefere den Post im oben genannten Format."""

    def _generate_with_openai_enterprise(self, prompt: str) -> str:
        """Generiert Content mit GPT-4 (Enterprise-optimiert)"""
        response = self.openai_client.chat.completions.create(
            model="gpt-4o",  # Besseres Modell für Enterprise Content
            messages=[
                {
                    "role": "system", 
                    "content": f"""Du bist Luis Orozco, Gründer & CEO von {self.company_name}. 
                    Du leitest SBS Nexus – eine KI-Plattform für Rechnungsverarbeitung, Vertragsanalyse und technische Dokumenten-KI.
                    Du schreibst authentische, datengetriebene LinkedIn Posts auf Enterprise-Niveau (Apple/SAP/NVIDIA Standard).
                    Dein Fokus: Steuerberater-Markt, DATEV-Integration, E-Rechnungspflicht, fertigender Mittelstand."""
                },
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1500,
            top_p=0.9,
            frequency_penalty=0.3,
            presence_penalty=0.3
        )
        return response.choices[0].message.content
    
    def _generate_with_claude_enterprise(self, prompt: str) -> str:
        """Generiert Content mit Claude (Enterprise-optimiert)"""
        message = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1500,
            temperature=0.7,
            system=f"""Du bist Luis Orozco, Gründer & CEO von {self.company_name}.
            Du leitest SBS Nexus – eine KI-Plattform für Rechnungsverarbeitung, Vertragsanalyse und technische Dokumenten-KI.
            Du schreibst authentische, datengetriebene LinkedIn Posts auf Enterprise-Niveau (Apple/SAP/NVIDIA Standard).
            Dein Fokus: Steuerberater-Markt, DATEV-Integration, E-Rechnungspflicht, fertigender Mittelstand.""",
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    def _parse_enterprise_response(self, response: str, topic: str) -> dict:
        """Parst KI-Antwort in strukturierte Enterprise-Daten"""
        result = {
            "topic": topic,
            "hook": "",
            "content": "",
            "hashtags": [],
            "cta": "",
            "full_post": "",
            "word_count": 0,
            "char_count": 0,
            "estimated_read_time": 0
        }
        
        # Extrahiere Sections
        sections = {
            "HOOK": "",
            "CONTEXT": "",
            "INSIGHT": "",
            "VALUE": "",
            "CTA": "",
            "HASHTAGS": []
        }
        
        current_section = None
        lines = response.split('\n')
        
        for line in lines:
            if '[HOOK]' in line or '**HOOK**' in line:
                current_section = "HOOK"
                continue
            elif '[CONTEXT]' in line or '**CONTEXT**' in line:
                current_section = "CONTEXT"
                continue
            elif '[INSIGHT]' in line or '**INSIGHT**' in line:
                current_section = "INSIGHT"
                continue
            elif '[VALUE]' in line or '**VALUE**' in line:
                current_section = "VALUE"
                continue
            elif '[CTA]' in line or '**CTA**' in line:
                current_section = "CTA"
                continue
            elif '[HASHTAGS]' in line or '**HASHTAGS**' in line:
                current_section = "HASHTAGS"
                continue
            
            if current_section and line.strip():
                if current_section == "HASHTAGS":
                    # Extrahiere Hashtags
                    hashtags = [tag.strip() for tag in line.split() if tag.startswith('#')]
                    sections["HASHTAGS"].extend(hashtags)
                else:
                    sections[current_section] += line.strip() + "\n"
        
        # Baue finalen Post zusammen
        result["hook"] = sections["HOOK"].strip()
        
        content_parts = [
            sections["HOOK"].strip(),
            "",  # Leerzeile nach Hook
            sections["CONTEXT"].strip(),
            "",
            sections["INSIGHT"].strip(),
            "",
            sections["VALUE"].strip()
        ]
        
        result["content"] = "\n".join([p for p in content_parts if p])
        result["cta"] = sections["CTA"].strip()
        result["hashtags"] = sections["HASHTAGS"][:5]  # Max 5 Hashtags
        
        # Vollständiger Post
        full_post_parts = [
            result["content"],
            "",
            result["cta"],
            "",
            " ".join(result["hashtags"])
        ]
        
        result["full_post"] = "\n".join([p for p in full_post_parts if p])
        
        # Metriken
        result["char_count"] = len(result["full_post"])
        result["word_count"] = len(result["full_post"].split())
        result["estimated_read_time"] = max(1, result["word_count"] // 200)  # Minuten
        
        return result
    
    def optimize_for_engagement(self, post_data: dict) -> dict:
        """Optimiert Post für maximales Engagement"""
        
        # LinkedIn Best Practices
        engagement_score = 100
        issues = []
        recommendations = []
        
        char_count = post_data["char_count"]
        
        # Längen-Check
        if char_count < 800:
            engagement_score -= 15
            issues.append("Zu kurz - weniger Sichtbarkeit im Feed")
            recommendations.append("Erweitere auf 1300-1700 Zeichen")
        elif 1300 <= char_count <= 2000:
            engagement_score += 10
            recommendations.append("✅ Optimale Länge für Engagement")
        elif char_count > 2500:
            engagement_score -= 10
            issues.append("Zu lang - Leser könnten abspringen")
            recommendations.append("Kürze auf max 2000 Zeichen")
        
        # Hashtag-Check
        hashtag_count = len(post_data["hashtags"])
        if hashtag_count < 3:
            engagement_score -= 5
            issues.append("Zu wenige Hashtags")
            recommendations.append("Nutze 3-5 Hashtags")
        elif 3 <= hashtag_count <= 5:
            engagement_score += 5
            recommendations.append("✅ Optimale Hashtag-Anzahl")
        
        # Hook-Check
        hook_length = len(post_data["hook"])
        if hook_length > 100:
            engagement_score -= 10
            issues.append("Hook zu lang - sollte in einer Zeile lesbar sein")
            recommendations.append("Kürze Hook auf max 65 Zeichen")
        elif hook_length <= 65:
            engagement_score += 10
            recommendations.append("✅ Hook perfekt für mobile Ansicht")
        
        post_data["engagement_score"] = engagement_score
        post_data["issues"] = issues
        post_data["recommendations"] = recommendations
        
        return post_data


if __name__ == "__main__":
    from rich.console import Console
    from rich.panel import Panel
    
    console = Console()
    
    console.print("\n🏢 Enterprise Content Generator V2\n", style="bold cyan")
    
    generator = EnterpriseContentGenerator()
    
    # Demo
    topic = "Wie CFOs mit KI-gestützter Vertragsanalyse 40% Zeit sparen"
    
    console.print(f"📝 Generiere Enterprise Post: [cyan]{topic}[/cyan]\n")
    
    post = generator.generate_cfo_post(
        topic=topic,
        target_length="optimal",
        include_data=True,
        ai_provider="openai"
    )
    
    # Optimiere
    post = generator.optimize_for_engagement(post)
    
    # Ausgabe
    console.print("="*70)
    console.print(Panel(post["full_post"], title="📄 Enterprise LinkedIn Post", border_style="blue"))
    
    console.print(f"\n📊 Metriken:")
    console.print(f"   Zeichen: {post['char_count']}")
    console.print(f"   Wörter: {post['word_count']}")
    console.print(f"   Lesezeit: ~{post['estimated_read_time']} Min")
    console.print(f"   Engagement Score: {post['engagement_score']}/100")
    
    if post["recommendations"]:
        console.print(f"\n💡 Empfehlungen:")
        for rec in post["recommendations"]:
            console.print(f"   • {rec}")
    
    console.print("\n" + "="*70 + "\n")
