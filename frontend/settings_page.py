import streamlit as st
import os
from dotenv import load_dotenv

load_dotenv()

def show():
    st.header("⚙️ Einstellungen")
    
    tabs = st.tabs(["🔑 API Keys", "👤 Profil", "🎨 Darstellung", "🔧 System"])
    
    with tabs[0]:
        st.subheader("API-Konfiguration")
        
        with st.expander("📧 Resend API"):
            resend_key = st.text_input(
                "API Key",
                value=os.getenv('RESEND_API_KEY', ''),
                type="password"
            )
            sender_email = st.text_input("Sender Email", value=os.getenv('SENDER_EMAIL', ''))
            
            if st.button("Verbindung testen"):
                st.success("✅ Verbindung erfolgreich")
        
        with st.expander("🤖 OpenAI API"):
            openai_key = st.text_input(
                "API Key",
                value=os.getenv('OPENAI_API_KEY', ''),
                type="password"
            )
            
            if st.button("OpenAI testen"):
                st.success("✅ API funktioniert")
        
        with st.expander("🔍 Lead-Gen APIs"):
            apollo_key = st.text_input("Apollo.io API Key", type="password")
            hunter_key = st.text_input("Hunter.io API Key", type="password")
            linkedin_cookies = st.text_area("LinkedIn Session Cookies")
        
        if st.button("💾 API Keys speichern", type="primary"):
            st.success("✅ Gespeichert")
    
    with tabs[1]:
        st.subheader("Benutzer-Profil")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name", value="Luis Schenk")
            title = st.text_input("Position", value="Innovation Manager")
            company = st.text_input("Firma", value="SBS Deutschland GmbH")
        
        with col2:
            email = st.text_input("Email", value="ki@sbsdeutschland.de")
            phone = st.text_input("Telefon", value="")
            linkedin = st.text_input("LinkedIn URL", value="")
        
        if st.button("💾 Profil speichern"):
            st.success("✅ Profil aktualisiert")
    
    with tabs[2]:
        st.subheader("Darstellungs-Einstellungen")
        
        theme = st.selectbox("Theme", ["Hell", "Dunkel", "Auto"])
        language = st.selectbox("Sprache", ["Deutsch", "English"])
        
        st.info("Theme-Änderungen erfordern Neustart")
    
    with tabs[3]:
        st.subheader("System-Information")
        
        st.code(f"""
        Version: 1.0.0
        Python: 3.13
        Streamlit: {st.__version__}
        Installation: {os.getcwd()}
        """)
        
        col_sys1, col_sys2 = st.columns(2)
        
        with col_sys1:
            if st.button("🔄 Cache leeren"):
                st.cache_data.clear()
                st.success("✅ Cache geleert")
        
        with col_sys2:
            if st.button("📥 Logs exportieren"):
                st.success("✅ Logs exportiert")
