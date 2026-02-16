#!/usr/bin/env python3
"""
SBS GTM Automation - Hauptprogramm
Enterprise Go-To-Market Automation für SBS Deutschland
"""

import os
import sys
from pathlib import Path
from datetime import datetime
import yaml
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from dotenv import load_dotenv

console = Console()

# Lade .env
load_dotenv()

class SBSGTMAutomation:
    """Hauptklasse für SBS GTM Automation"""
    
    def __init__(self):
        self.base_path = Path(__file__).parent
        self.config_path = self.base_path / "config"
        
    def show_banner(self):
        """Zeige Banner"""
        banner = """
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║        SBS GTM AUTOMATION SYSTEM                          ║
║        Enterprise LinkedIn Marketing & Lead Generation    ║
║                                                           ║
║        © 2026 SBS Deutschland GmbH                        ║
╚═══════════════════════════════════════════════════════════╝
        """
        console.print(banner, style="bold cyan")
        
    def show_menu(self):
        """Zeige Hauptmenü"""
        table = Table(title="Hauptmenü", box=box.ROUNDED, style="cyan")
        table.add_column("Nr.", style="bold yellow", justify="center")
        table.add_column("Funktion", style="bold green")
        table.add_column("Beschreibung", style="white")
        
        table.add_row("1", "Content Automation", "LinkedIn Posts automatisch erstellen & veröffentlichen")
        table.add_row("2", "Lead Generation", "Potenzielle Kunden finden & ansprechen")
        table.add_row("3", "Analytics Dashboard", "Performance-Metriken & Reporting")
        table.add_row("4", "Konfiguration anzeigen", "Aktuelle Systemkonfiguration anzeigen")
        table.add_row("5", "System-Status", "API-Verbindungen & Setup prüfen")
        table.add_row("0", "Beenden", "Programm beenden")
        
        console.print(table)
        
    def load_content_calendar(self):
        """Lade Content-Kalender"""
        calendar_file = self.config_path / "content_calendar.yaml"
        if calendar_file.exists():
            with open(calendar_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return None
        
    def load_icp_filters(self):
        """Lade ICP-Filter"""
        icp_file = self.config_path / "icp_filters.yaml"
        if icp_file.exists():
            with open(icp_file, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        return None
        
    def show_configuration(self):
        """Zeige Konfiguration"""
        console.print("\n[bold cyan]═══ Systemkonfiguration ═══[/bold cyan]\n")
        
        # Content Calendar
        calendar = self.load_content_calendar()
        if calendar:
            console.print("[bold green]📅 Content Calendar:[/bold green]")
            schedule = calendar.get('schedule', {})
            console.print(f"  • Posting-Frequenz: {schedule.get('posting_frequency', 'N/A')}")
            console.print(f"  • Optimale Zeiten:")
            for time_slot in schedule.get('optimal_times', []):
                console.print(f"    - {time_slot.get('day')}: {time_slot.get('time')} ({time_slot.get('reason')})")
        
        # ICP Filters
        icp = self.load_icp_filters()
        if icp:
            console.print("\n[bold green]🎯 Ideal Customer Profile (ICP):[/bold green]")
            filters = icp.get('target_filters', {})
            console.print(f"  • Branchen: {', '.join(filters.get('industries', []))}")
            console.print(f"  • Unternehmensgröße: {filters.get('company_size', {}).get('min', 0)}-{filters.get('company_size', {}).get('max', 0)} Mitarbeiter")
            console.print(f"  • Region: {', '.join(filters.get('regions', []))}")
            
    def check_system_status(self):
        """Prüfe System-Status"""
        console.print("\n[bold cyan]═══ System-Status ═══[/bold cyan]\n")
        
        # API Keys
        openai_key = os.getenv("OPENAI_API_KEY")
        anthropic_key = os.getenv("ANTHROPIC_API_KEY")
        
        table = Table(box=box.SIMPLE)
        table.add_column("Komponente", style="bold")
        table.add_column("Status", justify="center")
        table.add_column("Details")
        
        # OpenAI
        if openai_key and len(openai_key) > 20:
            table.add_row("OpenAI API", "✓", f"Key: ...{openai_key[-8:]}")
        else:
            table.add_row("OpenAI API", "✗", "Nicht konfiguriert")
            
        # Anthropic
        if anthropic_key and len(anthropic_key) > 20:
            table.add_row("Anthropic API", "✓", f"Key: ...{anthropic_key[-8:]}")
        else:
            table.add_row("Anthropic API", "✗", "Nicht konfiguriert")
            
        # Config-Dateien
        config_files = ["content_calendar.yaml", "icp_filters.yaml", "message_templates.yaml"]
        for config_file in config_files:
            file_path = self.config_path / config_file
            if file_path.exists():
                table.add_row(f"Config: {config_file}", "✓", "Geladen")
            else:
                table.add_row(f"Config: {config_file}", "✗", "Nicht gefunden")
                
        console.print(table)
        
    def content_automation(self):
        """Content Automation Modul"""
        console.print("\n[bold cyan]═══ Content Automation ═══[/bold cyan]\n")
        console.print("[yellow]Diese Funktion erstellt automatisch LinkedIn-Posts basierend auf deinem Content-Kalender.[/yellow]\n")
        
        calendar = self.load_content_calendar()
        if not calendar:
            console.print("[red]✗ Content-Kalender nicht gefunden![/red]")
            return
            
        console.print("[green]✓ Content-Kalender geladen[/green]")
        console.print("\n[bold]Nächste geplante Posts:[/bold]")
        
        # Zeige Content-Themen
        themes = calendar.get('content_themes', [])
        for i, theme in enumerate(themes[:5], 1):
            console.print(f"{i}. {theme.get('title', 'Unbekannt')}")
            console.print(f"   Kategorie: {theme.get('category', 'N/A')}")
            console.print(f"   Keywords: {', '.join(theme.get('keywords', []))}\n")
            
        console.print("[italic]Hinweis: Die vollständige Implementierung benötigt LinkedIn API-Zugriff.[/italic]")
        
    def lead_generation(self):
        """Lead Generation Modul"""
        console.print("\n[bold cyan]═══ Lead Generation ═══[/bold cyan]\n")
        console.print("[yellow]Diese Funktion findet potenzielle Kunden basierend auf deinem ICP.[/yellow]\n")
        
        icp = self.load_icp_filters()
        if not icp:
            console.print("[red]✗ ICP-Filter nicht gefunden![/red]")
            return
            
        console.print("[green]✓ ICP-Filter geladen[/green]")
        
        # Zeige Zielgruppe
        filters = icp.get('target_filters', {})
        console.print("\n[bold]Zielgruppen-Definition:[/bold]")
        console.print(f"• Positionen: {', '.join(filters.get('job_titles', []))}")
        console.print(f"• Branchen: {', '.join(filters.get('industries', []))}")
        console.print(f"• Unternehmensgröße: {filters.get('company_size', {}).get('min')}-{filters.get('company_size', {}).get('max')} Mitarbeiter")
        
        # Ausschluss-Kriterien
        exclusions = icp.get('exclusion_criteria', {})
        console.print(f"\n• Ausschlüsse:")
        console.print(f"  - Keywords: {', '.join(exclusions.get('keywords', []))}")
        console.print(f"  - Branchen: {', '.join(exclusions.get('industries', []))}")
        
        console.print("\n[italic]Hinweis: Die vollständige Implementierung benötigt LinkedIn Sales Navigator API.[/italic]")
        
    def analytics_dashboard(self):
        """Analytics Dashboard"""
        console.print("\n[bold cyan]═══ Analytics Dashboard ═══[/bold cyan]\n")
        console.print("[yellow]Hier siehst du Performance-Metriken und KPIs.[/yellow]\n")
        
        # Mock-Daten
        table = Table(title="Performance Übersicht", box=box.ROUNDED)
        table.add_column("Metrik", style="bold")
        table.add_column("Wert", justify="right", style="green")
        table.add_column("Trend", justify="center")
        
        table.add_row("LinkedIn Posts (30 Tage)", "8", "↑")
        table.add_row("Durchschn. Engagement", "4.2%", "↑")
        table.add_row("Neue Leads", "23", "↑")
        table.add_row("Antwortquote", "31%", "↓")
        table.add_row("Pipeline-Value", "€45.000", "↑")
        
        console.print(table)
        console.print("\n[italic]Hinweis: Dies sind Beispiel-Daten. Echte Metriken werden nach API-Anbindung angezeigt.[/italic]")
        
    def run(self):
        """Hauptprogramm ausführen"""
        self.show_banner()
        
        while True:
            self.show_menu()
            
            try:
                choice = console.input("\n[bold cyan]Wähle eine Option (0-5):[/bold cyan] ").strip()
                
                if choice == "0":
                    console.print("\n[green]Auf Wiedersehen! 👋[/green]\n")
                    sys.exit(0)
                elif choice == "1":
                    self.content_automation()
                elif choice == "2":
                    self.lead_generation()
                elif choice == "3":
                    self.analytics_dashboard()
                elif choice == "4":
                    self.show_configuration()
                elif choice == "5":
                    self.check_system_status()
                else:
                    console.print("[red]✗ Ungültige Auswahl! Bitte wähle 0-5.[/red]")
                    
                console.input("\n[dim]Drücke Enter um fortzufahren...[/dim]")
                console.clear()
                self.show_banner()
                
            except KeyboardInterrupt:
                console.print("\n\n[yellow]Programm wird beendet...[/yellow]")
                sys.exit(0)
            except Exception as e:
                console.print(f"\n[red]✗ Fehler: {e}[/red]")

if __name__ == "__main__":
    app = SBSGTMAutomation()
    app.run()
