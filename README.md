> **Historischer interner Entwicklungsbestand.** Dieses Repository gehört nicht zu den vier aktuellen SBS-Kernangeboten. Es ist keine Freigabe für Outreach, Kundendatenverarbeitung oder produktiven Betrieb. Aktuelles Portfolio: [SBS Deutschland](https://sbsdeutschland.com/).
>
> Lokale SQLite-Dateien werden beim Start durch die vorhandenen `_init_db`-Methoden erzeugt und dürfen nicht versioniert werden. Die drei am 23.11.2026 geprüften aktuellen Datenbankdateien enthielten jeweils null Datensätze. Das ist keine Prüfung der gesamten Git-Historie oder alter Kopien.

# ⚡ SBS Nexus GTM Automation

**Enterprise Go-To-Market Automation für SBS Deutschland GmbH & Co. KG**
KI-gestützte Vertriebs-Automatisierung für das Steuerberater-Partnerprogramm.

🌐 [Live App](https://sbs-automation.streamlit.app/) · [SBS Nexus](https://www.sbsnexus.de) · [Homepage](https://sbsdeutschland.com/sbshomepage/) · [Partner](https://www.sbsnexus.de/partner) · [Demo buchen](https://calendly.com/ki-sbsdeutschland/sbs-nexus-30-minuten-discovery-call)

---

## ⚡ SBS Nexus Plattform

Das operative OS für den fertigenden Mittelstand – drei KI-Module:

| Modul | Funktion | USP |
|-------|----------|-----|
| **💰 Finance Intelligence** | KI-Rechnungsverarbeitung | 8 Sek · 99,2% · DATEV + SAP Export |
| **📄 Contract Intelligence** | KI-Vertragsanalyse | Klauselerkennung · Fristenmanagement · Risikoanalyse |
| **🔧 Technical Intelligence** | HydraulikDoc AI (RAG) | Datenblätter · Handbücher · Normen · Bosch Rexroth |

**Compliance:** DSGVO-konform · Server in Frankfurt · E-Rechnungspflicht 2025

## 🚀 GTM Automation Features

| Modul | Beschreibung |
|-------|-------------|
| 📧 **Email Automation** | KI-personalisierte Outreach für Steuerberater (GPT-4/Claude, Resend + SMTP) |
| ✍️ **LinkedIn Posts** | Content für SBS Deutschland & HydraulikDoc AI Pages (Enterprise-Ton) |
| 🎯 **Lead Generation** | Steuerberater finden, qualifizieren, Lead Scoring (Hunter.io + DATEV SmartExperts) |
| 📊 **Analytics** | Kampagnen-Performance, Template-Analyse, Pipeline-Tracking |
| ⚙️ **Einstellungen** | API Keys, YAML-Konfiguration, System-Status |

## 🎯 Zielmarkt

- **89.000 Steuerberater** in Deutschland · €21,3 Mrd. Marktvolumen
- Fokus: Digitale DATEV-Kanzleien (UO, Label-Träger)
- Sekundär: Fertigender Mittelstand (50-5.000 MA, DACH)
- **Partnerprogramm:** 15-25% Revenue Share · [sbsnexus.de/partner](https://www.sbsnexus.de/partner)

## 🔗 Links

| Resource | URL |
|----------|-----|
| **SBS Homepage** | [sbsdeutschland.com/sbshomepage/](https://sbsdeutschland.com/sbshomepage/) |
| **SBS Nexus** | [sbsnexus.de](https://www.sbsnexus.de) |
| **Contract AI** | [contract.sbsdeutschland.com](https://contract.sbsdeutschland.com/) |
| **Partner-Programm** | [sbsnexus.de/partner](https://www.sbsnexus.de/partner) |
| **LinkedIn SBS** | [/sbs-deutschland-gmbh-co-kg/](https://www.linkedin.com/company/sbs-deutschland-gmbh-co-kg/) |
| **LinkedIn HydraulikDoc** | [/hydraulikdoc-ai/](https://www.linkedin.com/company/hydraulikdoc-ai/) |
| **Live App** | [sbs-automation.streamlit.app](https://sbs-automation.streamlit.app/) |
| **Demo** | [Calendly](https://calendly.com/ki-sbsdeutschland/sbs-nexus-30-minuten-discovery-call) |

## ⚡ Quick Start

```bash
git clone https://github.com/Luyzz22/sbs-gtm-automation.git
cd sbs-gtm-automation
pip install -r requirements.txt
cp .env.example .env  # API Keys eintragen
streamlit run streamlit_app.py
```

## 🔑 API Keys

| Service | Zweck |
|---------|-------|
| OpenAI | GPT-4 Email- & Content-Generierung |
| Anthropic | Claude Enterprise Content |
| Resend | Email-Versand (API) |
| Hunter.io | Lead-Recherche & Email-Finder |

## 📁 Struktur

```
├── streamlit_app.py          # Haupt-Dashboard (SBS Nexus Branding)
├── automated_email_sender.py # Email-Engine (Steuerberater-Outreach)
├── config/
│   ├── icp_filters.yaml      # ICP: Steuerberater & Kanzleien
│   ├── message_templates.yaml # Email-Templates (StB, Digital, KMU)
│   └── content_calendar.yaml  # LinkedIn-Themen (E-Rechnung, DATEV, KI)
├── pages/
│   ├── 1_📧_Email_Automation.py
│   ├── 2_✍️_LinkedIn_Posts.py
│   ├── 3_🎯_Lead_Generation.py
│   ├── 4_📊_Analytics.py
│   └── 5_⚙️_Einstellungen.py
├── src/ai/
│   ├── content_generator.py       # LinkedIn KI-Content (SBS Nexus Kontext)
│   └── enterprise_content_generator.py  # Enterprise Thought Leadership
├── backend/
│   ├── email_service.py     # SMTP + Resend Dual-Versand
│   ├── linkedin_service.py  # LinkedIn Post Management
│   └── lead_service.py      # Lead-Datenbank & Scoring
└── data/                    # SQLite Datenbanken
```

## 🎨 Corporate Design

| Element | Wert |
|---------|------|
| **SBS Blue** | `#003856` |
| **SBS Yellow** | `#FFB900` |
| **SBS Orange** | `#F97316` |
| **Ton** | Enterprise-Standard (Apple, SAP, NVIDIA) |
| **Theme** | Dark Mode |

## 📋 GTM Arsenal — 13 Building Blocks

✅ GTM Playbook · ✅ Blog SEO-Artikel (2x live) · ✅ Steuerberater-Partnerschaftsstrategie · ✅ Partner Landing Page · ✅ Case Study Template · ✅ Webinar-Konzept · ✅ ROI-Infografik · ✅ LinkedIn Optimization Pack · ✅ Outreach Execution Kit · ✅ CRM Tracking Template · ✅ Prospect-Datenbank (50 Kontakte) · ✅ Sendefertige E-Mails (7 Prio A) · ✅ GTM Automation Tool

---

**SBS Deutschland GmbH & Co. KG** · Weinheim · Luis Orozco, Gründer & CEO · [sbsnexus.de](https://www.sbsnexus.de)

Version 3.0.0 · Enterprise Edition
