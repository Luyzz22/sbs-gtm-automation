#!/usr/bin/env python3
"""
Performance Monitoring & Alert System
Überwacht Kampagnen-Performance und sendet Alerts
"""
import pandas as pd
from datetime import datetime, timedelta
import resend
import os
from dotenv import load_dotenv

load_dotenv()
resend.api_key = os.getenv('RESEND_API_KEY')

def check_campaign_health():
    """Prüft Kampagnen-Gesundheit"""
    try:
        df = pd.read_csv('campaign_results.csv')
        df['timestamp'] = pd.to_datetime(df['timestamp'])
    except FileNotFoundError:
        return None
    
    total = len(df)
    sent = len(df[df['status'] == 'sent'])
    failed = len(df[df['status'] == 'failed'])
    success_rate = (sent/total*100) if total > 0 else 0
    
    # Letzte 24h
    last_24h = df[df['timestamp'] > datetime.now() - timedelta(hours=24)]
    
    health = {
        'total': total,
        'sent': sent,
        'failed': failed,
        'success_rate': success_rate,
        'last_24h': len(last_24h),
        'status': 'healthy' if success_rate >= 95 else 'warning' if success_rate >= 80 else 'critical'
    }
    
    return health

def send_alert(health):
    """Sendet Alert-Email bei Problemen"""
    if health['status'] == 'critical':
        subject = "🚨 CRITICAL: SBS GTM Kampagnen-Performance"
        message = f"""
        <h2>🚨 Kritische Kampagnen-Performance</h2>
        <p><strong>Erfolgsrate:</strong> {health['success_rate']:.1f}%</p>
        <p><strong>Fehlgeschlagen:</strong> {health['failed']}/{health['total']}</p>
        <p><strong>Letzte 24h:</strong> {health['last_24h']} Emails</p>
        <p>Bitte prüfen Sie die Kampagnen-Konfiguration.</p>
        """
    elif health['status'] == 'warning':
        subject = "⚠️ WARNING: SBS GTM Performance unter 95%"
        message = f"""
        <h2>⚠️ Kampagnen-Performance-Warnung</h2>
        <p><strong>Erfolgsrate:</strong> {health['success_rate']:.1f}%</p>
        <p><strong>Gesamt versendet:</strong> {health['sent']}/{health['total']}</p>
        """
    else:
        return  # Kein Alert bei healthy
    
    params = {
        "from": "SBS Monitoring <ki@sbsdeutschland.de>",
        "to": ["ki@sbsdeutschland.de"],
        "subject": subject,
        "html": message
    }
    
    try:
        resend.Emails.send(params)
        print(f"✓ Alert gesendet: {health['status']}")
    except Exception as e:
        print(f"✗ Alert-Fehler: {str(e)}")

def generate_daily_report():
    """Generiert täglichen Performance-Report"""
    health = check_campaign_health()
    
    if not health:
        print("Keine Daten verfügbar")
        return
    
    print("\n" + "="*60)
    print("📊 DAILY PERFORMANCE REPORT")
    print("="*60)
    print(f"Datum: {datetime.now().strftime('%d.%m.%Y %H:%M')}")
    print(f"Status: {health['status'].upper()}")
    print(f"Erfolgsrate: {health['success_rate']:.1f}%")
    print(f"Versendet: {health['sent']}/{health['total']}")
    print(f"Fehlgeschlagen: {health['failed']}")
    print(f"Letzte 24h: {health['last_24h']} Emails")
    print("="*60)
    
    # Alert senden falls nötig
    send_alert(health)

if __name__ == "__main__":
    generate_daily_report()
