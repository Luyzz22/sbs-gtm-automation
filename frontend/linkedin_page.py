import streamlit as st
import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

def show():
    st.header("✍️ LinkedIn Post Generator")
    
    tabs = st.tabs(["📝 Neuer Post", "📅 Content-Kalender", "📊 Performance"])
    
    with tabs[0]:
        st.subheader("Neuen LinkedIn Post erstellen")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            topic = st.text_input("Thema / Kernbotschaft", placeholder="z.B. KI-gestützte Rechnungsverarbeitung")
            
            tone = st.selectbox(
                "Tonalität",
                ["Professional", "Thought Leadership", "Casual", "Educational", "Storytelling"]
            )
            
            length = st.selectbox(
                "Länge",
                ["Kurz (100-150 Wörter)", "Mittel (150-250 Wörter)", "Lang (250+ Wörter)"]
            )
            
            include_cta = st.checkbox("Call-to-Action einbinden", value=True)
            include_hashtags = st.checkbox("Hashtags generieren", value=True)
            
            additional_info = st.text_area(
                "Zusätzliche Informationen (optional)",
                placeholder="Fakten, Statistiken, persönliche Erfahrungen..."
            )
        
        with col2:
            st.markdown("### 💡 Tipps")
            st.info("""
            **Best Practices:**
            - Erster Satz entscheidend
            - Persönliche Story einbauen
            - Max. 5 Hashtags
            - Emojis sparsam nutzen
            - Frage ans Ende
            """)
        
        if st.button("✨ Post generieren", type="primary", width='stretch'):
            with st.spinner("KI generiert LinkedIn Post..."):
                # Prompt für GPT-4
                prompt = f"""
                Erstelle einen professionellen LinkedIn Post zum Thema: {topic}
                
                Tonalität: {tone}
                Länge: {length}
                Include CTA: {include_cta}
                Include Hashtags: {include_hashtags}
                
                Zusätzliche Infos: {additional_info}
                
                Der Post sollte für Luis Schenk (Innovation Manager, SBS Deutschland) sein,
                ein B2B SaaS Unternehmen im Bereich KI-gestützte Contract Intelligence.
                
                Format: LinkedIn-optimiert mit Absätzen und Emojis.
                """
                
                try:
                    response = openai.ChatCompletion.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "Du bist ein LinkedIn Content Expert für B2B SaaS Marketing."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.7
                    )
                    
                    generated_post = response.choices[0].message.content
                    
                    st.markdown("### 📄 Generierter Post")
                    st.text_area("", generated_post, height=300)
                    
                    col_a, col_b, col_c = st.columns(3)
                    
                    with col_a:
                        if st.button("📋 Kopieren"):
                            st.success("✓ In Zwischenablage kopiert")
                    
                    with col_b:
                        if st.button("💾 Speichern"):
                            st.success("✓ Post gespeichert")
                    
                    with col_c:
                        if st.button("🔄 Neu generieren"):
                            st.rerun()
                
                except Exception as e:
                    st.error(f"Fehler: {str(e)}")
    
    with tabs[1]:
        st.subheader("📅 Content-Kalender")
        
        import datetime
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            selected_date = st.date_input("Datum", datetime.date.today())
        
        with col2:
            post_frequency = st.selectbox("Frequenz", ["Täglich", "3x Woche", "Wöchentlich"])
        
        st.markdown("### Geplante Posts")
        
        calendar_data = {
            "Datum": ["17.02.2026", "19.02.2026", "21.02.2026"],
            "Thema": ["KI in der Buchhaltung", "Digital Transformation", "Erfolgsgeschichte"],
            "Status": ["📝 Entwurf", "⏰ Geplant", "⏰ Geplant"]
        }
        
        st.dataframe(calendar_data, width='stretch', hide_index=True)
    
    with tabs[2]:
        st.subheader("📊 Post Performance")
        
        st.info("LinkedIn API Integration erforderlich für Live-Daten")
        
        metrics_col1, metrics_col2, metrics_col3, metrics_col4 = st.columns(4)
        
        metrics_col1.metric("👁️ Impressions", "0")
        metrics_col2.metric("👍 Reactions", "0")
        metrics_col3.metric("💬 Comments", "0")
        metrics_col4.metric("🔄 Shares", "0")
