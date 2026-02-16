import streamlit as st
from datetime import datetime
import sqlite3
import os
from typing import Dict, List

class LinkedInService:
    def __init__(self):
        """Initialize LinkedIn Service"""
        self.openai_api_key = st.secrets.get("OPENAI_API_KEY", "")
        self.sender_name = st.secrets.get("SENDER_NAME", "Luis Schenk")
        self.company = st.secrets.get("COMPANY_NAME", "SBS Deutschland GmbH")
        
        self.db_path = "data/linkedin.db"
        self._init_db()
    
    def _init_db(self):
        """Erstelle Posts DB"""
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                thema TEXT NOT NULL,
                inhalt TEXT NOT NULL,
                hashtags TEXT,
                cta TEXT,
                status TEXT DEFAULT 'entwurf',
                likes INTEGER DEFAULT 0,
                kommentare INTEGER DEFAULT 0,
                shares INTEGER DEFAULT 0,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def generate_post(self, thema: str, ton: str = "professional") -> Dict:
        """Generiere LinkedIn Post mit OpenAI"""
        
        if not self.openai_api_key:
            # Fallback ohne AI
            return {
                "content": f"🚀 {thema}\n\nSpannende Entwicklungen in diesem Bereich! Mehr dazu in Kürze.\n\n{self.sender_name}\n{self.company}",
                "hashtags": ["#Innovation", "#Technology", "#Business"],
                "call_to_action": "Was ist Ihre Meinung dazu? Kommentieren Sie!"
            }
        
        try:
            # OpenAI API Call würde hier rein
            # Für jetzt: Strukturierter Platzhalter
            return {
                "content": f"""🚀 {thema}

Wir bei {self.company} arbeiten kontinuierlich an innovativen Lösungen.

{thema} ist ein wichtiger Aspekt unserer Strategie für 2026.

{self.sender_name}
{self.company}""",
                "hashtags": ["#Innovation", "#B2B", "#Technology", "#Leadership"],
                "call_to_action": "Was sind Ihre Erfahrungen? Lassen Sie uns diskutieren!"
            }
        
        except Exception as e:
            return {
                "content": f"Error: {str(e)}",
                "hashtags": [],
                "call_to_action": ""
            }
    
    def save_post(self, thema: str, inhalt: str, hashtags: str = "", 
                  cta: str = "", status: str = "entwurf") -> Dict:
        """Speichere Post in DB"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO posts (thema, inhalt, hashtags, cta, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (thema, inhalt, hashtags, cta, status))
        conn.commit()
        conn.close()
        
        return {
            "success": True,
            "message": f"Post '{thema}' gespeichert"
        }
    
    def get_posts(self, limit: int = 20) -> List[Dict]:
        """Hole Posts"""
        if not os.path.exists(self.db_path):
            return []
            
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT thema, inhalt, hashtags, status, likes, kommentare, shares, timestamp
            FROM posts
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = c.fetchall()
        conn.close()
        
        return [
            {
                "thema": row[0],
                "inhalt": row[1][:100] + "..." if len(row[1]) > 100 else row[1],
                "hashtags": row[2],
                "status": row[3],
                "likes": row[4],
                "kommentare": row[5],
                "shares": row[6],
                "timestamp": row[7]
            }
            for row in rows
        ]
    
    def get_stats(self) -> Dict:
        """Hole Statistiken"""
        if not os.path.exists(self.db_path):
            return {"posts_monat": 0, "total_engagement": 0}
            
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM posts WHERE DATE(timestamp) >= DATE('now', '-30 days')")
        posts_monat = c.fetchone()[0]
        
        c.execute("SELECT SUM(likes + kommentare + shares) FROM posts")
        engagement = c.fetchone()[0] or 0
        
        conn.close()
        
        return {
            "posts_monat": posts_monat,
            "total_engagement": engagement
        }
