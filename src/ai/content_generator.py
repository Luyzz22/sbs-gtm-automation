#!/usr/bin/env python3
"""
KI-gestützter Content Generator für LinkedIn Posts
Nutzt OpenAI und Anthropic für verschiedene Content-Typen
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
from anthropic import Anthropic
from typing import Literal

load_dotenv()

class ContentGenerator:
    """Generiert LinkedIn Content mit KI"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.anthropic_client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.company_name = os.getenv('COMPANY_NAME', 'SBS Deutschland GmbH')
        
    def generate_linkedin_post(
        self,
        topic: str,
        style: Literal["professional", "casual", "educational", "storytelling"] = "professional",
        ai_provider: Literal["openai", "claude"] = "openai",
        max_length: int = 280
    ) -> dict:
        """
        Generiert einen LinkedIn Post
        
        Args:
            topic: Thema des Posts
            style: Schreibstil
            ai_provider: KI-Anbieter (openai oder claude)
            max_length: Maximale Zeichenanzahl
            
        Returns:
            dict mit 'content', 'hashtags', 'call_to_action'
        """
        
        prompt = self._build_prompt(topic, style, max_length)
        
        if ai_provider == "openai":
            response = self._generate_with_openai(prompt)
        else:
            response = self._generate_with_claude(prompt)
            
        return self._parse_response(response)
    
    def _build_prompt(self, topic: str, style: str, max_length: int) -> str:
        """Erstellt den Prompt für die KI"""
        
        style_descriptions = {
            "professional": "professionell, fachlich, seriös",
            "casual": "locker, persönlich, nahbar",
            "educational": "lehrreich, informativ, hilfreich",
            "storytelling": "Geschichte erzählend, emotional, packend"
        }
        
        return f"""Erstelle einen LinkedIn Post für {self.company_name}.

Thema: {topic}
Stil: {style_descriptions.get(style, "professionell")}
Maximale Länge: {max_length} Zeichen

Struktur:
1. Aufmerksamkeitsstarke erste Zeile
2. Hauptinhalt mit Mehrwert
3. 3-5 relevante Hashtags
4. Call-to-Action

Format:
[CONTENT]
Dein Post-Text hier...

[HASHTAGS]
#hashtag1 #hashtag2 #hashtag3

[CTA]
Dein Call-to-Action hier...

Schreibe auf Deutsch und halte dich an die Zeichenlimit!"""

    def _generate_with_openai(self, prompt: str) -> str:
        """Generiert Content mit OpenAI GPT-4"""
        response = self.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "Du bist ein LinkedIn Marketing Experte für B2B Software-Unternehmen."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=600
        )
        return response.choices[0].message.content
    
    def _generate_with_claude(self, prompt: str) -> str:
        """Generiert Content mit Anthropic Claude"""
        message = self.anthropic_client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=600,
            temperature=0.7,
            system="Du bist ein LinkedIn Marketing Experte für B2B Software-Unternehmen.",
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text
    
    def _parse_response(self, response: str) -> dict:
        """Parst die KI-Antwort in strukturierte Daten"""
        result = {
            "content": "",
            "hashtags": [],
            "call_to_action": ""
        }
        
        # Extrahiere Sections
        if "[CONTENT]" in response:
            content_start = response.find("[CONTENT]") + len("[CONTENT]")
            content_end = response.find("[HASHTAGS]") if "[HASHTAGS]" in response else response.find("[CTA]")
            result["content"] = response[content_start:content_end].strip()
        else:
            # Fallback: Nimm alles vor Hashtags
            lines = response.split('\n')
            content_lines = []
            for line in lines:
                if line.strip().startswith('#'):
                    break
                content_lines.append(line)
            result["content"] = '\n'.join(content_lines).strip()
        
        if "[HASHTAGS]" in response:
            hashtags_start = response.find("[HASHTAGS]") + len("[HASHTAGS]")
            hashtags_end = response.find("[CTA]") if "[CTA]" in response else len(response)
            hashtags_text = response[hashtags_start:hashtags_end].strip()
            result["hashtags"] = [tag.strip() for tag in hashtags_text.split() if tag.startswith('#')]
        
        if "[CTA]" in response:
            cta_start = response.find("[CTA]") + len("[CTA]")
            result["call_to_action"] = response[cta_start:].strip()
        
        return result

    def generate_content_series(self, main_topic: str, num_posts: int = 5) -> list:
        """Generiert eine Serie von Posts zu einem Hauptthema"""
        posts = []
        
        # Erstelle Unterthemen
        subtopics_prompt = f"""Erstelle {num_posts} spezifische Unterthemen für eine LinkedIn Content-Serie zum Thema "{main_topic}".
        
Liste nur die Themen auf, ein Thema pro Zeile, ohne Nummerierung."""

        response = self._generate_with_openai(subtopics_prompt)
        subtopics = [line.strip() for line in response.split('\n') if line.strip()][:num_posts]
        
        # Generiere Posts für jeden Subtopic
        for i, subtopic in enumerate(subtopics, 1):
            print(f"Generiere Post {i}/{num_posts}: {subtopic}...")
            post = self.generate_linkedin_post(
                topic=subtopic,
                style="educational" if i % 2 == 0 else "professional"
            )
            post["number"] = i
            post["subtopic"] = subtopic
            posts.append(post)
        
        return posts


if __name__ == "__main__":
    # Demo
    generator = ContentGenerator()
    
    print("🤖 SBS LinkedIn Content Generator")
    print("=" * 60)
    
    topic = "Künstliche Intelligenz in der Vertragsprüfung"
    
    print(f"\n📝 Generiere Post zum Thema: {topic}\n")
    
    post = generator.generate_linkedin_post(
        topic=topic,
        style="professional",
        ai_provider="openai"
    )
    
    print("✅ Post generiert!\n")
    print("=" * 60)
    print("CONTENT:")
    print(post["content"])
    print("\n" + "=" * 60)
    print("HASHTAGS:")
    print(" ".join(post["hashtags"]))
    print("\n" + "=" * 60)
    print("CALL-TO-ACTION:")
    print(post["call_to_action"])
    print("=" * 60)
