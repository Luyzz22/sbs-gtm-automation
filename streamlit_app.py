#!/usr/bin/env python3
"""
SBS Nexus GTM Automation Hub
Enterprise Go-to-Market Automatisierung für SBS Deutschland GmbH & Co. KG
Plattform: Finance Intelligence · Contract Intelligence · Technical Intelligence
"""
import streamlit as st

st.set_page_config(
    page_title="SBS Nexus – GTM Automation",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# SBS Corporate Design
SBS_BLUE = "#003856"
SBS_YELLOW = "#FFB900"
SBS_ORANGE = "#F97316"

st.markdown(f"""
<style>
    .main-header {{
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, {SBS_BLUE} 0%, #005a8c 50%, {SBS_ORANGE} 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 0.5rem 0;
    }}
    .sub-header {{
        text-align: center;
        color: #64748b;
        font-size: 1.05rem;
        margin-top: -0.5rem;
    }}
    .stMetric > div {{
        border-left: 3px solid {SBS_ORANGE};
        padding-left: 12px;
    }}
    .product-card {{
        background: linear-gradient(135deg, #f8fafc, #f1f5f9);
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }}
    .module-card {{
        background: linear-gradient(135deg, #0f172a, #1e293b);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 1.2rem;
        margin-bottom: 0.8rem;
        color: white;
    }}
    .module-card h4 {{ color: {SBS_ORANGE}; margin-bottom: 0.5rem; }}
    .module-card p {{ color: #cbd5e1; font-size: 0.9rem; }}
    a {{ color: {SBS_ORANGE}; }}
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">⚡ SBS Nexus GTM Automation</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Enterprise Go-to-Market · Finance · Contract · Technical Intelligence · DATEV & SAP Integration</p>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar
with st.sidebar:
    st.markdown(f"""
    <div style="text-align:center; padding: 1rem; background: linear-gradient(135deg, {SBS_BLUE}, #0f172a); border-radius: 12px; margin-bottom: 1rem;">
        <h2 style="color: {SBS_ORANGE}; margin: 0; font-size: 1.6rem;">SBS Nexus</h2>
        <p style="color: #94a3b8; margin: 0; font-size: 0.8rem;">Deutschland GmbH & Co. KG</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("### 🏢 Plattform")
    st.markdown("""
    - [🌐 SBS Homepage](https://sbsdeutschland.com/sbshomepage/)
    - [⚡ SBS Nexus](https://www.sbsnexus.de)
    - [📊 SBS Nexus App](https://sbsdeutschland.com/sbshomepage/)
    - [📄 Contract Intelligence](https://contract.sbsdeutschland.com/)
    - [🔧 HydraulikDoc AI](https://www.linkedin.com/company/hydraulikdoc-ai/)
    - [🤝 Partner-Programm](https://www.sbsnexus.de/partner)
    """)
    st.markdown("---")
    st.markdown("### 🔗 LinkedIn")
    st.markdown("""
    - [SBS Deutschland](https://www.linkedin.com/company/sbs-deutschland-gmbh-co-kg/)
    - [HydraulikDoc AI](https://www.linkedin.com/company/hydraulikdoc-ai/)
    """)
    st.markdown("---")
    st.markdown("### 📅 Discovery Call")
    st.markdown("[🗓️ 30-Min Demo buchen](https://calendly.com/ki-sbsdeutschland/sbs-nexus-30-minuten-discovery-call)")
    st.markdown("---")
    st.markdown("### 👤 Benutzer")
    st.info("**Luis Orozco**\nGründer & CEO")
    st.caption("Version 3.0.0 · Enterprise Edition")

# KPI Metrics
st.header("📊 GTM Command Center")

col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    st.metric("🎯 StB-Leads", "50", "+50")
with col2:
    st.metric("📧 Emails ready", "7", "Prio A")
with col3:
    st.metric("✍️ Content", "12", "Themen")
with col4:
    st.metric("💰 Revenue Share", "15-25%", "Partner")
with col5:
    st.metric("🏢 Module", "3", "Live")

st.markdown("---")

# SBS Nexus Platform — 3 Module
st.subheader("⚡ SBS Nexus Plattform – Das operative OS für den Mittelstand")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="module-card">
    <h4>💰 Finance Intelligence</h4>
    <p><b>KI-Rechnungsverarbeitung</b><br>
    8 Sek. · 99,2% Genauigkeit · DATEV-Export<br>
    XRechnung · ZUGFeRD · PDF<br>
    Budget-Dashboard · Zahlungen & Skonto<br>
    <i>→ Fokus: Steuerberater & KMU</i></p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="module-card">
    <h4>📄 Contract Intelligence</h4>
    <p><b>KI-Vertragsanalyse</b><br>
    Automatische Klauselerkennung<br>
    Fristenmanagement · Risikoanalyse<br>
    Kündigungsfristen-Alarm<br>
    <i>→ contract.sbsdeutschland.com</i></p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="module-card">
    <h4>🔧 Technical Intelligence</h4>
    <p><b>HydraulikDoc AI</b><br>
    Technische Dokumenten-KI (RAG)<br>
    Datenblätter · Handbücher · Normen<br>
    Bosch Rexroth · Industriehydraulik<br>
    <i>→ Fokus: Fertigender Mittelstand</i></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Zielgruppe & Markt
st.subheader("🎯 Markt & Zielgruppen")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("""
    <div class="product-card">
    <h4>🏛️ Steuerberater (Primär)</h4>
    <p><b>89.000 StB</b> in Deutschland<br>
    €21,3 Mrd. Marktvolumen<br>
    DATEV 90%+ Marktanteil<br>
    Fokus: Digitale DATEV-Kanzleien</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="product-card">
    <h4>🏭 Fertigender Mittelstand</h4>
    <p><b>SAP & DATEV</b> Umgebungen<br>
    50-5.000 Mitarbeiter<br>
    Maschinenbau · Automotive · Chemie<br>
    Fokus: Rhein-Neckar & DACH</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="product-card">
    <h4>🤝 Partner-Programm</h4>
    <p><b>3-Tier Revenue Share</b><br>
    15-25% dauerhaft pro Mandant<br>
    14-Tage-Onboarding · Keine Vorabkosten<br>
    <a href="https://www.sbsnexus.de/partner" target="_blank">sbsnexus.de/partner →</a></p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# Quick Actions
st.subheader("🚀 Schnellzugriff")

col1, col2, col3 = st.columns(3)
with col1:
    st.page_link("pages/1_📧_Email_Automation.py", label="📧 Email Automation", icon="📧")
    st.markdown("KI-personalisierte Outreach-Emails für Steuerberater & Industriekunden")

with col2:
    st.page_link("pages/2_✍️_LinkedIn_Posts.py", label="✍️ LinkedIn Posts", icon="✍️")
    st.markdown("Content für SBS Deutschland & HydraulikDoc AI – alle 3 Module")

with col3:
    st.page_link("pages/3_🎯_Lead_Generation.py", label="🎯 Lead Generation", icon="🎯")
    st.markdown("Leads finden, qualifizieren & in die Pipeline – StB & Industrie")

st.markdown("---")

# GTM Arsenal Status
st.subheader("📋 GTM Arsenal – 13 Building Blocks")

arsenal = {
    "GTM Playbook (DOCX)": "✅",
    "Blog SEO-Artikel (2x live)": "✅",
    "Steuerberater-Partnerschaftsstrategie": "✅",
    "Partner Landing Page (sbsnexus.de/partner)": "✅",
    "Case Study Template": "✅",
    "Webinar-Konzept (6 Sessions)": "✅",
    "ROI-Infografik (PDF)": "✅",
    "LinkedIn Optimization Pack": "✅",
    "Outreach Execution Kit": "✅",
    "CRM Tracking Template (XLSX)": "✅",
    "Prospect-Datenbank (50 Kontakte)": "✅",
    "Sendefertige E-Mails (7 Prio A)": "✅",
    "GTM Automation Tool (diese App)": "✅",
}

cols = st.columns(3)
for idx, (item, status) in enumerate(arsenal.items()):
    with cols[idx % 3]:
        st.markdown(f"{status} {item}")

# Footer
st.markdown("---")
st.markdown(f"""
<div style="text-align:center; color: #94a3b8; font-size: 0.85rem;">
    <b>SBS Deutschland GmbH & Co. KG</b> · Weinheim · Luis Orozco, Gründer & CEO<br>
    <a href="https://sbsdeutschland.com/sbshomepage/">Homepage</a> ·
    <a href="https://www.sbsnexus.de">SBS Nexus</a> ·
    <a href="https://contract.sbsdeutschland.com/">Contracts</a> ·
    <a href="https://www.sbsnexus.de/partner">Partner</a> ·
    <a href="https://calendly.com/ki-sbsdeutschland/sbs-nexus-30-minuten-discovery-call">Demo buchen</a> ·
    <a href="https://www.linkedin.com/company/sbs-deutschland-gmbh-co-kg/">LinkedIn</a>
</div>
""", unsafe_allow_html=True)
