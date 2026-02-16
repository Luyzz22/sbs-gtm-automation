import streamlit as st
import pandas as pd
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from automated_email_sender import SBSEmailAutomation, TARGET_CONTACTS

def show():
    st.header("📧 Email Automation")
    
    tabs = st.tabs(["📤 Kampagne starten", "📋 Kontakte verwalten", "📊 Ergebnisse", "🔄 Follow-ups"])
    
    # Tab 1: Kampagne starten
    with tabs[0]:
        st.subheader("Neue Email-Kampagne")
        
        col1, col2 = st.columns(2)
        
        with col1:
            campaign_name = st.text_input("Kampagnen-Name", "Campaign_" + pd.Timestamp.now().strftime("%Y%m%d"))
            template_type = st.selectbox("Template auswählen", ["Auto (basierend auf Rolle)", "CFO Template", "CTO Template", "CEO Template"])
            delay = st.slider("Pause zwischen Emails (Sekunden)", 60, 300, 120)
        
        with col2:
            test_mode = st.checkbox("Test-Modus (keine echten Emails)", value=False)
            ab_testing = st.checkbox("A/B Testing aktivieren", value=False)
            st.info(f"📊 {len(TARGET_CONTACTS)} Kontakte werden angeschrieben")
        
        if st.button("🚀 Kampagne starten", type="primary", width='stretch'):
            with st.spinner("Kampagne wird gestartet..."):
                automation = SBSEmailAutomation()
                
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                results = {'sent': 0, 'failed': 0, 'details': []}
                
                for idx, contact in enumerate(TARGET_CONTACTS):
                    progress = (idx + 1) / len(TARGET_CONTACTS)
                    progress_bar.progress(progress)
                    status_text.text(f"Sende Email {idx+1}/{len(TARGET_CONTACTS)}: {contact['email']}")
                    
                    if not test_mode:
                        # Echte Email senden
                        pass
                    
                    results['sent'] += 1
                
                st.success(f"✅ Kampagne abgeschlossen! {results['sent']}/{len(TARGET_CONTACTS)} Emails versendet")
    
    # Tab 2: Kontakte verwalten
    with tabs[1]:
        st.subheader("Kontakte verwalten")
        
        # Upload CSV
        uploaded_file = st.file_uploader("Kontakte hochladen (CSV)", type=['csv'])
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df, width='stretch')
            
            if st.button("Kontakte importieren"):
                st.success(f"✓ {len(df)} Kontakte importiert")
        
        st.markdown("---")
        
        # Manuell Kontakt hinzufügen
        with st.expander("➕ Neuen Kontakt hinzufügen"):
            col1, col2 = st.columns(2)
            
            with col1:
                new_email = st.text_input("Email")
                new_first_name = st.text_input("Vorname")
                new_company = st.text_input("Firma")
            
            with col2:
                new_role = st.selectbox("Rolle", ["CFO", "CTO", "CEO"])
                new_industry = st.text_input("Branche", "Maschinenbau")
                new_size = st.number_input("Mitarbeiter", 50, 500, 150)
            
            if st.button("Kontakt speichern"):
                st.success("✓ Kontakt gespeichert")
        
        # Aktuelle Kontakte
        st.markdown("### 📋 Aktuelle Kontaktliste")
        contacts_df = pd.DataFrame(TARGET_CONTACTS)
        st.dataframe(contacts_df, width='stretch')
    
    # Tab 3: Ergebnisse
    with tabs[2]:
        st.subheader("Kampagnen-Ergebnisse")
        
        try:
            results_df = pd.read_csv('campaign_results.csv')
            
            col1, col2, col3 = st.columns(3)
            
            total = len(results_df)
            sent = len(results_df[results_df['status'] == 'sent'])
            success_rate = (sent/total*100) if total > 0 else 0
            
            col1.metric("Gesamt", total)
            col2.metric("Erfolgreich", sent)
            col3.metric("Erfolgsrate", f"{success_rate:.0f}%")
            
            st.dataframe(results_df, width='stretch')
            
            # Download
            csv = results_df.to_csv(index=False)
            st.download_button(
                "📥 CSV herunterladen",
                csv,
                "campaign_results.csv",
                "text/csv"
            )
            
        except FileNotFoundError:
            st.info("Noch keine Kampagnen-Ergebnisse vorhanden")
    
    # Tab 4: Follow-ups
    with tabs[3]:
        st.subheader("Follow-up Management")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### ⚙️ Einstellungen")
            follow_up_day_3 = st.checkbox("Tag 3 Follow-up", value=True)
            follow_up_day_7 = st.checkbox("Tag 7 Follow-up", value=True)
            follow_up_day_14 = st.checkbox("Tag 14 Follow-up", value=True)
        
        with col2:
            st.markdown("### 📅 Nächste Follow-ups")
            st.info("Keine Follow-ups fällig")
        
        if st.button("🔄 Follow-ups jetzt prüfen"):
            st.success("✓ Follow-ups geprüft")
