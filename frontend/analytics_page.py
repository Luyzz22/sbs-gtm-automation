import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

def show():
    st.header("📊 Analytics & Reports")
    
    tabs = st.tabs(["📈 Overview", "📧 Email-Metriken", "🎯 Lead-Pipeline", "💰 ROI-Tracking"])
    
    with tabs[0]:
        st.subheader("Performance Overview")
        
        # KPIs
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("📧 Emails (30 Tage)", "3", delta="+3")
        col2.metric("✅ Zustellrate", "100%", delta="+100%")
        col3.metric("👁️ Öffnungsrate", "-", delta="N/A")
        col4.metric("🎯 Reply-Rate", "-", delta="N/A")
        
        st.markdown("---")
        
        # Chart: Emails over time
        chart_data = pd.DataFrame({
            'Datum': pd.date_range('2026-02-10', periods=7),
            'Emails': [0, 0, 0, 0, 0, 0, 3]
        })
        
        fig = px.line(chart_data, x='Datum', y='Emails', title='Email-Versand (letzte 7 Tage)')
        st.plotly_chart(fig, width='stretch')
    
    with tabs[1]:
        st.subheader("📧 Email-Performance")
        
        try:
            df = pd.read_csv('campaign_results.csv')
            
            # Template Performance
            template_stats = df['template'].value_counts()
            
            fig_pie = px.pie(
                values=template_stats.values,
                names=template_stats.index,
                title='Template-Verteilung'
            )
            
            st.plotly_chart(fig_pie, width='stretch')
            
        except FileNotFoundError:
            st.info("Keine Daten verfügbar")
    
    with tabs[2]:
        st.subheader("🎯 Lead-Pipeline")
        
        # Funnel Chart
        funnel_data = {
            'Stage': ['Leads gefunden', 'Emails versendet', 'Emails geöffnet', 'Antworten', 'Qualifiziert'],
            'Count': [50, 30, 15, 5, 2]
        }
        
        fig_funnel = go.Figure(go.Funnel(
            y=funnel_data['Stage'],
            x=funnel_data['Count'],
            textinfo="value+percent initial"
        ))
        
        fig_funnel.update_layout(title='Lead-to-Customer Funnel')
        st.plotly_chart(fig_funnel, width='stretch')
    
    with tabs[3]:
        st.subheader("💰 ROI-Tracking")
        
        st.info("ROI-Tracking wird implementiert wenn erste Deals abgeschlossen wurden")
        
        col_roi1, col_roi2, col_roi3 = st.columns(3)
        
        col_roi1.metric("💵 Investiert", "0€")
        col_roi2.metric("💰 Pipeline-Value", "0€")
        col_roi3.metric("📈 ROI", "-%")
