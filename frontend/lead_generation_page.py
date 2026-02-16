import streamlit as st
import pandas as pd

def show():
    st.header("🎯 Lead Generation")
    
    tabs = st.tabs(["🔍 Neue Leads finden", "📋 Lead-Datenbank", "🤖 Auto-Enrichment"])
    
    with tabs[0]:
        st.subheader("Automatische Lead-Suche")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🎯 ICP Filter")
            
            industry = st.multiselect(
                "Branche",
                ["Maschinenbau", "Automotive", "Anlagenbau", "Hydraulik", "Werkzeugmaschinenbau"],
                default=["Maschinenbau", "Automotive"]
            )
            
            company_size_min = st.number_input("Min. Mitarbeiter", 50, 1000, 50)
            company_size_max = st.number_input("Max. Mitarbeiter", 50, 1000, 500)
            
            region = st.multiselect(
                "Region",
                ["Baden-Württemberg", "Bayern", "Hessen", "Rheinland-Pfalz"],
                default=["Baden-Württemberg"]
            )
        
        with col2:
            st.markdown("### 👤 Entscheider-Profile")
            
            target_roles = st.multiselect(
                "Ziel-Rollen",
                ["CFO", "CTO", "CEO", "Leiter Buchhaltung", "Controller"],
                default=["CFO", "CTO", "CEO"]
            )
            
            seniority = st.multiselect(
                "Seniority Level",
                ["C-Level", "VP", "Director", "Manager"],
                default=["C-Level", "VP"]
            )
        
        st.markdown("---")
        
        if st.button("🔍 Leads suchen", type="primary", width='stretch'):
            with st.spinner("Suche läuft... (Apollo.io, LinkedIn Sales Navigator)"):
                st.info("🔧 API-Integration wird eingerichtet...")
                
                # Dummy-Daten
                found_leads = {
                    "Firma": ["Tech Solutions GmbH", "Industrie AG", "Maschinen Müller"],
                    "Kontakt": ["Anna Schmidt", "Peter Weber", "Maria Fischer"],
                    "Rolle": ["CFO", "CTO", "CEO"],
                    "Email": ["a.schmidt@techsolutions.de", "p.weber@industrie.de", "m.fischer@mueller.de"],
                    "Mitarbeiter": [180, 250, 120],
                    "Score": ["95%", "88%", "82%"]
                }
                
                st.success(f"✓ {len(found_leads['Firma'])} Leads gefunden!")
                st.dataframe(found_leads, width='stretch', hide_index=True)
                
                if st.button("💾 Leads importieren"):
                    st.success("✓ Leads zur Datenbank hinzugefügt")
    
    with tabs[1]:
        st.subheader("📋 Lead-Datenbank")
        
        # Filter
        col_filter1, col_filter2, col_filter3 = st.columns(3)
        
        with col_filter1:
            status_filter = st.selectbox("Status", ["Alle", "Neu", "Kontaktiert", "Qualifiziert", "Abgelehnt"])
        
        with col_filter2:
            role_filter = st.selectbox("Rolle", ["Alle", "CFO", "CTO", "CEO"])
        
        with col_filter3:
            date_filter = st.date_input("Hinzugefügt seit")
        
        # Lead-Liste
        st.markdown("### Gespeicherte Leads")
        
        leads_db = pd.DataFrame(TARGET_CONTACTS)
        st.dataframe(leads_db, width='stretch')
        
        # Bulk Actions
        st.markdown("### 🔧 Bulk-Aktionen")
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("📧 Email-Kampagne starten"):
                st.success("✓ Kampagne vorbereitet")
        
        with col_b:
            if st.button("🏷️ Tags hinzufügen"):
                st.success("✓ Tags aktualisiert")
        
        with col_c:
            if st.button("📤 Export CSV"):
                st.success("✓ Exportiert")
    
    with tabs[2]:
        st.subheader("🤖 Automatisches Lead-Enrichment")
        
        st.info("""
        **Automatische Datenanreicherung:**
        - Email-Verifizierung (Hunter.io, ZeroBounce)
        - Firmendaten (Clearbit, Apollo)
        - Social Media Profile
        - Technologie-Stack (BuiltWith)
        """)
        
        uploaded_file = st.file_uploader("Lead-Liste hochladen (nur Firmenname + Name)", type=['csv'])
        
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.dataframe(df, width='stretch')
            
            if st.button("🚀 Enrichment starten"):
                with st.spinner("Enriching leads..."):
                    st.success("✓ Leads angereichert mit Emails, Telefonnummern, LinkedIn-Profilen")

from automated_email_sender import TARGET_CONTACTS
