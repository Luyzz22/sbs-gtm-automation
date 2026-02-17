import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, List
from datetime import datetime
import sqlite3
import os

class EmailService:
    def __init__(self):
        """Initialize mit Streamlit Secrets"""
        self.sender_email = st.secrets.get("SENDER_EMAIL", "")
        self.sender_name = st.secrets.get("SENDER_NAME", "Luis Orozco")
        self.smtp_server = st.secrets.get("SMTP_SERVER", "smtp.strato.de")
        self.smtp_port = int(st.secrets.get("SMTP_PORT", 465))
        self.smtp_username = st.secrets.get("SMTP_USERNAME", "")
        self.smtp_password = st.secrets.get("SMTP_PASSWORD", "")
        self.smtp_use_ssl = st.secrets.get("SMTP_USE_SSL", "True") == "True"
        
        self.db_path = "data/emails.db"
        self._init_db()
    
    def _init_db(self):
        """Erstelle Email-Historie Datenbank"""
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS emails (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                empfaenger TEXT NOT NULL,
                betreff TEXT NOT NULL,
                nachricht TEXT NOT NULL,
                template TEXT,
                status TEXT DEFAULT 'gesendet',
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def send_email(self, empfaenger: str, betreff: str, nachricht: str, 
                   template: str = None) -> Dict:
        """Sende Email via SMTP"""
        
        # Prüfe Credentials
        if not self.smtp_username or not self.smtp_password:
            self._save_to_db(empfaenger, betreff, nachricht, template, "simuliert")
            return {
                "success": True,
                "simulated": True,
                "message": "Email simuliert (SMTP nicht konfiguriert)"
            }
        
        try:
            # Erstelle Email
            msg = MIMEMultipart('alternative')
            msg['From'] = f"{self.sender_name} <{self.sender_email}>"
            msg['To'] = empfaenger
            msg['Subject'] = betreff
            msg['Reply-To'] = self.sender_email
            
            # Body
            text_part = MIMEText(nachricht, 'plain', 'utf-8')
            html_part = MIMEText(nachricht.replace('\n', '<br>'), 'html', 'utf-8')
            msg.attach(text_part)
            msg.attach(html_part)
            
            # Sende via SMTP
            if self.smtp_use_ssl:
                with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as server:
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
            else:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.smtp_username, self.smtp_password)
                    server.send_message(msg)
            
            # Speichere in DB
            self._save_to_db(empfaenger, betreff, nachricht, template, "gesendet")
            
            return {
                "success": True,
                "message": f"Email erfolgreich an {empfaenger} gesendet",
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            # Fehler in DB speichern
            self._save_to_db(empfaenger, betreff, nachricht, template, "fehler")
            
            return {
                "success": False,
                "error": str(e)
            }
    
    def _save_to_db(self, empfaenger: str, betreff: str, nachricht: str, 
                    template: str, status: str):
        """Speichere in DB"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            INSERT INTO emails (empfaenger, betreff, nachricht, template, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (empfaenger, betreff, nachricht, template, status))
        conn.commit()
        conn.close()
    
    def get_history(self, limit: int = 50) -> List[Dict]:
        """Hole Email-Historie"""
        if not os.path.exists(self.db_path):
            return []
            
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            SELECT empfaenger, betreff, template, status, timestamp
            FROM emails
            ORDER BY timestamp DESC
            LIMIT ?
        ''', (limit,))
        
        rows = c.fetchall()
        conn.close()
        
        return [
            {
                "empfaenger": row[0],
                "betreff": row[1],
                "template": row[2] or "Keins",
                "status": row[3],
                "timestamp": row[4]
            }
            for row in rows
        ]
    
    def get_stats(self) -> Dict:
        """Hole Statistiken"""
        if not os.path.exists(self.db_path):
            return {"heute": 0, "woche": 0, "gesamt": 0}
            
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM emails WHERE DATE(timestamp) = DATE('now')")
        heute = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM emails WHERE DATE(timestamp) >= DATE('now', '-7 days')")
        woche = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM emails")
        gesamt = c.fetchone()[0]
        
        conn.close()
        
        return {
            "heute": heute,
            "woche": woche,
            "gesamt": gesamt
        }
