#!/bin/bash

# SBS GTM Automation Launcher
# Zentrales Startskript für alle Features

PROJECT_DIR="$HOME/Desktop/sbs-gtm-automation"
cd $PROJECT_DIR

# Virtual Environment aktivieren
source venv/bin/activate

# ASCII Art Banner
cat << 'BANNER'
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║   ███████╗██████╗ ███████╗     ██████╗ ████████╗███╗   ███║
║   ██╔════╝██╔══██╗██╔════╝    ██╔════╝ ╚══██╔══╝████╗ ████║
║   ███████╗██████╔╝███████╗    ██║  ███╗   ██║   ██╔████╔██║
║   ╚════██║██╔══██╗╚════██║    ██║   ██║   ██║   ██║╚██╔╝██║
║   ███████║██████╔╝███████║    ╚██████╔╝   ██║   ██║ ╚═╝ ██║
║   ╚══════╝╚═════╝ ╚══════╝     ╚═════╝    ╚═╝   ╚═╝     ╚═╝
║                                                           ║
║           Email Automation & Campaign Management          ║
║                   Luis Schenk - 2026                      ║
╚═══════════════════════════════════════════════════════════╝
BANNER

echo ""
echo "Wählen Sie eine Option:"
echo ""
echo "  1) 📧  Neue Kampagne starten"
echo "  2) 🔄  Follow-ups prüfen & versenden"
echo "  3) 📊  Analytics Dashboard öffnen"
echo "  4) 🧪  A/B Testing Kampagne"
echo "  5) 📈  Performance Monitoring"
echo "  6) 🌐  Webhook Handler starten"
echo "  7) 📋  Ergebnisse anzeigen"
echo "  8) 🔗  Resend Dashboard öffnen"
echo "  9) 🛠️  Alle Features ausführen"
echo "  0) ❌  Beenden"
echo ""
read -p "Option wählen [0-9]: " option

case $option in
    1)
        echo "Starting neue Kampagne..."
        python automated_email_sender.py
        ;;
    2)
        echo "Checking Follow-ups..."
        python follow_up_automation.py
        ;;
    3)
        echo "Opening Analytics Dashboard..."
        streamlit run dashboard.py
        ;;
    4)
        echo "Starting A/B Testing..."
        python ab_testing.py
        ;;
    5)
        echo "Running Performance Monitoring..."
        python monitoring.py
        ;;
    6)
        echo "Starting Webhook Handler..."
        python webhook_handler.py
        ;;
    7)
        echo "Campaign Results:"
        cat campaign_results.csv | column -t -s,
        ;;
    8)
        echo "Opening Resend Dashboard..."
        open https://resend.com/emails
        ;;
    9)
        echo "Running all features..."
        python monitoring.py
        python follow_up_automation.py
        streamlit run dashboard.py &
        ;;
    0)
        echo "Auf Wiedersehen!"
        exit 0
        ;;
    *)
        echo "Ungültige Option"
        exit 1
        ;;
esac
