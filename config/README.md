# Configuration Files

Zentraler Ordner für alle Konfigurationsdateien der SBS GTM Automation.

## Struktur:

### ICP-Definition
- `icp_filters.yaml` - Ideal Customer Profile Filter
  - Branche, Unternehmensgröße, Region, Technologie-Stack
  - Sales Navigator Such-Parameter

### Message Templates
- `message_templates.yaml` - Outreach-Nachrichten
  - CFO Template
  - CTO Template  
  - Geschäftsführer Template
  - Follow-up Sequenzen

### Content Calendar
- `content_calendar.yaml` - LinkedIn Posting-Plan
  - Post-Templates
  - Hashtag-Strategie
  - Timing-Konfiguration

### API Credentials (nicht im Git!)
- `linkedin_credentials.json` - OAuth Tokens
- `clearbit_api_key.txt` - Enrichment API
- `hubspot_api_key.txt` - CRM Integration

## Sicherheit:
⚠️ **Alle Credentials sind in .gitignore ausgeschlossen!**

- Secrets werden via GitHub Secrets oder Environment Variables geladen
- Niemals API-Keys in diesem Ordner committen
- Template-Dateien mit `.example` Suffix für Dokumentation

## Beispiel:

```yaml
# icp_filters.yaml.example
icp:
  company_size: "50-500"
  industries:
    - Maschinenbau
    - Automotive
  region: "Baden-Württemberg"
  technologies:
    - DATEV
    - SAP
```
