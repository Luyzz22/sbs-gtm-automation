import streamlit as st
import os
import yaml
from pathlib import Path
import openai
from datetime import datetime

st.set_page_config(page_title="LinkedIn Posts", page_icon="✍️")

st.title("✍️ LinkedIn Posts Automation")

# Load Config
config_path = Path("config")
calendar_file = config_path / "content_calendar.yaml"

if not calendar_file.exists():
    st.error("❌ config/content_calendar.yaml nicht gefunden!")
    st.info("💡 Bitte erstelle die Datei oder führe Setup aus")
    st.stop()

try:
    with open(calendar_file, 'r', encoding='utf-8') as f:
        calendar = yaml.safe_load(f)
except Exception as e:
    st.error(f"❌ Fehler beim Laden: {str(e)}")
    st.stop()

# Sidebar
with st.sidebar:
    st.header("⚙️ Post-Einstellungen")
    
    openai_key = st.text_input("OpenAI API Key", type="password", value=os.getenv('OPENAI_API_KEY', ''))
    if openai_key:
        os.environ['OPENAI_API_KEY'] = openai_key
        openai.api_key = openai_key
    
    tone = st.selectbox("Tonalität", ["Professionell", "Informativ", "Thought Leadership"])
    length = st.slider("Länge (Wörter)", 100, 400, 250)

# Main Content
tab1, tab2, tab3 = st.tabs(["📝 Neuer Post", "📅 Content-Kalender", "📊 Posting-Plan"])

with tab1:
    st.subheader("Post generieren")
    
    themes = calendar.get('content_themes', [])
    
    if not themes:
        st.warning("⚠️ Keine Content-Themen in content_calendar.yaml gefunden!")
        st.info("Füge Content-Themen in config/content_calendar.yaml hinzu")
        st.stop()
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        theme_options = {f"{t['title']} ({t['category']})": t for t in themes}
        selected_theme = st.selectbox("Wähle Content-Thema", options=list(theme_options.keys()))
        
        if selected_theme:
            theme = theme_options[selected_theme]
            
            st.info(f"**Kategorie:** {theme.get('category', 'N/A')}")
            st.write(f"**Keywords:** {', '.join(theme.get('keywords', []))}")
    
    with col2:
        st.metric("Empfohlene Länge", f"{length} Wörter")
        if selected_theme:
            theme = theme_options[selected_theme]
            st.metric("Hashtags", len(theme.get('keywords', [])))
    
    custom_prompt = st.text_area("Zusätzliche Anweisungen (optional)", 
                                  placeholder="z.B. Erwähne Fallbeispiel aus Maschinenbau...")
    
    if st.button("✨ Post generieren", type="primary", use_container_width=True):
        if not openai_key:
            st.error("❌ Bitte OpenAI API Key eingeben!")
        elif not selected_theme:
            st.error("❌ Bitte Content-Thema auswählen!")
        else:
            with st.spinner("🤖 Generiere LinkedIn Post..."):
                try:
                    theme = theme_options[selected_theme]
                    
                    prompt = f"""Erstelle einen professionellen LinkedIn-Post für SBS Deutschland:

THEMA: {theme['title']}
KATEGORIE: {theme.get('category', 'Business')}
KEYWORDS: {', '.join(theme.get('keywords', []))}

TONALITÄT: {tone}
LÄNGE: Ca. {length} Wörter

STIL:
- Professionell und seriös
- Thought Leadership im deutschen Mittelstand
- Konkrete Insights, keine Marketing-Floskeln
- Deutsche Business-Etikette

STRUKTUR:
1. Hook (erste Zeile muss fesseln)
2. Hauptaussage mit konkretem Mehrwert
3. Beispiel oder Insights
4. Call-to-Action (subtil)
5. Relevante Hashtags

{f"ZUSATZ: {custom_prompt}" if custom_prompt else ""}

Schreibe NUR den Post, keine Metakommentare."""

                    response = openai.chat.completions.create(
                        model="gpt-4",
                        messages=[
                            {"role": "system", "content": "Du bist LinkedIn Content-Experte für B2B Enterprise im deutschen Mittelstand."},
                            {"role": "user", "content": prompt}
                        ],
                        temperature=0.8,
                        max_tokens=600
                    )
                    
                    post_content = response.choices[0].message.content.strip()
                    
                    st.session_state['generated_post'] = post_content
                    st.session_state['post_theme'] = theme['title']
                    
                    st.success("✅ Post erfolgreich generiert!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Fehler: {str(e)}")
    
    # Anzeige generierter Post
    if 'generated_post' in st.session_state:
        st.markdown("---")
        st.subheader("📄 Generierter Post")
        
        post_text = st.text_area(
            "Post-Text (editierbar)",
            value=st.session_state['generated_post'],
            height=300,
            key="post_display"
        )
        
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            if st.button("📤 Auf LinkedIn posten", use_container_width=True):
                st.warning("⚠️ LinkedIn API Integration in Entwicklung")
        
        with col_b:
            if st.button("🔄 Neu generieren", use_container_width=True):
                del st.session_state['generated_post']
                st.rerun()
        
        with col_c:
            st.download_button(
                "💾 Speichern",
                data=post_text,
                file_name=f"linkedin_post_{datetime.now().strftime('%Y%m%d_%H%M')}.txt",
                mime="text/plain",
                use_container_width=True
            )

with tab2:
    st.subheader("📅 Content-Kalender")
    
    schedule = calendar.get('schedule', {})
    
    if schedule:
        st.metric("Posting-Frequenz", schedule.get('posting_frequency', 'N/A'))
        
        st.markdown("### 🕒 Optimale Posting-Zeiten")
        
        for time_slot in schedule.get('optimal_times', []):
            with st.expander(f"**{time_slot.get('day', 'N/A')}** um {time_slot.get('time', 'N/A')}"):
                st.write(f"**Grund:** {time_slot.get('reason', 'N/A')}")
    else:
        st.info("📅 Keine Scheduling-Informationen verfügbar")

with tab3:
    st.subheader("📊 Content-Themen Übersicht")
    
    if themes:
        for i, theme in enumerate(themes, 1):
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**{i}. {theme.get('title', 'Unbekannt')}**")
                    st.caption(f"Kategorie: {theme.get('category', 'N/A')}")
                
                with col2:
                    if st.button("Nutzen", key=f"use_theme_{i}"):
                        st.info("Feature in Entwicklung")
                
                st.markdown("---")
    else:
        st.info("Keine Content-Themen definiert")
