import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from automated_email_sender import SBSEmailAutomation

st.set_page_config(page_title="SBS Nexus – Email Automation", page_icon="📧")

st.title("📧 SBS Nexus Email Automation")
st.caption("KI-personalisierte Outreach-Emails für Steuerberater & Kanzleien")

# Sidebar
with st.sidebar:
    st.header("⚙️ Einstellungen")

    use_ai = st.toggle("🤖 AI-Generierung (GPT-4)", value=True,
                       help="Nutze OpenAI GPT-4 für personalisierte Emails")

    if use_ai:
        openai_key = st.text_input(
            "OpenAI API Key",
            type="password",
            value=os.getenv('OPENAI_API_KEY', ''),
            help="Dein OpenAI API Schlüssel"
        )
        if openai_key:
            os.environ['OPENAI_API_KEY'] = openai_key
            st.success("✓ API Key gesetzt")

    st.markdown("---")

    use_resend = st.toggle("📧 Resend API", value=True)

    if use_resend:
        resend_key = st.text_input(
            "Resend API Key",
            type="password",
            value=os.getenv('RESEND_API_KEY', '')
        )
        if resend_key:
            os.environ['RESEND_API_KEY'] = resend_key
    else:
        st.info("📮 Nutze SMTP aus .env")

    st.markdown("---")
    st.markdown("### 🔗 Ressourcen")
    st.markdown("""
    - [🌐 SBS Homepage](https://sbsdeutschland.com/sbshomepage/)
    - [⚡ SBS Nexus](https://www.sbsnexus.de)
    - [📄 Contract AI](https://contract.sbsdeutschland.com/)
    - [🤝 Partner-Seite](https://www.sbsnexus.de/partner)
    - [📅 Demo buchen](https://calendly.com/ki-sbsdeutschland/sbs-nexus-30-minuten-discovery-call)
    """)

# Tabs
tab1, tab2, tab3 = st.tabs(["✨ Einzelne Email", "📊 Kampagne", "📜 Verlauf"])

with tab1:
    st.subheader("Steuerberater-Email generieren & senden")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👤 Kontaktdaten")
        first_name = st.text_input("Vorname*", "", key="single_fname", placeholder="Tobias")
        last_name = st.text_input("Nachname*", "", key="single_lname", placeholder="Staat")
        email = st.text_input("Email*", "", key="single_email", placeholder="info@stbstaat.de")
        job_title = st.selectbox("Position*", [
            "Steuerberater", "Kanzleiinhaber", "Partner",
            "Geschäftsführer", "Wirtschaftsprüfer",
            "CFO", "Leiter Finanzbuchhaltung"
        ], key="single_title")

    with col2:
        st.markdown("### 🏢 Kanzlei / Unternehmen")
        company_name = st.text_input("Kanzlei / Firma*", "", key="single_company", placeholder="Steuerberater Tobias Staat")
        segment = st.selectbox("Segment", [
            "Digital-affin (DATEV UO, Label)",
            "Traditionell (DATEV Mitglied)",
            "Großkanzlei (50+ MA)",
            "KMU-Entscheider"
        ], key="single_segment")
        company_size = st.number_input("Team-Größe", 1, 500, 15, key="single_size")
        datev_status = st.selectbox("DATEV-Status", [
            "DATEV UO aktiv + Digitale Kanzlei Label",
            "DATEV UO aktiv",
            "DATEV Mitglied",
            "Andere Software",
            "Unbekannt"
        ], key="single_datev")

    st.markdown("### 🎯 Personalisierung")
    personalization_hook = st.text_area(
        "Personalisierungs-Hook (warum diese Kanzlei?)",
        placeholder="z.B. Mehrfach ausgezeichnete digitale Kanzlei, Handelsblatt-Preis, KI-Tools auf Website, papierlos seit 2019...",
        height=80,
        key="single_hook"
    )

    st.markdown("---")

    col_gen, col_send = st.columns([2, 1])

    with col_gen:
        generate_btn = st.button("✨ Email generieren", type="primary", use_container_width=True)

    if generate_btn:
        if not all([email, first_name, last_name, company_name]):
            st.error("❌ Bitte alle Pflichtfelder (*) ausfüllen!")
        elif use_ai and not os.getenv('OPENAI_API_KEY'):
            st.error("❌ Bitte OpenAI API Key eingeben!")
        else:
            contact = {
                'email': email,
                'first_name': first_name,
                'last_name': last_name,
                'job_title': job_title,
                'role': job_title,
                'company_name': company_name,
                'segment': segment,
                'company_size': company_size,
                'datev_status': datev_status,
                'personalization_hook': personalization_hook or f"als {job_title} bei {company_name} setzen Sie digitale Maßstäbe."
            }

            with st.spinner("🤖 Generiere SBS Nexus Email..." if use_ai else "📄 Lade Template..."):
                try:
                    automation = SBSEmailAutomation(use_resend=use_resend)

                    if use_ai and os.getenv('OPENAI_API_KEY'):
                        subject, body = automation.generate_ai_email(contact)
                        st.success("✅ KI-Email erfolgreich generiert!")
                    else:
                        templates = automation.load_templates()
                        template = automation.select_template(job_title, templates)
                        subject, body = automation.personalize_message(template, contact)
                        st.info("✅ Template-Email generiert")

                    st.session_state['generated_subject'] = subject
                    st.session_state['generated_body'] = body
                    st.session_state['generated_email'] = email
                    st.session_state['generated_contact'] = contact

                except Exception as e:
                    st.error(f"❌ Fehler: {str(e)}")

    # Generierte Email anzeigen
    if 'generated_subject' in st.session_state:
        st.markdown("---")
        st.subheader("📧 Generierte Email")

        subject_display = st.text_input(
            "Betreff",
            value=st.session_state['generated_subject'],
            key="subject_display"
        )

        body_display = st.text_area(
            "Nachricht",
            value=st.session_state['generated_body'],
            height=400,
            key="body_display"
        )

        col_send, col_edit, col_save = st.columns([2, 1, 1])

        with col_send:
            if st.button("📤 Jetzt senden", type="primary", use_container_width=True):
                try:
                    automation = SBSEmailAutomation(use_resend=use_resend)
                    success = automation.send_email(
                        st.session_state['generated_email'],
                        subject_display,
                        body_display
                    )
                    if success:
                        st.success(f"✅ Email gesendet an {st.session_state['generated_email']}!")
                        del st.session_state['generated_subject']
                        del st.session_state['generated_body']
                        st.rerun()
                    else:
                        st.error("❌ Fehler beim Senden")
                except Exception as e:
                    st.error(f"❌ Fehler: {str(e)}")

        with col_edit:
            if st.button("🔄 Neu generieren", use_container_width=True):
                del st.session_state['generated_subject']
                del st.session_state['generated_body']
                st.rerun()

        with col_save:
            st.download_button(
                "💾 Speichern",
                data=f"Subject: {subject_display}\n\n{body_display}",
                file_name=f"email_{st.session_state['generated_contact']['company_name']}.txt",
                mime="text/plain",
                use_container_width=True
            )

with tab2:
    st.subheader("📊 Steuerberater-Kampagne")
    st.info("💡 Upload CSV mit Steuerberater-Kontakten für Massen-Versand (aus CRM Template)")

    uploaded_file = st.file_uploader("CSV hochladen", type=['csv'])

    if uploaded_file:
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head(10))
        st.metric("Kontakte geladen", len(df))

        if st.button("🚀 Kampagne starten", type="primary"):
            st.warning("⚠️ Kampagne wird vorbereitet... Bitte API Keys prüfen.")

with tab3:
    st.subheader("📜 Versand-Verlauf")
    st.info("📊 Versandstatistiken werden nach dem ersten Versand angezeigt")

st.markdown("---")
st.caption("SBS Deutschland GmbH & Co. KG · Finance · Contract · Technical Intelligence · sbsnexus.de")
