import sqlite3
import os
from typing import List, Dict
from datetime import datetime

class LeadService:
    def __init__(self):
        self.db_path = "data/leads.db"
        self._init_db()
    
    def _init_db(self):
        """Erstelle Leads DB"""
        os.makedirs("data", exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS leads (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                unternehmen TEXT NOT NULL,
                kontakt TEXT NOT NULL,
                position TEXT,
                email TEXT,
                telefon TEXT,
                branche TEXT,
                score INTEGER DEFAULT 0,
                status TEXT DEFAULT 'kalt',
                notizen TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
    
    def add_lead(self, unternehmen: str, kontakt: str, position: str = "", 
                 email: str = "", branche: str = "", score: int = 0) -> Dict:
        """Füge Lead hinzu"""
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        # Status basierend auf Score
        if score >= 80:
            status = "heiss"
        elif score >= 60:
            status = "warm"
        else:
            status = "kalt"
        
        c.execute('''
            INSERT INTO leads (unternehmen, kontakt, position, email, branche, score, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (unternehmen, kontakt, position, email, branche, score, status))
        
        conn.commit()
        conn.close()
        
        return {"success": True, "message": f"Lead {unternehmen} hinzugefügt"}
    
    def get_leads(self, status_filter: List[str] = None, limit: int = 100) -> List[Dict]:
        """Hole Leads"""
        if not os.path.exists(self.db_path):
            return []
            
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        if status_filter:
            # Konvertiere Emoji-Status zurück
            status_map = {"🟢 Heiß": "heiss", "🟡 Warm": "warm", "🔵 Kalt": "kalt"}
            status_db = [status_map.get(s, s.lower()) for s in status_filter]
            
            placeholders = ','.join('?' * len(status_db))
            query = f'''
                SELECT unternehmen, kontakt, position, email, score, status, timestamp
                FROM leads
                WHERE status IN ({placeholders})
                ORDER BY score DESC, timestamp DESC
                LIMIT ?
            '''
            c.execute(query, (*status_db, limit))
        else:
            c.execute('''
                SELECT unternehmen, kontakt, position, email, score, status, timestamp
                FROM leads
                ORDER BY score DESC, timestamp DESC
                LIMIT ?
            ''', (limit,))
        
        rows = c.fetchall()
        conn.close()
        
        # Emoji-Mapping
        status_emoji = {
            "heiss": "🟢 Heiß",
            "warm": "🟡 Warm",
            "kalt": "🔵 Kalt"
        }
        
        return [
            {
                "unternehmen": row[0],
                "kontakt": row[1],
                "position": row[2],
                "email": row[3],
                "score": row[4],
                "status": status_emoji.get(row[5], row[5]),
                "timestamp": row[6]
            }
            for row in rows
        ]
    
    def get_stats(self) -> Dict:
        """Hole Lead-Statistiken"""
        if not os.path.exists(self.db_path):
            return {"heiss": 0, "warm": 0, "kalt": 0, "gesamt": 0}
            
        conn = sqlite3.connect(self.db_path)
        c = conn.cursor()
        
        c.execute("SELECT COUNT(*) FROM leads WHERE status = 'heiss'")
        heiss = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM leads WHERE status = 'warm'")
        warm = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM leads WHERE status = 'kalt'")
        kalt = c.fetchone()[0]
        
        c.execute("SELECT COUNT(*) FROM leads")
        gesamt = c.fetchone()[0]
        
        conn.close()
        
        return {
            "heiss": heiss,
            "warm": warm,
            "kalt": kalt,
            "gesamt": gesamt
        }
