import streamlit as st
import os
import yaml
from pathlib import Path
from datetime import datetime
import time

st.set_page_config(page_title="SBS Nexus – LinkedIn Posts", page_icon="✍️")

st.title("✍️ SBS Nexus LinkedIn Automation")
st.caption("Content für SBS Deutschland & HydraulikDoc AI LinkedIn Pages")

# Load Config
config_path = Path("config")
calendar_file = config_path / "content_calendar.yaml"

if not calendar_file.exists():
    st.error("❌ config/content_calendar.yaml nicht gefunden!")
    st.stop()

try:
    with open(calendar_file, 'r', encoding='utf-8') as f:
        calendar = yaml.safe_load(f)
except Exception as e:
    st.error(f"❌ Fehler beim Laden: {str(e)}")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("⚙️ Post-Einstellungen")

    openai_key = st.text_input("OpenAI API Key", type="password", value=os.getenv('OPENAI_API_KEY', ''))

    tone = st.selectbox("Tonalität", [
        "Thought Leadership",
        "Professionell / Informativ",
        "Praxis-orientiert / How-To",
        "Provokant / Kontrovers"
    ])
    length = st.slider("Länge (Wörter)", 100, 400, 250)

    st.markdown("---")
    linkedin_page = st.selectbox("LinkedIn Page", [
        "SBS Deutschland GmbH",
        "HydraulikDoc AI"
    ])

    st.markdown("---")
    st.markdown("### 🔗 Pages")
    st.markdown("""
    - [SBS Deutschland](https://www.linkedin.com/company/sbs-deutschland-gmbh-co-kg/)
    - [HydraulikDoc AI](https://www.linkedin.com/company/hydraulikdoc-ai/)
    """)


def generate_with_openai(prompt, system_prompt="Du bist LinkedIn Content-Experte."):
    if not openai_key:
        raise ValueError("API Key fehlt")
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=800
    )
    return response.choices[0].message.content.strip()


# Main Content
tab1, tab2, tab3, tab4 = st.tabs(["📝 Neuer Post", "📚 Post-Serie", "📅 Content-Kalender", "📊 Hashtag-Strategie"])

with tab1:
    st.subheader("SBS Nexus Post generieren")

    themes = calendar.get('content_themes', [])

    if not themes:
        st.warning("⚠️ Keine Content-Themen gefunden!")
        st.stop()

    col1, col2 = st.columns([2, 1])

    with col1:
        theme_options = {f"{t['title']} ({t['category']})": t for t in themes}
        selected_theme = st.selectbox("Content-Thema", options=list(theme_options.keys()))

        if selected_theme:
            theme = theme_options[selected_theme]
            st.info(f"**Kategorie:** {theme.get('category', 'N/A')}")
            st.write(f"**Kontext:** {theme.get('context', 'N/A')}")
            st.write(f"**Keywords:** {', '.join(theme.get('keywords', []))}")

    with col2:
        st.metric("Empfohlene Länge", f"{length} Wörter")
        st.metric("LinkedIn Page", linkedin_page)

    custom_prompt = st.text_area("Zusätzliche Anweisungen (optional)",
                                  placeholder="z.B. Erwähne konkrete Zahlen, beziehe dich auf E-Rechnungspflicht...",
                                  height=80)

    if st.button("✨ Post generieren", type="primary", use_container_width=True):
        if not openai_key:
            st.error("❌ Bitte OpenAI API Key eingeben!")
        else:
            with st.spinner("🤖 Generiere LinkedIn Post..."):
                try:
                    theme = theme_options[selected_theme]

                    page_context = ""
                    if linkedin_page == "SBS Deutschland GmbH":
                        page_context = """
UNTERNEHMEN: SBS Deutschland GmbH & Co. KG (Weinheim, Rhein-Neckar)
PLATTFORM: SBS Nexus – Das operative OS für den fertigenden Mittelstand
3 MODULE:
  1. Finance Intelligence: KI-Rechnungsverarbeitung (8 Sek, 99,2%, DATEV + SAP Export)
  2. Contract Intelligence: KI-Vertragsanalyse (Klauselerkennung, Fristenmanagement, Risikoanalyse) → contract.sbsdeutschland.com
  3. Technical Intelligence / HydraulikDoc AI: Technische Dokumenten-KI (RAG für Datenblätter, Handbücher, Normen)
ZIELGRUPPE: Steuerberater (89.000 in DE), fertigender Mittelstand (50-5.000 MA), KMU-Finanzentscheider
PARTNERPROGRAMM: 15-25% Revenue Share für Steuerberater-Partner → www.sbsnexus.de/partner
WEBSITES: www.sbsnexus.de | sbsdeutschland.com/sbshomepage/ | contract.sbsdeutschland.com
DEMO: calendly.com/ki-sbsdeutschland/sbs-nexus-30-minuten-discovery-call
COMPLIANCE: DSGVO-konform, Server in Frankfurt, E-Rechnungspflicht 2025
DIFFERENZIERUNG: Multimodale KI (nicht regelbasierte OCR), SAP + DATEV Integration, 100% deutsche Server
MARKT: €21,3 Mrd. Steuerberatung | DATEV 90%+ Marktanteil | Rhein-Neckar Industrieregion
INTEGRATIONEN: DATEV UO, SAP S/4HANA, n8n Workflows, REST API, Webhooks, Batch Processing"""
                    else:
                        page_context = """
UNTERNEHMEN: HydraulikDoc AI (Technical Intelligence Modul von SBS Nexus / SBS Deutschland GmbH & Co. KG)
PRODUKT: KI-gestützte technische Dokumenten-Analyse (RAG-Architektur)
USP: Beantwortet komplexe Servicefragen aus 80-Seiten Datenblättern in Sekunden
ZIELGRUPPE: Serviceteams, Instandhaltung, Maschinenbau, Industriehydraulik
TECHNOLOGIE: RAG Stack (LangChain + Vector-DB), Embeddings, PDF-Chunking
BEISPIEL-QUELLEN: Bosch Rexroth, Herstellerdatenblätter, DIN-Normen, interne Manuals
ANWENDUNGSFÄLLE: Prüfdrucke ermitteln, Dichtungsarten vergleichen, Medienkompatibilität prüfen
WEBSITES: sbsdeutschland.com/sbshomepage/ | www.sbsnexus.de
DEMO: calendly.com/ki-sbsdeutschland/sbs-nexus-30-minuten-discovery-call
MUTTERPLATTFORM: SBS Nexus (Finance + Contract + Technical Intelligence)"""

                    prompt = f"""Erstelle einen professionellen LinkedIn-Post:

{page_context}

THEMA: {theme['title']}
KATEGORIE: {theme.get('category', 'Business')}
KONTEXT: {theme.get('context', '')}
KEYWORDS: {', '.join(theme.get('keywords', []))}

TONALITÄT: {tone}
LÄNGE: Ca. {length} Wörter

STIL-VORGABEN:
- Enterprise-Standard (Apple, SAP, NVIDIA Niveau)
- Thought Leadership für deutschen Mittelstand & Steuerberater-Markt
- Konkrete Zahlen und Fakten verwenden
- Kein generisches Marketing-Blabla
- Authentisch, nicht werblich
- Bezug auf die 3 Module (Finance, Contract, Technical) wo passend

STRUKTUR:
1. Hook (provokant oder überraschend)
2. Problemdarstellung mit Marktdaten
3. Lösung mit konkretem Nutzen
4. Social Proof oder Zahlen
5. Call-to-Action (subtil, Link zu sbsnexus.de oder Calendly)
6. 3-5 relevante Hashtags

HASHTAGS bevorzugt: #SBSNexus #ERechnung #Steuerberater #DATEV #KI #Mittelstand #HydraulikDoc

{f"ZUSATZ: {custom_prompt}" if custom_prompt else ""}

Schreibe NUR den Post, keine Meta-Kommentare."""

                    post_content = generate_with_openai(
                        prompt,
                        "Du bist LinkedIn Content-Stratege für B2B Enterprise SaaS im deutschen Steuerberater-Markt. Du schreibst auf dem Niveau von Apple, SAP und NVIDIA Corporate Communications."
                    )

                    st.session_state['generated_post'] = post_content
                    st.session_state['post_theme'] = theme['title']
                    st.success("✅ Post erfolgreich generiert!")
                    st.rerun()

                except Exception as e:
                    st.error(f"❌ Fehler: {str(e)}")

    if 'generated_post' in st.session_state:
        st.markdown("---")
        st.subheader("📄 Generierter Post")

        post_text = st.text_area(
            "Post-Text (editierbar)",
            value=st.session_state['generated_post'],
            height=350,
            key="post_display"
        )

        col_a, col_b, col_c = st.columns(3)

        with col_a:
            if st.button("📋 In Zwischenablage", use_container_width=True):
                st.code(post_text, language=None)
                st.info("👆 Text markieren und kopieren")

        with col_b:
            if st.button("🔄 Neu generieren", use_container_width=True):
                del st.session_state['generated_post']
                st.rerun()

        with col_c:
            st.download_button(
                "💾 Speichern",
                data=post_text,
                file_name=f"linkedin_{linkedin_page.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

with tab2:
    st.subheader("📚 SBS Nexus Content-Serie (5 Posts)")
    st.info("💡 Erstelle automatisch eine 5-teilige LinkedIn Post-Serie")

    serie_options = [
        "E-Rechnungspflicht 2025 – Was Steuerberater wissen müssen",
        "KI in der Steuerberatung – Von Hype zu Praxis",
        "DATEV + KI: Die Zukunft der digitalen Kanzlei",
        "Steuerberater als Technologie-Partner ihrer Mandanten",
        "Eigenes Thema eingeben..."
    ]

    serie_choice = st.selectbox("Serie wählen", serie_options)

    if serie_choice == "Eigenes Thema eingeben...":
        serie_theme = st.text_input("Thema der Serie", placeholder="z.B. Automatisierung in der Buchhaltung")
    else:
        serie_theme = serie_choice

    if st.button("🚀 Serie generieren (5 Posts)", type="primary", use_container_width=True):
        if not openai_key:
            st.error("❌ Bitte OpenAI API Key eingeben!")
        elif not serie_theme:
            st.error("❌ Bitte Thema wählen!")
        else:
            progress_bar = st.progress(0)
            status = st.empty()

            generated_serie = []
            post_fokus = [
                "Hook & Problem Statement – Marktdaten & Dringlichkeit",
                "Ursachen & Status Quo – Warum Steuerberater handeln müssen",
                "Lösung & Technologie – SBS Nexus Produkt-Demo in Worten",
                "Partnerprogramm & Business Case – ROI für Steuerberater",
                "Vision & CTA – Die Zukunft der KI-gestützten Steuerberatung"
            ]

            for i in range(5):
                status.text(f"Generiere Post {i+1}/5...")

                prompt = f"""Erstelle LinkedIn Post {i+1} einer 5-teiligen Serie: {serie_theme}

UNTERNEHMEN: SBS Deutschland GmbH & Co. KG (Weinheim)
PLATTFORM: SBS Nexus – Das operative OS für den Mittelstand
3 MODULE: Finance Intelligence (KI-Rechnungen, 8 Sek, DATEV + SAP) | Contract Intelligence (Vertragsanalyse) | Technical Intelligence / HydraulikDoc (Datenblatt-KI)
ZIELGRUPPE: 89.000 Steuerberater + fertigender Mittelstand in DACH
PARTNERPROGRAMM: 15-25% Revenue Share
WEBSITES: www.sbsnexus.de | sbsdeutschland.com/sbshomepage/ | contract.sbsdeutschland.com
DEMO: calendly.com/ki-sbsdeutschland/sbs-nexus-30-minuten-discovery-call

FOKUS dieses Posts: {post_fokus[i]}
TONALITÄT: Thought Leadership, Enterprise-Standard
LÄNGE: 200-300 Wörter

Beziehe dich auf vorherige Posts der Serie. Nutze Hashtags: #SBSNexus #Steuerberater #DATEV
Schreibe NUR den Post."""

                try:
                    post_text = generate_with_openai(
                        prompt,
                        "Du bist LinkedIn Content-Stratege für B2B Enterprise SaaS im deutschen Steuerberater-Markt."
                    )

                    generated_serie.append({
                        'nummer': i+1,
                        'text': post_text,
                        'fokus': post_fokus[i]
                    })

                    progress_bar.progress((i+1)/5)
                    time.sleep(2)

                except Exception as e:
                    st.error(f"❌ Fehler bei Post {i+1}: {str(e)}")
                    break

            if len(generated_serie) == 5:
                status.text("✅ Serie komplett!")
                st.session_state['generated_serie'] = generated_serie
                st.balloons()
                st.rerun()

    if 'generated_serie' in st.session_state:
        st.markdown("---")
        for post in st.session_state['generated_serie']:
            with st.expander(f"📄 Post {post['nummer']}/5: {post['fokus']}"):
                st.text_area(f"Post {post['nummer']}", value=post['text'], height=250, key=f"serie_{post['nummer']}", disabled=True)
                st.download_button("💾 Speichern", data=post['text'], file_name=f"serie_post{post['nummer']}.txt", key=f"dl_{post['nummer']}", use_container_width=True)

with tab3:
    st.subheader("📅 Content-Kalender")

    schedule = calendar.get('schedule', {})
    if schedule:
        st.metric("Posting-Frequenz", schedule.get('posting_frequency', 'N/A'))

        st.markdown("### 🕒 Optimale Posting-Zeiten")
        for time_slot in schedule.get('optimal_times', []):
            with st.expander(f"**{time_slot.get('day')}** um {time_slot.get('time')}"):
                st.write(f"**Grund:** {time_slot.get('reason')}")

        st.markdown("### 📱 LinkedIn Pages")
        pages = schedule.get('linkedin_pages', {})
        if pages:
            st.markdown(f"- **Primary:** [{pages.get('primary', '')}]({pages.get('primary', '')})")
            st.markdown(f"- **Secondary:** [{pages.get('secondary', '')}]({pages.get('secondary', '')})")

with tab4:
    st.subheader("📊 Hashtag-Strategie")

    hashtags = calendar.get('hashtag_strategy', {})
    if hashtags:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("### 🏷️ Primary")
            for tag in hashtags.get('primary', []):
                st.code(tag, language=None)
        with col2:
            st.markdown("### 🏷️ Secondary")
            for tag in hashtags.get('secondary', []):
                st.code(tag, language=None)
        with col3:
            st.markdown("### 🏷️ Trending")
            for tag in hashtags.get('trending', []):
                st.code(tag, language=None)

st.markdown("---")
st.caption("SBS Deutschland GmbH & Co. KG · LinkedIn: /sbs-deutschland-gmbh-co-kg/ · /hydraulikdoc-ai/ · sbsdeutschland.com/sbshomepage/")
