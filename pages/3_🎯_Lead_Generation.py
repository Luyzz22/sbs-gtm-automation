import streamlit as st
import yaml
from pathlib import Path
import pandas as pd

st.set_page_config(page_title="Lead Generation", page_icon="🎯")

st.title("🎯 Lead Generation")

# Load ICP Config
config_path = Path("config")
icp_file = config_path / "icp_filters.yaml"

if not icp_file.exists():
    st.error("❌ config/icp_filters.yaml nicht gefunden!")
    st.info("Erstelle Datei mit: python sbs_gtm.py")
    st.stop()

try:
    with open(icp_file, 'r', encoding='utf-8') as f:
        icp = yaml.safe_load(f)
except Exception as e:
    st.error(f"Fehler beim Laden: {str(e)}")
    st.stop()

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
    st.subheader("🔍 Lead-Suche")
    
    st.info("💡 **Sales Navigator Integration**: Automatische Lead-Suche basierend auf ICP")
    
    col1, col2, col3 = st.columns(3)
    
    industries = filters.get('industries', [])
    regions = filters.get('regions', [])
    company_size = filters.get('company_size', {})
    
    with col1:
        search_industry = st.selectbox("Branche filtern", ["Alle"] + industries)
    
    with col2:
        search_size_min = st.number_input("Min. Mitarbeiter", 
                                          value=company_size.get('min', 100))
    
    with col3:
        search_region = st.selectbox("Region", ["Alle"] + regions)
    
    if st.button("🔍 Suche starten", type="primary", use_container_width=True):
        with st.spinner("Suche Leads..."):
            st.warning("⚠️ LinkedIn Sales Navigator API Integration in Entwicklung")
            
            # Mock-Daten basierend auf Filter
            mock_leads = [
                {
                    "Name": "Dr. Thomas Weber", 
                    "Position": "Geschäftsführer", 
                    "Unternehmen": "PrecisionTech GmbH", 
                    "Mitarbeiter": 250, 
                    "Region": "Baden-Württemberg",
                    "Branche": "Maschinenbau"
                },
                {
                    "Name": "Anna Schmidt", 
                    "Position": "CFO", 
                    "Unternehmen": "AutoParts AG", 
                    "Mitarbeiter": 380, 
                    "Region": "Bayern",
                    "Branche": "Automobilzulieferer"
                },
                {
                    "Name": "Michael Hoffmann", 
                    "Position": "CTO", 
                    "Unternehmen": "MachineWorks", 
                    "Mitarbeiter": 180, 
                    "Region": "Nordrhein-Westfalen",
                    "Branche": "Werkzeugbau"
                },
            ]
            
            df = pd.DataFrame(mock_leads)
            
            # Filter anwenden
            if search_industry != "Alle":
                df = df[df['Branche'] == search_industry]
            
            if search_region != "Alle":
                df = df[df['Region'] == search_region]
            
            df = df[df['Mitarbeiter'] >= search_size_min]
            
            st.success(f"✅ {len(df)} Leads gefunden")
            st.dataframe(df, use_container_width=True, hide_index=True)

with tab3:
    st.subheader("📋 Gespeicherte Leads")
    
    st.info("📊 Lead-Datenbank - Import/Export Funktionen")
    
    uploaded = st.file_uploader("CSV mit Leads hochladen", type=['csv'])
    
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df, use_container_width=True)
        
        st.success(f"✅ {len(df)} Leads geladen")
    else:
        st.caption("💡 Upload eine CSV-Datei um Leads zu importieren")
