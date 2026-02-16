import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime, timedelta
import json

st.set_page_config(page_title="Analytics", page_icon="📊", layout="wide")

st.title("📊 Analytics Dashboard")

# Versuche echte Daten zu laden
results_file = Path("campaign_results.csv")
has_real_data = results_file.exists()

if has_real_data:
    df = pd.read_csv(results_file)
    
    total_sent = len(df[df['status'] == 'sent'])
    total_failed = len(df[df['status'] == 'failed'])
    success_rate = (total_sent / len(df) * 100) if len(df) > 0 else 0
    
    st.success("✅ Echte Kampagnen-Daten geladen")
else:
    st.info("💡 Starte eine Email-Kampagne um echte Daten zu sehen")
    total_sent = 8
    total_failed = 2
    success_rate = 80.0

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Emails gesendet", total_sent, f"+{total_sent // 3}")

with col2:
    st.metric("Erfolgsquote", f"{success_rate:.1f}%", 
              "🟢" if success_rate > 90 else "🟡" if success_rate > 70 else "🔴")

with col3:
    if has_real_data:
        unique_companies = df['company'].nunique()
        st.metric("Unternehmen erreicht", unique_companies)
    else:
        st.metric("LinkedIn Posts (30d)", "8", "+2")

with col4:
    st.metric("Fehlgeschlagen", total_failed, 
              "🟢" if total_failed == 0 else "🟡")

st.markdown("---")

tab1, tab2, tab3 = st.tabs(["📈 Email Performance", "📊 Templates", "🎯 Kampagnen-Verlauf"])

with tab1:
    st.subheader("📧 Email Campaign Analytics")
    
    if has_real_data:
        st.dataframe(df, use_container_width=True)
        
        # Erfolgsrate nach Template
        if 'template' in df.columns:
            template_stats = df.groupby('template')['status'].value_counts().unstack(fill_value=0)
            st.markdown("### 📋 Performance nach Template")
            st.bar_chart(template_stats)
        
        # Timeline
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            daily_stats = df.groupby(df['timestamp'].dt.date).size()
            st.markdown("### 📅 Versand-Timeline")
            st.line_chart(daily_stats)
    else:
        st.info("🔜 Keine Email-Kampagnen Daten verfügbar")
        
        mock_data = pd.DataFrame({
            'Email': ['max@example.de', 'anna@example.de', 'thomas@example.de'],
            'Unternehmen': ['TechCorp', 'MachineWorks', 'Precision'],
            'Status': ['✅ Gesendet', '✅ Gesendet', '❌ Fehler'],
            'Template': ['CEO', 'CTO', 'CFO'],
            'Timestamp': [datetime.now() - timedelta(hours=i) for i in range(3)]
        })
        st.dataframe(mock_data, use_container_width=True)

with tab2:
    st.subheader("📋 Template-Analyse")
    
    template_data = pd.DataFrame({
        'Template': ['CEO Template', 'CFO Template', 'CTO Template'],
        'Verwendet': [12, 8, 5],
        'Erfolgsquote': ['92%', '88%', '80%']
    })
    
    st.dataframe(template_data, use_container_width=True)
    st.bar_chart(template_data.set_index('Template')['Verwendet'])

with tab3:
    st.subheader("🎯 Kampagnen-Verlauf")
    
    if has_real_data:
        st.success(f"✅ Letzte Kampagne: {df['timestamp'].max()}")
        st.metric("Gesamt versendet (all time)", len(df))
    else:
        st.info("Noch keine Kampagnen durchgeführt")

st.markdown("---")

if not has_real_data:
    st.caption("💡 **Hinweis:** Dies sind Beispiel-Daten. Starte Email-Kampagnen um echte Analytics zu sehen.")
else:
    st.caption(f"📊 Daten aktualisiert: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
