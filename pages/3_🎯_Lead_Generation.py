import streamlit as st
import yaml
from pathlib import Path
import pandas as pd
import requests
import os

st.set_page_config(page_title="Lead Generation", page_icon="🎯")

st.title("🎯 Lead Generation")

# Load ICP Config
config_path = Path("config")
icp_file = config_path / "icp_filters.yaml"

if icp_file.exists():
    with open(icp_file, 'r', encoding='utf-8') as f:
        icp = yaml.safe_load(f)
else:
    st.error("❌ config/icp_filters.yaml nicht gefunden!")
    st.stop()

# Sidebar - Hunter.io API
with st.sidebar:
    st.header("🔑 Hunter.io API")
    hunter_key = st.text_input("Hunter API Key", type="password", 
                               value=os.getenv('HUNTER_API_KEY', ''))
    if hunter_key:
        os.environ['HUNTER_API_KEY'] = hunter_key

# Tabs
tab1, tab2, tab3 = st.tabs(["🎯 ICP Definition", "🔍 Lead Search", "📋 Lead-Liste"])

with tab1:
    st.subheader("Ideal Customer Profile (ICP)")
    
    filters = icp.get('target_filters', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 👔 Ziel-Positionen")
        for title in filters.get('job_titles', []):
            st.markdown(f"✓ {title}")
        
        st.markdown("### 🏭 Branchen")
        for industry in filters.get('industries', []):
            st.markdown(f"✓ {industry}")
    
    with col2:
        st.markdown("### 📊 Unternehmensgröße")
        company_size = filters.get('company_size', {})
        
        col_min, col_max = st.columns(2)
        with col_min:
            st.metric("Minimum", f"{company_size.get('min', 0)} MA")
        with col_max:
            st.metric("Maximum", f"{company_size.get('max', 0)} MA")
        
        st.markdown("### 🌍 Regionen")
        for region in filters.get('regions', []):
            st.markdown(f"✓ {region}")
    
    st.markdown("---")
    
    st.markdown("### ❌ Ausschluss-Kriterien")
    exclusions = icp.get('exclusion_criteria', {})
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**Keywords:**")
        for kw in exclusions.get('keywords', []):
            st.markdown(f"✗ {kw}")
    
    with col_b:
        st.markdown("**Branchen:**")
        for ind in exclusions.get('industries', []):
            st.markdown(f"✗ {ind}")

with tab2:
    st.subheader("🔍 Lead-Suche mit Hunter.io")
    
    search_method = st.radio("Such-Methode", ["Domain Search", "Email Finder"])
    
    if search_method == "Domain Search":
        st.info("💡 Finde alle öffentlichen Email-Adressen einer Domain")
        
        domain = st.text_input("Unternehmens-Domain", placeholder="beispiel-gmbh.de")
        
        if st.button("🔍 Suche starten", type="primary", use_container_width=True):
            if not hunter_key:
                st.error("❌ Bitte Hunter.io API Key eingeben!")
            elif not domain:
                st.error("❌ Bitte Domain eingeben!")
            else:
                with st.spinner(f"Suche Emails für {domain}..."):
                    try:
                        url = "https://api.hunter.io/v2/domain-search"
                        params = {
                            "domain": domain,
                            "api_key": hunter_key,
                            "limit": 25
                        }
                        
                        response = requests.get(url, params=params, timeout=15)
                        response.raise_for_status()
                        
                        data = response.json()
                        
                        if 'data' in data:
                            emails = data['data'].get('emails', [])
                            
                            # API Quota anzeigen
                            if 'meta' in data:
                                meta = data['meta']
                                if 'requests' in meta:
                                    used = meta['requests'].get('used', 0)
                                    available = meta['requests'].get('available', 0)
                                    st.info(f"📊 API Quota: {used} verwendet, {available} verfügbar")
                            
                            if emails:
                                st.success(f"✅ {len(emails)} Emails gefunden!")
                                
                                # Dataframe erstellen
                                df_data = []
                                for email_info in emails:
                                    df_data.append({
                                        'Email': email_info.get('value', 'N/A'),
                                        'Name': f"{email_info.get('first_name', '')} {email_info.get('last_name', '')}".strip(),
                                        'Position': email_info.get('position', 'N/A'),
                                        'Type': email_info.get('type', 'N/A'),
                                        'Confidence': f"{email_info.get('confidence', 0)}%"
                                    })
                                
                                df = pd.DataFrame(df_data)
                                st.dataframe(df, use_container_width=True, hide_index=True)
                                
                                # Download Button
                                csv = df.to_csv(index=False)
                                st.download_button(
                                    "💾 Als CSV exportieren",
                                    csv,
                                    f"leads_{domain}.csv",
                                    "text/csv",
                                    use_container_width=True
                                )
                            else:
                                st.warning("⚠️ Keine öffentlichen Emails gefunden")
                                st.info("""
                                **Mögliche Gründe:**
                                - Domain ist zu klein/neu
                                - Keine öffentlichen Team-Seiten
                                - Emails sind nicht indexiert
                                
                                **Tipp:** Nutze "Email Finder" mit Namen von bekannten Mitarbeitern
                                """)
                    
                    except requests.exceptions.HTTPError as e:
                        if e.response.status_code == 422:
                            st.error("❌ Domain nicht gefunden oder ungültig")
                        elif e.response.status_code == 429:
                            st.error("❌ Rate Limit erreicht - zu viele Requests")
                        else:
                            st.error(f"❌ HTTP Error: {e}")
                    except Exception as e:
                        st.error(f"❌ Fehler: {str(e)}")
    
    else:  # Email Finder
        st.info("💡 Finde Email-Adresse basierend auf Name und Domain")
        
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Vorname", "Thomas")
        with col2:
            last_name = st.text_input("Nachname", "Müller")
        
        domain = st.text_input("Domain", "beispiel-gmbh.de")
        
        if st.button("🔍 Email finden", type="primary", use_container_width=True):
            if not hunter_key:
                st.error("❌ Bitte Hunter.io API Key eingeben!")
            elif not all([first_name, last_name, domain]):
                st.error("❌ Bitte alle Felder ausfüllen!")
            else:
                with st.spinner("Suche Email..."):
                    try:
                        url = "https://api.hunter.io/v2/email-finder"
                        params = {
                            "domain": domain,
                            "first_name": first_name,
                            "last_name": last_name,
                            "api_key": hunter_key
                        }
                        
                        response = requests.get(url, params=params, timeout=15)
                        response.raise_for_status()
                        
                        data = response.json()
                        
                        if 'data' in data:
                            email_data = data['data']
                            email = email_data.get('email')
                            score = email_data.get('score', 0)
                            
                            if email:
                                st.success(f"✅ Email gefunden: **{email}**")
                                st.metric("Confidence Score", f"{score}%")
                            else:
                                st.warning("⚠️ Keine Email gefunden")
                    
                    except Exception as e:
                        st.error(f"❌ Fehler: {str(e)}")

with tab3:
    st.subheader("📋 Gespeicherte Leads")
    
    st.info("📊 Lead-Datenbank - Import/Export Funktionen")
    
    uploaded = st.file_uploader("CSV mit Leads hochladen", type=['csv'])
    
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df, use_container_width=True)
        
        st.success(f"✅ {len(df)} Leads geladen")
