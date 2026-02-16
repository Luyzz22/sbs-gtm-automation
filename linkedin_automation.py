#!/usr/bin/env python3
"""
SBS LinkedIn Automation - Interaktives CLI Tool
Hauptsteuerung für alle LinkedIn Automation Features
"""

import os
import sys
from datetime import datetime
from dotenv import load_dotenv
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, Confirm
from rich.table import Table
from src.ai.content_generator import ContentGenerator

load_dotenv()
console = Console()

class LinkedInAutomationCLI:
    """Interaktives CLI für LinkedIn Automation"""
    
    def __init__(self):
        self.content_generator = ContentGenerator()
        self.generated_posts = []
    
    def show_banner(self):
        """Zeigt Banner"""
        banner = """
╔═══════════════════════════════════════════════════════╗
║   SBS DEUTSCHLAND - LINKEDIN AUTOMATION SYSTEM        ║
║   🤖 KI-gestützte Content Creation & Lead Generation  ║
╚═══════════════════════════════════════════════════════╝
        """
        console.print(banner, style="bold cyan")
        console.print(f"📅 {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
    
    def show_menu(self):
        """Zeigt Hauptmenü"""
        table = Table(show_header=False, box=None)
        table.add_row("1", "📝 LinkedIn Post generieren")
        table.add_row("2", "📚 Content-Serie erstellen (5 Posts)")
        table.add_row("3", "👀 Generierte Posts anzeigen")
        table.add_row("4", "💾 Post als Datei speichern")
        table.add_row("5", "⚙️  Einstellungen anzeigen")
        table.add_row("0", "❌ Beenden")
        
        console.print(Panel(table, title="Hauptmenü", border_style="blue"))
    
    def generate_single_post(self):
        """Generiert einzelnen Post"""
        console.print("\n[bold]📝 LinkedIn Post Generator[/bold]\n")
        
        # Input
        topic = Prompt.ask("Thema des Posts")
        
        style_options = {
            "1": "professional",
            "2": "casual", 
            "3": "educational",
            "4": "storytelling"
        }
        
        console.print("\nSchreibstil:")
        console.print("1. Professional (seriös, fachlich)")
        console.print("2. Casual (locker, persönlich)")
        console.print("3. Educational (lehrreich, informativ)")
        console.print("4. Storytelling (Geschichte erzählend)")
        
        style_choice = Prompt.ask("Wähle Stil", choices=["1","2","3","4"], default="1")
        style = style_options[style_choice]
        
        ai_choice = Prompt.ask("KI-Provider", choices=["openai", "claude"], default="openai")
        
        # Generiere
        with console.status("[bold green]Generiere Post mit KI..."):
            post = self.content_generator.generate_linkedin_post(
                topic=topic,
                style=style,
                ai_provider=ai_choice
            )
        
        # Speichere
        post["topic"] = topic
        post["style"] = style
        post["ai_provider"] = ai_choice
        post["timestamp"] = datetime.now().isoformat()
        self.generated_posts.append(post)
        
        # Zeige Ergebnis
        self._display_post(post)
        
        # Frage ob speichern
        if Confirm.ask("\n💾 Als Datei speichern?"):
            self.save_post_to_file(post)
    
    def generate_content_series(self):
        """Generiert Content-Serie"""
        console.print("\n[bold]📚 Content-Serie Generator[/bold]\n")
        
        main_topic = Prompt.ask("Hauptthema der Serie")
        num_posts = int(Prompt.ask("Anzahl Posts", default="5"))
        
        with console.status(f"[bold green]Generiere {num_posts} Posts..."):
            posts = self.content_generator.generate_content_series(main_topic, num_posts)
        
        # Speichere alle
        for post in posts:
            post["main_topic"] = main_topic
            post["timestamp"] = datetime.now().isoformat()
            self.generated_posts.append(post)
        
        console.print(f"\n✅ {len(posts)} Posts erfolgreich generiert!\n", style="bold green")
        
        # Zeige Preview
        for post in posts:
            console.print(f"[cyan]Post {post['number']}:[/cyan] {post['subtopic']}")
        
        if Confirm.ask("\n📖 Alle Posts im Detail anzeigen?"):
            for post in posts:
                self._display_post(post)
                if post != posts[-1]:  # Nicht bei letztem Post
                    Prompt.ask("\nWeiter mit Enter")
    
    def show_generated_posts(self):
        """Zeigt alle generierten Posts"""
        if not self.generated_posts:
            console.print("\n⚠️  Noch keine Posts generiert\n", style="yellow")
            return
        
        console.print(f"\n[bold]📋 Generierte Posts ({len(self.generated_posts)})[/bold]\n")
        
        for i, post in enumerate(self.generated_posts, 1):
            topic = post.get('topic') or post.get('subtopic', 'Unbekannt')
            timestamp = datetime.fromisoformat(post['timestamp']).strftime('%d.%m.%Y %H:%M')
            console.print(f"{i}. {topic} ({timestamp})")
        
        choice = Prompt.ask("\nPost anzeigen (Nummer) oder 0 für zurück", default="0")
        
        if choice != "0" and choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.generated_posts):
                self._display_post(self.generated_posts[idx])
    
    def save_post_to_file(self, post=None):
        """Speichert Post als Markdown-Datei"""
        if post is None:
            if not self.generated_posts:
                console.print("\n⚠️  Keine Posts zum Speichern\n", style="yellow")
                return
            post = self.generated_posts[-1]  # Letzter Post
        
        # Erstelle Dateiname
        topic = post.get('topic') or post.get('subtopic', 'post')
        filename = f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join("generated_content", filename)
        
        # Erstelle Ordner
        os.makedirs("generated_content", exist_ok=True)
        
        # Schreibe Datei
        content = f"""# LinkedIn Post

**Thema:** {topic}
**Erstellt:** {datetime.now().strftime('%d.%m.%Y %H:%M')}
**KI-Provider:** {post.get('ai_provider', 'N/A')}

---

## Content

{post['content']}

---

## Hashtags

{' '.join(post['hashtags'])}

---

## Call-to-Action

{post['call_to_action']}
"""
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        console.print(f"\n✅ Post gespeichert: [cyan]{filepath}[/cyan]\n", style="bold green")
    
    def show_settings(self):
        """Zeigt Einstellungen"""
        table = Table(title="⚙️  System-Einstellungen")
        table.add_column("Setting", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Company", os.getenv('COMPANY_NAME'))
        table.add_row("Domain", os.getenv('COMPANY_DOMAIN'))
        table.add_row("LinkedIn Email", os.getenv('LINKEDIN_EMAIL'))
        table.add_row("OpenAI API", "✅ Konfiguriert" if os.getenv('OPENAI_API_KEY') else "❌ Fehlt")
        table.add_row("Claude API", "✅ Konfiguriert" if os.getenv('ANTHROPIC_API_KEY') else "❌ Fehlt")
        table.add_row("Hunter.io API", "✅ Konfiguriert" if os.getenv('HUNTER_API_KEY') else "❌ Fehlt")
        table.add_row("Generierte Posts", str(len(self.generated_posts)))
        
        console.print("\n")
        console.print(table)
        console.print()
    
    def _display_post(self, post):
        """Zeigt einzelnen Post formatiert an"""
        console.print("\n" + "═" * 70)
        console.print(f"[bold cyan]📝 Post: {post.get('topic') or post.get('subtopic', 'Unbekannt')}[/bold cyan]")
        console.print("═" * 70)
        
        console.print("\n[bold]CONTENT:[/bold]")
        console.print(Panel(post['content'], border_style="blue"))
        
        console.print("\n[bold]HASHTAGS:[/bold]")
        console.print(" ".join(post['hashtags']), style="cyan")
        
        console.print("\n[bold]CALL-TO-ACTION:[/bold]")
        console.print(post['call_to_action'], style="green")
        
        console.print("═" * 70 + "\n")
    
    def run(self):
        """Hauptschleife"""
        self.show_banner()
        
        while True:
            self.show_menu()
            choice = Prompt.ask("\nWähle Option", default="0")
            
            if choice == "1":
                self.generate_single_post()
            elif choice == "2":
                self.generate_content_series()
            elif choice == "3":
                self.show_generated_posts()
            elif choice == "4":
                self.save_post_to_file()
            elif choice == "5":
                self.show_settings()
            elif choice == "0":
                console.print("\n👋 Auf Wiedersehen!\n", style="bold green")
                break
            else:
                console.print("\n⚠️  Ungültige Auswahl\n", style="yellow")
            
            if choice != "0":
                Prompt.ask("\nWeiter mit Enter")


if __name__ == "__main__":
    try:
        cli = LinkedInAutomationCLI()
        cli.run()
    except KeyboardInterrupt:
        console.print("\n\n👋 Programm beendet.\n", style="bold yellow")
        sys.exit(0)
