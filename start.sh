#!/bin/bash

echo "🚀 Starting SBS GTM Automation Hub..."

# Pfad zum Projekt
cd ~/Desktop/sbs-gtm-automation

# Virtual Environment aktivieren
source venv/bin/activate

# Backend-Scheduler im Hintergrund starten
echo "Starting automation backend..."
python automation_scheduler.py &
BACKEND_PID=$!

# Frontend starten
echo "Starting web frontend..."
streamlit run frontend/main_app.py --server.port 8501 &
FRONTEND_PID=$!

echo ""
echo "✅ System gestartet!"
echo ""
echo "📊 Frontend: http://localhost:8501"
echo "🤖 Backend PID: $BACKEND_PID"
echo "🎨 Frontend PID: $FRONTEND_PID"
echo ""
echo "Zum Stoppen: ./stop.sh"

# PIDs speichern
echo $BACKEND_PID > .backend.pid
echo $FRONTEND_PID > .frontend.pid
