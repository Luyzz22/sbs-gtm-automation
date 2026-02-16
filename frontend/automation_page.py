import streamlit as st
import pandas as pd
from datetime import datetime

def show():
    st.header("🤖 Vollautomatische Email-Pipeline")
    
    st.markdown("""
    Diese Seite konfiguriert die vollautomatische Email-Pipeline:
    **Lead-Suche → Email-Generierung → Versand**
    """)
    
    tabs = st.tabs(["⚙️ Konfiguration", "📅 Zeitplan", "📊 Pipeline-Status", "🔔 Benachrichtigungen"])
    
    with tabs[0]:
        st.subheader("Pipeline-Konfiguration")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🔍 Lead-Generierung")
            
            auto_lead_gen = st.checkbox("Automatische Lead-Suche aktivieren", value=True)
            
            if auto_lead_gen:
                lead_frequency = st.selectbox(
                    "Frequenz",
                    ["Täglich", "2x Woche (Mo & Do)", "Wöchentlich (Montag)"],
                    index=1
                )
                
                leads_per_run = st.number_input("Leads pro Durchlauf", 5, 50, 10)
                
                st.markdown("**ICP Filter (vorkonfiguriert):**")
                st.info("""
                - Branche: Maschinenbau, Automotive, Anlagenbau
                - Größe: 50-500 Mitarbeiter
                - Region: Baden-Württemberg, Bayern
                - Rollen: CFO, CTO, CEO
                """)
        
        with col2:
            st.markdown("### 📧 Email-Generierung & Versand")
            
            auto_email_gen = st.checkbox("Automatische Email-Generierung", value=True)
            
            if auto_email_gen:
                email_frequency = st.selectbox(
                    "Versand-Frequenz",
                    ["Sofort nach Lead-Gen", "Täglich 9:00 Uhr", "2x Woche (Mo 9:00, Do 9:00)"],
                    index=2
                )
                
                batch_size = st.number_input("Batch-Größe", 1, 20, 10)
                delay_between = st.slider("Pause zwischen Emails (Sek)", 60, 300, 120)
                
                use_ai_personalization = st.checkbox("KI-Personalisierung (GPT-4)", value=True)
        
        st.markdown("---")
        
        st.markdown("### 🔄 Follow-up Automation")
        
        col_f1, col_f2, col_f3 = st.columns(3)
        
        with col_f1:
            follow_up_3 = st.checkbox("Tag 3 Follow-up", value=True)
        with col_f2:
            follow_up_7 = st.checkbox("Tag 7 Follow-up", value=True)
        with col_f3:
            follow_up_14 = st.checkbox("Tag 14 Follow-up", value=True)
        
        st.markdown("---")
        
        if st.button("💾 Konfiguration speichern", type="primary", width='stretch'):
            st.success("✅ Automation-Pipeline konfiguriert!")
            st.balloons()
    
    with tabs[1]:
        st.subheader("📅 Automation-Zeitplan")
        
        schedule_data = {
            "Task": [
                "🔍 Lead-Generierung",
                "📧 Email-Kampagne",
                "📧 Email-Kampagne",
                "🔄 Follow-up Check",
                "📊 Performance-Report"
            ],
            "Frequenz": [
                "Montag & Donnerstag",
                "Montag 9:00",
                "Donnerstag 9:00",
                "Täglich 9:00",
                "Freitag 17:00"
            ],
            "Nächste Ausführung": [
                "Do, 20.02.2026 09:00",
                "Mo, 17.02.2026 09:00",
                "Do, 20.02.2026 09:00",
                "Di, 17.02.2026 09:00",
                "Fr, 21.02.2026 17:00"
            ],
            "Status": [
                "✅ Aktiv",
                "✅ Aktiv",
                "✅ Aktiv",
                "✅ Aktiv",
                "✅ Aktiv"
            ]
        }
        
        st.dataframe(schedule_data, width='stretch', hide_index=True)
        
        st.markdown("---")
        
        col_btn1, col_btn2 = st.columns(2)
        
        with col_btn1:
            if st.button("▶️ Pipeline jetzt starten"):
                st.success("✓ Pipeline läuft...")
        
        with col_btn2:
            if st.button("⏸️ Pipeline pausieren"):
                st.warning("Pipeline pausiert")
    
    with tabs[2]:
        st.subheader("📊 Pipeline-Status & Logs")
        
        # Status Cards
        status_col1, status_col2, status_col3, status_col4 = st.columns(4)
        
        status_col1.metric("🤖 Pipeline-Status", "Aktiv", delta="Running")
        status_col2.metric("📧 Emails heute", "0", delta="0")
        status_col3.metric("🔍 Leads gefunden", "0", delta="0")
        status_col4.metric("⏱️ Nächster Run", "17.02. 09:00")
        
        st.markdown("---")
        
        # Activity Log
        st.markdown("### 📜 Activity Log (Live)")
        
        log_data = {
            "Zeit": [
                datetime.now().strftime("%H:%M:%S"),
                "14:18:00",
                "14:16:00",
                "14:14:00"
            ],
            "Ereignis": [
                "Pipeline gestartet",
                "Email versendet: julia.richter@machinevision.de",
                "Email versendet: claudia.meyer@techmach.de",
                "Email versendet: max.mustermann@hahn-automation.de"
            ],
            "Status": [
                "🟢 Info",
                "✅ Erfolg",
                "✅ Erfolg",
                "✅ Erfolg"
            ]
        }
        
        st.dataframe(log_data, width='stretch', hide_index=True)
        
        # Download Logs
        if st.button("📥 Logs herunterladen"):
            st.success("✓ Logs exportiert")
    
    with tabs[3]:
        st.subheader("🔔 Benachrichtigungen")
        
        col_notif1, col_notif2 = st.columns(2)
        
        with col_notif1:
            st.markdown("### Email-Benachrichtigungen")
            
            notify_email = st.text_input("Benachrichtigungs-Email", "ki@sbsdeutschland.de")
            
            notify_on_complete = st.checkbox("Bei Kampagnen-Abschluss", value=True)
            notify_on_error = st.checkbox("Bei Fehlern", value=True)
            notify_daily_report = st.checkbox("Täglicher Report (17:00)", value=True)
            notify_weekly_summary = st.checkbox("Wöchentliche Zusammenfassung (Fr)", value=True)
        
        with col_notif2:
            st.markdown("### Slack-Integration")
            
            slack_webhook = st.text_input("Slack Webhook URL", placeholder="https://hooks.slack.com/...")
            
            slack_on_leads = st.checkbox("Bei neuen Leads", value=False)
            slack_on_replies = st.checkbox("Bei Email-Antworten", value=False)
            slack_on_errors = st.checkbox("Bei kritischen Fehlern", value=True)
        
        if st.button("💾 Benachrichtigungen speichern"):
            st.success("✓ Benachrichtigungen konfiguriert")
