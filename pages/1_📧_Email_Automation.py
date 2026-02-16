import streamlit as st
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from automated_email_sender import SBSEmailAutomation

st.set_page_config(page_title="Email Automation", page_icon="📧")

st.title("📧 Email Automation")

# Sidebar - Einstellungen
with st.sidebar:
    st.header("⚙️ Einstellungen")
    
    # AI Toggle
    use_ai = st.toggle("🤖 AI-Generierung", value=True, 
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
    
    # Email Provider
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

# Tabs für verschiedene Modi
tab1, tab2, tab3 = st.tabs(["✨ Einzelne Email", "📊 Kampagne", "📜 Verlauf"])

with tab1:
    st.subheader("Einzelne Email generieren & senden")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👤 Kontaktdaten")
        first_name = st.text_input("Vorname*", "Max", key="single_fname")
        last_name = st.text_input("Nachname*", "Mustermann", key="single_lname")
        email = st.text_input("Email*", "max.mustermann@example.de", key="single_email")
        job_title = st.text_input("Position*", "CFO", key="single_title")
    
    with col2:
        st.markdown("### 🏢 Unternehmen")
        company_name = st.text_input("Firmenname*", "Beispiel GmbH", key="single_company")
        industry = st.selectbox("Branche", 
            ["Maschinenbau", "Werkzeugbau", "Automobilzulieferer", "Sondermaschinenbau"],
            key="single_industry"
        )
        company_size = st.number_input("Mitarbeiter", 50, 5000, 150, key="single_size")
        revenue = st.text_input("Umsatz (optional)", "45M EUR", key="single_revenue")
    
    st.markdown("---")
    
    col_gen, col_send = st.columns([2, 1])
    
    with col_gen:
        generate_btn = st.button("✨ Email generieren", type="primary", use_container_width=True)
    
    if generate_btn:
        if not all([email, first_name, last_name, company_name]):
            st.error("❌ Bitte fülle alle Pflichtfelder (*) aus!")
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
                'industry': industry,
                'company_size': company_size,
                'estimated_revenue': revenue
            }
            
            with st.spinner("🤖 Generiere Email..." if use_ai else "📄 Lade Template..."):
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
                    
                    # Speichere in Session State
                    st.session_state['generated_subject'] = subject
                    st.session_state['generated_body'] = body
                    st.session_state['generated_email'] = email
                    st.session_state['generated_contact'] = contact
                    
                except Exception as e:
                    st.error(f"❌ Fehler: {str(e)}")
    
    # Zeige generierte Email
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
            height=350,
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
                        # Lösche aus Session
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
    st.subheader("📊 Email-Kampagne")
    st.info("💡 Upload CSV mit Kontakten für Massen-Versand")
    
    uploaded_file = st.file_uploader("CSV hochladen", type=['csv'])
    
    if uploaded_file:
        import pandas as pd
        df = pd.read_csv(uploaded_file)
        st.dataframe(df.head())
        
        if st.button("🚀 Kampagne starten"):
            st.warning("⚠️ Feature in Entwicklung")

with tab3:
    st.subheader("📜 Versand-Verlauf")
    st.info("📊 Versandstatistiken werden hier angezeigt")
