#!/usr/bin/env python3
"""
SBS GTM Automation - Haupt-Dashboard
"""
import streamlit as st
import sys
import os

# Path Setup
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

# Page Config
st.set_page_config(
    page_title="SBS GTM Automation Hub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
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

# Header
st.markdown('<h1 class="main-header">🚀 SBS GTM Automation Hub</h1>', unsafe_allow_html=True)
st.markdown("---")

# Get current page from query params (st.query_params is the correct API)
current_page = st.query_params.get("page", "dashboard")

# Sidebar Navigation
with st.sidebar:
    st.image("https://placehold.co/200x80/667eea/ffffff?text=SBS+Deutschland", width='stretch')
    st.markdown("### 📋 Navigation")
    
    pages = {
        "🏠 Dashboard": "dashboard",
        "📧 Email Automation": "email",
        "✍️ LinkedIn Post Generator": "linkedin",
        "🎯 Lead Generation": "leads",
        "📊 Analytics & Reports": "analytics",
        "⚙️ Einstellungen": "settings",
        "🤖 Automatisierung": "automation"
    }
    
    for label, page_id in pages.items():
        if st.button(label, use_container_width=True, type="primary" if current_page == page_id else "secondary"):
            st.query_params["page"] = page_id
            st.rerun()
    
    st.markdown("---")
    st.markdown("### 👤 Benutzer")
    st.info("**Luis Schenk**\nInnovation Manager")

# Main Content Area
if current_page == "dashboard":
    st.header("📊 Übersicht")
    
    # KPI Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📧 Emails versendet (heute)", "3", "+3")
    with col2:
        st.metric("🎯 Leads generiert", "0", "0")
    with col3:
        st.metric("✍️ LinkedIn Posts", "0", "0")
    with col4:
        st.metric("📈 Erfolgsrate", "100%", "+100%")
    
    st.markdown("---")
    st.subheader("🎯 Schnellzugriff")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("📧 Neue Email senden", use_container_width=True):
            st.query_params["page"] = "email"
            st.rerun()
    with col2:
        if st.button("✍️ LinkedIn Post erstellen", use_container_width=True):
            st.query_params["page"] = "linkedin"
            st.rerun()
    with col3:
        if st.button("🎯 Leads generieren", use_container_width=True):
            st.query_params["page"] = "leads"
            st.rerun()

elif current_page == "email":
    try:
        import email_automation_page
        email_automation_page.show()
    except Exception as e:
        st.error(f"❌ Fehler beim Laden: {e}")
        st.exception(e)

elif current_page == "linkedin":
    try:
        import linkedin_page
        linkedin_page.show()
    except Exception as e:
        st.error(f"❌ Fehler: {e}")
        st.exception(e)

elif current_page == "leads":
    try:
        import lead_generation_page
        lead_generation_page.show()
    except Exception as e:
        st.error(f"❌ Fehler: {e}")
        st.exception(e)

elif current_page == "analytics":
    try:
        import analytics_page
        analytics_page.show()
    except Exception as e:
        st.error(f"❌ Fehler: {e}")
        st.exception(e)

elif current_page == "settings":
    try:
        import settings_page
        settings_page.show()
    except Exception as e:
        st.error(f"❌ Fehler: {e}")
        st.exception(e)

elif current_page == "automation":
    try:
        import automation_page
        automation_page.show()
    except Exception as e:
        st.error(f"❌ Fehler: {e}")
        st.exception(e)

# Footer
st.markdown("---")
st.caption("SBS Deutschland GmbH | Luis Schenk - Innovation Manager | Version 1.0.0")
