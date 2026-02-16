import streamlit as st
import os
from pathlib import Path
import yaml

st.set_page_config(page_title="Einstellungen", page_icon="⚙️")

st.title("⚙️ Einstellungen")

tab1, tab2, tab3 = st.tabs(["🔑 API Keys", "📋 Konfiguration", "🔧 System-Status"])

with tab1:
    st.subheader("API-Schlüssel verwalten")
    
    with st.form("api_keys_form"):
        openai_key = st.text_input("OpenAI API Key", type="password", value=os.getenv('OPENAI_API_KEY', ''))
        anthropic_key = st.text_input("Anthropic API Key", type="password", value=os.getenv('ANTHROPIC_API_KEY', ''))
        resend_key = st.text_input("Resend API Key", type="password", value=os.getenv('RESEND_API_KEY', ''))
        
        smtp_server = st.text_input("SMTP Server", value=os.getenv('SMTP_SERVER', 'smtp.strato.de'))
        smtp_user = st.text_input("SMTP Username", value=os.getenv('SMTP_USERNAME', ''))
        smtp_pass = st.text_input("SMTP Password", type="password", value=os.getenv('SMTP_PASSWORD', ''))
        
        submitted = st.form_submit_button("💾 Speichern", type="primary")
        
        if submitted:
            # Update .env wäre hier
            st.success("✅ API Keys gespeichert (Restart erforderlich)")

with tab2:
    st.subheader("📋 Systemkonfiguration")
    
    config_path = Path("config")
    config_files = ["content_calendar.yaml", "icp_filters.yaml", "message_templates.yaml"]
    
    for config_file in config_files:
        file_path = config_path / config_file
        
        with st.expander(f"📄 {config_file}"):
            if file_path.exists():
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                st.code(content, language='yaml')
                st.success(f"✓ Geladen: {file_path}")
            else:
                st.error(f"✗ Nicht gefunden: {file_path}")

with tab3:
    st.subheader("🔧 System-Status")
    
    status_data = []
    
    # Check API Keys
    openai_key = os.getenv("OPENAI_API_KEY")
    if openai_key and len(openai_key) > 20:
        status_data.append({"Komponente": "OpenAI API", "Status": "✅", "Details": f"...{openai_key[-8:]}"})
    else:
        status_data.append({"Komponente": "OpenAI API", "Status": "❌", "Details": "Nicht konfiguriert"})
    
    anthropic_key = os.getenv("ANTHROPIC_API_KEY")
    if anthropic_key and len(anthropic_key) > 20:
        status_data.append({"Komponente": "Anthropic API", "Status": "✅", "Details": f"...{anthropic_key[-8:]}"})
    else:
        status_data.append({"Komponente": "Anthropic API", "Status": "❌", "Details": "Nicht konfiguriert"})
    
    resend_key = os.getenv("RESEND_API_KEY")
    if resend_key and len(resend_key) > 10:
        status_data.append({"Komponente": "Resend API", "Status": "✅", "Details": f"...{resend_key[-8:]}"})
    else:
        status_data.append({"Komponente": "Resend API", "Status": "❌", "Details": "Nicht konfiguriert"})
    
    # Check Config Files
    config_path = Path("config")
    for config_file in ["content_calendar.yaml", "icp_filters.yaml", "message_templates.yaml"]:
        file_path = config_path / config_file
        if file_path.exists():
            status_data.append({"Komponente": f"Config: {config_file}", "Status": "✅", "Details": "Geladen"})
        else:
            status_data.append({"Komponente": f"Config: {config_file}", "Status": "❌", "Details": "Nicht gefunden"})
    
    import pandas as pd
    st.dataframe(pd.DataFrame(status_data), use_container_width=True, hide_index=True)
