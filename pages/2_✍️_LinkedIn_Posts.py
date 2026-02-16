import streamlit as st
import os
import yaml
from pathlib import Path
from datetime import datetime
import time

st.set_page_config(page_title="LinkedIn Posts", page_icon="✍️")

st.title("✍️ LinkedIn Posts Automation")

# Load Config
config_path = Path("config")
calendar_file = config_path / "content_calendar.yaml"

if not calendar_file.exists():
    st.error("❌ config/content_calendar.yaml nicht gefunden!")
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
    
    tone = st.selectbox("Tonalität", ["Professionell", "Informativ", "Thought Leadership"])
    length = st.slider("Länge (Wörter)", 100, 400, 250)

# Helper function for OpenAI calls
def generate_with_openai(prompt, system_prompt="Du bist LinkedIn Content-Experte."):
    """Generate content using OpenAI API"""
    if not openai_key:
        raise ValueError("API Key fehlt")
    
    from openai import OpenAI
    client = OpenAI(api_key=openai_key)
    
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": prompt}
        ],
        temperature=0.8,
        max_tokens=600
    )
    
    return response.choices[0].message.content.strip()

# Main Content
tab1, tab2, tab3, tab4 = st.tabs(["📝 Neuer Post", "📚 Post-Serie", "📅 Content-Kalender", "📊 Posting-Plan"])

with tab1:
    st.subheader("Post generieren")
    
    themes = calendar.get('content_themes', [])
    
    if not themes:
        st.warning("⚠️ Keine Content-Themen gefunden!")
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
- Konkrete Insights

STRUKTUR:
1. Hook
2. Hauptaussage mit Mehrwert
3. Beispiel
4. Call-to-Action
5. Hashtags

{f"ZUSATZ: {custom_prompt}" if custom_prompt else ""}

Schreibe NUR den Post."""

                    post_content = generate_with_openai(
                        prompt, 
                        "Du bist LinkedIn Content-Experte für B2B Enterprise im deutschen Mittelstand."
                    )
                    
                    st.session_state['generated_post'] = post_content
                    st.session_state['post_theme'] = theme['title']
                    
                    st.success("✅ Post erfolgreich generiert!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"❌ Fehler: {str(e)}")
    
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
    st.subheader("📚 Content-Serie generieren")
    st.info("💡 Erstelle automatisch eine Serie von 5 LinkedIn Posts")
    
    serie_theme = st.text_input("Hauptthema der Serie", 
                                placeholder="z.B. Digital Transformation im Mittelstand")
    
    serie_style = st.selectbox("Stil der Serie", 
                              ["Professionell", "Educational", "Thought Leadership", "Storytelling"])
    
    if st.button("🚀 Serie generieren (5 Posts)", type="primary", use_container_width=True):
        if not openai_key:
            st.error("❌ Bitte OpenAI API Key eingeben!")
        elif not serie_theme:
            st.error("❌ Bitte Thema eingeben!")
        else:
            progress_bar = st.progress(0)
            status = st.empty()
            
            generated_serie = []
            
            post_fokus = [
                "Einführung: Problem Statement",
                "Ursachen & Hintergründe",
                "Lösungsansätze",
                "Praxisbeispiel/Case Study",
                "Zusammenfassung & CTA"
            ]
            
            for i in range(5):
                status.text(f"Generiere Post {i+1}/5...")
                
                prompt = f"""Erstelle LinkedIn Post {i+1} einer 5-teiligen Serie: {serie_theme}

FOKUS: {post_fokus[i]}
STIL: {serie_style}
LÄNGE: 200-300 Wörter

Zielgruppe: B2B Entscheider im deutschen Mittelstand
Schreibe konkret und praxisnah mit relevanten Hashtags."""

                try:
                    post_text = generate_with_openai(
                        prompt,
                        "Du bist LinkedIn Content-Experte für B2B im deutschen Mittelstand."
                    )
                    
                    generated_serie.append({
                        'nummer': i+1,
                        'text': post_text,
                        'fokus': post_fokus[i]
                    })
                    
                    progress_bar.progress((i+1)/5)
                    time.sleep(2)
                    
                except Exception as e:
                    st.error(f"❌ Fehler bei Post {i+1}: {str(e)}")
                    break
            
            if len(generated_serie) == 5:
                status.text("✅ Serie komplett!")
                st.session_state['generated_serie'] = generated_serie
                st.balloons()
                st.rerun()
    
    if 'generated_serie' in st.session_state:
        st.markdown("---")
        st.subheader("📚 Generierte Post-Serie")
        
        for post in st.session_state['generated_serie']:
            with st.expander(f"📄 Post {post['nummer']}/5: {post['fokus']}"):
                st.text_area(
                    "Post-Text",
                    value=post['text'],
                    height=250,
                    key=f"serie_post_{post['nummer']}",
                    disabled=True
                )
                
                col_a, col_b = st.columns(2)
                with col_a:
                    st.download_button(
                        "💾 Speichern",
                        data=post['text'],
                        file_name=f"serie_post{post['nummer']}.txt",
                        key=f"dl_{post['nummer']}",
                        use_container_width=True
                    )
                with col_b:
                    if st.button("📤 Posten", key=f"post_{post['nummer']}", use_container_width=True):
                        st.info("LinkedIn API in Entwicklung")
        
        if st.button("🗑️ Serie löschen", use_container_width=True):
            del st.session_state['generated_serie']
            st.rerun()

with tab3:
    st.subheader("📅 Content-Kalender")
    
    schedule = calendar.get('schedule', {})
    
    if schedule:
        st.metric("Posting-Frequenz", schedule.get('posting_frequency', 'N/A'))
        
        st.markdown("### 🕒 Optimale Posting-Zeiten")
        
        for time_slot in schedule.get('optimal_times', []):
            with st.expander(f"**{time_slot.get('day')}** um {time_slot.get('time')}"):
                st.write(f"**Grund:** {time_slot.get('reason')}")

with tab4:
    st.subheader("📊 Content-Themen Übersicht")
    
    if themes:
        for i, theme in enumerate(themes, 1):
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.markdown(f"**{i}. {theme.get('title')}**")
                st.caption(f"Kategorie: {theme.get('category')}")
            
            with col2:
                if st.button("Nutzen", key=f"theme_{i}"):
                    st.info("Feature in Entwicklung")
            
            st.markdown("---")
