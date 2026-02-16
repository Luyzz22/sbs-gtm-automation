#!/usr/bin/env python3
"""
SBS GTM Automation - Haupt-Dashboard
"""
import streamlit as st

# Page Config
st.set_page_config(
    page_title="SBS GTM Automation Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        padding: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<h1 class="main-header">🚀 SBS GTM Automation Hub</h1>', unsafe_allow_html=True)
st.markdown("---")

# Sidebar Info
with st.sidebar:
    st.image("https://placehold.co/200x80/667eea/ffffff?text=SBS+Deutschland", width='stretch')
    st.markdown("---")
    st.markdown("### 👤 Benutzer")
    st.info("**Luis Schenk**\nInnovation Manager")
    st.markdown("---")
    st.caption("Version 1.0.0")

# Dashboard Content
st.header("📊 Übersicht")

# KPI Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("📧 Emails versendet", "3", "+3")
with col2:
    st.metric("🎯 Leads generiert", "0", "0")
with col3:
    st.metric("✍️ LinkedIn Posts", "0", "0")
with col4:
    st.metric("📈 Erfolgsrate", "100%", "+100%")

st.markdown("---")

# Quick Actions
st.subheader("🎯 Schnellzugriff")

col1, col2, col3 = st.columns(3)

with col1:
    st.page_link("pages/1_📧_Email_Automation.py", label="📧 Email Automation", icon="📧")
    st.markdown("Erstellen und versenden Sie automatisierte Emails")

with col2:
    st.page_link("pages/2_✍️_LinkedIn_Posts.py", label="✍️ LinkedIn Posts", icon="✍️")
    st.markdown("Generieren Sie LinkedIn-Inhalte mit KI")

with col3:
    st.page_link("pages/3_🎯_Lead_Generation.py", label="🎯 Lead Generation", icon="🎯")
    st.markdown("Finden und qualifizieren Sie neue Leads")

st.markdown("---")

# Recent Activity
st.subheader("📋 Letzte Aktivitäten")
st.info("Noch keine Aktivitäten vorhanden. Starten Sie mit der Email-Automation!")

# Footer
st.markdown("---")
st.caption("SBS Deutschland GmbH | Luis Schenk - Innovation Manager")
