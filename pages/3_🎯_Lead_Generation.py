import streamlit as st
import yaml
from pathlib import Path
import pandas as pd
import requests
import os

st.set_page_config(page_title="SBS Nexus – Lead Generation", page_icon="🎯")

st.title("🎯 Steuerberater Lead Generation")
st.caption("Digitale Kanzleien finden, qualifizieren und in die Pipeline aufnehmen")

# Load ICP Config
config_path = Path("config")
icp_file = config_path / "icp_filters.yaml"

if icp_file.exists():
    with open(icp_file, 'r', encoding='utf-8') as f:
        icp = yaml.safe_load(f)
else:
    st.error("❌ config/icp_filters.yaml nicht gefunden!")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("🔑 API Keys")
    hunter_key = st.text_input("Hunter.io API Key", type="password",
                               value=os.getenv('HUNTER_API_KEY', ''))
    if hunter_key:
        os.environ['HUNTER_API_KEY'] = hunter_key

    st.markdown("---")
    st.markdown("### 🔍 Recherche-Tools")
    st.markdown("""
    - [DATEV SmartExperts](https://smartexperts.datev.de/)
    - [Steuerberater-Suche](https://www.steuerberater-suchservice.de/)
    - [Digitale DATEV-Kanzlei](https://www.datev.de/web/de/datev-magazin/digitale-kanzlei/)
    - [Hunter.io](https://hunter.io/)
    """)

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🎯 ICP Definition", "🔍 Lead Search", "📋 Lead-Liste", "📊 Lead Scoring"])

with tab1:
    st.subheader("Ideal Customer Profile – Steuerberater")

    filters = icp.get('target_filters', {})

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👔 Ziel-Positionen")
        for title in filters.get('job_titles', []):
            st.markdown(f"✓ {title}")

        st.markdown("### 🏢 Kanzlei-Typen")
        for ct in filters.get('company_types', []):
            st.markdown(f"✓ {ct}")

        st.markdown("### 🎯 Spezialisierungen (Premium)")
        for spec in filters.get('specializations', []):
            st.markdown(f"✓ {spec}")

    with col2:
        st.markdown("### 📊 Kanzleigröße")
        company_size = filters.get('company_size', {})
        col_min, col_max = st.columns(2)
        with col_min:
            st.metric("Minimum", f"{company_size.get('min', 0)} MA")
        with col_max:
            st.metric("Maximum", f"{company_size.get('max', 0)} MA")

        st.markdown("### 🌍 Regionen (Priorisiert)")
        regions = filters.get('regions', {})
        for tier, region_list in regions.items():
            tier_label = tier.replace('_', ' ').title()
            st.markdown(f"**{tier_label}:**")
            for r in region_list:
                st.markdown(f"  ✓ {r}")

        st.markdown("### 💻 DATEV-Status")
        datev = filters.get('datev_status', {})
        for priority, items in datev.items():
            label = priority.replace('priority_', '').title()
            st.markdown(f"**{label}:**")
            for item in items:
                st.markdown(f"  ✓ {item}")

    st.markdown("---")

    st.markdown("### 📈 Digital-Signale (Qualifizierungskriterien)")
    signals = filters.get('digital_signals', {})
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**🟢 Starke Signale:**")
        for s in signals.get('strong', []):
            st.markdown(f"✓ {s}")
    with col_b:
        st.markdown("**🟡 Mittlere Signale:**")
        for s in signals.get('medium', []):
            st.markdown(f"~ {s}")

with tab2:
    st.subheader("🔍 Steuerberater-Suche")

    search_method = st.radio("Such-Methode", ["Domain Search (Hunter.io)", "Email Finder (Name + Domain)", "Manuelle Recherche"])

    if search_method == "Domain Search (Hunter.io)":
        st.info("💡 Finde alle öffentlichen Email-Adressen einer Kanzlei-Domain")

        domain = st.text_input("Kanzlei-Domain", placeholder="stbstaat.de")

        if st.button("🔍 Suche starten", type="primary", use_container_width=True):
            if not hunter_key:
                st.error("❌ Bitte Hunter.io API Key eingeben!")
            elif not domain:
                st.error("❌ Bitte Domain eingeben!")
            else:
                with st.spinner(f"Suche Emails für {domain}..."):
                    try:
                        url = "https://api.hunter.io/v2/domain-search"
                        params = {"domain": domain, "api_key": hunter_key, "limit": 25}
                        response = requests.get(url, params=params, timeout=15)
                        response.raise_for_status()
                        data = response.json()

                        if 'data' in data:
                            emails = data['data'].get('emails', [])
                            if emails:
                                st.success(f"✅ {len(emails)} Emails gefunden!")
                                df_data = []
                                for email_info in emails:
                                    df_data.append({
                                        'Email': email_info.get('value', 'N/A'),
                                        'Name': f"{email_info.get('first_name', '')} {email_info.get('last_name', '')}".strip(),
                                        'Position': email_info.get('position', 'N/A'),
                                        'Confidence': f"{email_info.get('confidence', 0)}%"
                                    })
                                df = pd.DataFrame(df_data)
                                st.dataframe(df, use_container_width=True, hide_index=True)
                                csv = df.to_csv(index=False)
                                st.download_button("💾 CSV Export", csv, f"leads_{domain}.csv", "text/csv", use_container_width=True)
                            else:
                                st.warning("⚠️ Keine Emails gefunden – nutze Impressum/Kontaktseite der Kanzlei")
                    except Exception as e:
                        st.error(f"❌ Fehler: {str(e)}")

    elif search_method == "Email Finder (Name + Domain)":
        st.info("💡 Finde Email basierend auf Name und Kanzlei-Domain")
        col1, col2 = st.columns(2)
        with col1:
            first_name = st.text_input("Vorname", placeholder="Tobias")
        with col2:
            last_name = st.text_input("Nachname", placeholder="Staat")
        domain = st.text_input("Domain", placeholder="stbstaat.de")

        if st.button("🔍 Email finden", type="primary", use_container_width=True):
            if not hunter_key:
                st.error("❌ Bitte Hunter.io API Key eingeben!")
            elif not all([first_name, last_name, domain]):
                st.error("❌ Bitte alle Felder ausfüllen!")
            else:
                with st.spinner("Suche Email..."):
                    try:
                        url = "https://api.hunter.io/v2/email-finder"
                        params = {"domain": domain, "first_name": first_name, "last_name": last_name, "api_key": hunter_key}
                        response = requests.get(url, params=params, timeout=15)
                        response.raise_for_status()
                        data = response.json()
                        if 'data' in data:
                            email = data['data'].get('email')
                            score = data['data'].get('score', 0)
                            if email:
                                st.success(f"✅ Email gefunden: **{email}**")
                                st.metric("Confidence", f"{score}%")
                            else:
                                st.warning("⚠️ Keine Email gefunden")
                    except Exception as e:
                        st.error(f"❌ Fehler: {str(e)}")

    else:
        st.markdown("### 📝 Manuelle Steuerberater-Recherche")
        st.info("💡 Nutze folgende Quellen zur manuellen Recherche:")
        st.markdown("""
        1. **DATEV SmartExperts** – smartexperts.datev.de → Nach Stadt filtern
        2. **Digitale DATEV-Kanzlei Label** – Kanzlei-Website prüfen
        3. **Google: `"Digitale Kanzlei" + Stadt + Steuerberater`**
        4. **Impressum** der Kanzlei-Website → E-Mail, Tel, Ansprechpartner
        5. **LinkedIn** → Steuerberater + Stadt → Profil prüfen
        """)

        st.markdown("### ✅ Qualifizierungs-Checkliste")
        col1, col2 = st.columns(2)
        with col1:
            st.checkbox("DATEV-Mitglied?", key="q1")
            st.checkbox("Digitale DATEV-Kanzlei Label?", key="q2")
            st.checkbox("Website modern / responsive?", key="q3")
        with col2:
            st.checkbox("DATEV Unternehmen Online aktiv?", key="q4")
            st.checkbox("KI oder Digitalisierung erwähnt?", key="q5")
            st.checkbox("Mandantenportal vorhanden?", key="q6")

with tab3:
    st.subheader("📋 Steuerberater Lead-Liste")
    st.info("📊 Importiere die SBS_Steuerberater_Prospect_Liste.xlsx oder füge manuell Leads hinzu")

    uploaded = st.file_uploader("CSV/XLSX mit Leads hochladen", type=['csv', 'xlsx'])

    if uploaded:
        if uploaded.name.endswith('.csv'):
            df = pd.read_csv(uploaded)
        else:
            df = pd.read_excel(uploaded)
        st.dataframe(df, use_container_width=True)
        st.success(f"✅ {len(df)} Leads geladen")

        csv = df.to_csv(index=False)
        st.download_button("💾 Als CSV exportieren", csv, "steuerberater_leads.csv", "text/csv", use_container_width=True)

with tab4:
    st.subheader("📊 Lead Scoring Modell")

    scoring = icp.get('lead_scoring', {})
    thresholds = scoring.pop('thresholds', {})

    st.markdown("### Scoring-Kriterien")
    scoring_df = pd.DataFrame([
        {"Kriterium": k.replace('_', ' ').title(), "Punkte": v}
        for k, v in scoring.items()
    ])
    st.dataframe(scoring_df, use_container_width=True, hide_index=True)

    st.markdown("### Schwellenwerte")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("🔥 Hot (Prio A)", f"≥ {thresholds.get('hot', 60)} Punkte")
    with col2:
        st.metric("🟡 Warm (Prio B)", f"≥ {thresholds.get('warm', 35)} Punkte")
    with col3:
        st.metric("🔵 Cold (Prio C)", f"≥ {thresholds.get('cold', 15)} Punkte")

st.markdown("---")
st.caption("SBS Deutschland GmbH & Co. KG · Steuerberater-Partnerprogramm · sbsnexus.de/partner · sbsdeutschland.com/sbshomepage/")
