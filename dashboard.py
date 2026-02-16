#!/usr/bin/env python3
"""
SBS GTM Analytics Dashboard
Echtzeit-Monitoring von Email-Kampagnen
"""
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os

st.set_page_config(
    page_title="SBS GTM Analytics", 
    page_icon="📊", 
    layout="wide"
)

# Header
st.title("📊 SBS GTM Email Campaign Analytics")
st.markdown(f"**Dashboard aktualisiert:** {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}")
st.markdown("---")

# Daten laden
try:
    df = pd.read_csv('campaign_results.csv')
    df['timestamp'] = pd.to_datetime(df['timestamp'])
except FileNotFoundError:
    st.error("❌ Keine campaign_results.csv gefunden. Bitte zuerst eine Kampagne ausführen.")
    st.stop()

# KPI Cards
col1, col2, col3, col4 = st.columns(4)

total = len(df)
sent = len(df[df['status'] == 'sent'])
failed = len(df[df['status'] == 'failed'])
success_rate = (sent/total*100) if total > 0 else 0

with col1:
    st.metric(
        label="📧 Gesamt versendet",
        value=total,
        delta=f"+{total} Kontakte"
    )

with col2:
    st.metric(
        label="✅ Erfolgreich",
        value=sent,
        delta=f"{success_rate:.1f}% Erfolgsquote"
    )

with col3:
    st.metric(
        label="❌ Fehlgeschlagen",
        value=failed,
        delta="0 Fehler" if failed == 0 else f"-{failed}"
    )

with col4:
    st.metric(
        label="📈 Performance",
        value="Ausgezeichnet" if success_rate == 100 else "Gut",
        delta=f"{success_rate:.0f}%"
    )

st.markdown("---")

# Zwei Spalten Layout
col_left, col_right = st.columns(2)

with col_left:
    # Kampagnen-Details Tabelle
    st.subheader("📋 Kampagnen-Details")
    
    # Filteroptionen
    status_filter = st.multiselect(
        "Status filtern:",
        options=df['status'].unique(),
        default=df['status'].unique()
    )
    
    filtered_df = df[df['status'].isin(status_filter)]
    
    # Formatierte Tabelle
    display_df = filtered_df[['email', 'company', 'status', 'template', 'timestamp']].copy()
    display_df['timestamp'] = display_df['timestamp'].dt.strftime('%d.%m.%Y %H:%M')
    
    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

with col_right:
    # Status-Verteilung (Pie Chart)
    st.subheader("📊 Status-Verteilung")
    
    status_counts = df['status'].value_counts()
    
    fig_pie = px.pie(
        values=status_counts.values,
        names=status_counts.index,
        color=status_counts.index,
        color_discrete_map={'sent': '#00C853', 'failed': '#FF1744'}
    )
    
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    st.plotly_chart(fig_pie, use_container_width=True)
    
    # Template-Verteilung
    st.subheader("📝 Template-Nutzung")
    
    template_counts = df['template'].value_counts()
    
    fig_bar = px.bar(
        x=template_counts.index,
        y=template_counts.values,
        labels={'x': 'Template', 'y': 'Anzahl'},
        color=template_counts.values,
        color_continuous_scale='Blues'
    )
    
    st.plotly_chart(fig_bar, use_container_width=True)

st.markdown("---")

# Timeline Visualisierung
st.subheader("⏱️ Versand-Timeline")

fig_timeline = px.scatter(
    df,
    x='timestamp',
    y='company',
    color='status',
    size=[1]*len(df),
    hover_data=['email', 'template'],
    color_discrete_map={'sent': '#00C853', 'failed': '#FF1744'}
)

fig_timeline.update_layout(
    xaxis_title="Zeitpunkt",
    yaxis_title="Firma",
    showlegend=True
)

st.plotly_chart(fig_timeline, use_container_width=True)

# Download & Export
st.markdown("---")
st.subheader("💾 Export & Downloads")

col_export1, col_export2, col_export3 = st.columns(3)

with col_export1:
    # CSV Export
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 CSV herunterladen",
        data=csv,
        file_name=f'campaign_report_{datetime.now().strftime("%Y%m%d_%H%M")}.csv',
        mime='text/csv',
    )

with col_export2:
    # Excel Export
    if st.button("📊 Excel generieren"):
        excel_file = f'campaign_report_{datetime.now().strftime("%Y%m%d_%H%M")}.xlsx'
        df.to_excel(excel_file, index=False)
        st.success(f"✓ Excel erstellt: {excel_file}")

with col_export3:
    # Resend Dashboard Link
    if st.button("🔗 Resend Dashboard öffnen"):
        st.markdown("[📧 Zu Resend Dashboard](https://resend.com/emails)")

# Footer
st.markdown("---")
st.caption("SBS Deutschland GmbH | Luis Schenk - Innovation Manager | ki@sbsdeutschland.de")
