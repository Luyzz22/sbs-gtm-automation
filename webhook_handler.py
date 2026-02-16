#!/usr/bin/env python3
"""
Resend Webhook Handler
Empfängt Email-Events (delivered, opened, clicked, bounced)
"""
from flask import Flask, request, jsonify
import pandas as pd
from datetime import datetime
import os

app = Flask(__name__)

# Event-Log Datei
EVENT_LOG = 'email_events.csv'

@app.route('/webhook/resend', methods=['POST'])
def handle_resend_webhook():
    """Empfängt Resend Webhook Events"""
    
    data = request.json
    event_type = data.get('type')
    email_data = data.get('data', {})
    
    print(f"📨 Event empfangen: {event_type}")
    
    # Event loggen
    event_record = {
        'timestamp': datetime.now().isoformat(),
        'event_type': event_type,
        'email_id': email_data.get('email_id'),
        'to': email_data.get('to'),
        'subject': email_data.get('subject'),
        'status': email_data.get('status')
    }
    
    # In CSV speichern
    df = pd.DataFrame([event_record])
    
    if os.path.exists(EVENT_LOG):
        df.to_csv(EVENT_LOG, mode='a', header=False, index=False)
    else:
        df.to_csv(EVENT_LOG, index=False)
    
    print(f"✓ Event geloggt: {event_type} für {email_data.get('to')}")
    
    return jsonify({'status': 'success'}), 200

@app.route('/events/summary', methods=['GET'])
def get_events_summary():
    """Zeigt Event-Zusammenfassung"""
    
    if not os.path.exists(EVENT_LOG):
        return jsonify({'error': 'Keine Events vorhanden'}), 404
    
    df = pd.read_csv(EVENT_LOG)
    
    summary = {
        'total_events': len(df),
        'by_type': df['event_type'].value_counts().to_dict(),
        'last_event': df.iloc[-1].to_dict() if len(df) > 0 else None
    }
    
    return jsonify(summary), 200

if __name__ == '__main__':
    print("🌐 Webhook Handler gestartet auf http://localhost:5000")
    print("📍 Webhook URL: http://localhost:5000/webhook/resend")
    app.run(host='0.0.0.0', port=5000, debug=True)
