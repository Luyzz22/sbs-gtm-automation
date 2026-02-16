#!/bin/bash

# Pfade
PROJECT_DIR="$HOME/Desktop/sbs-gtm-automation"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python"

echo "Setting up Cron Jobs für SBS GTM Automation..."

# Aktuelle Crontab sichern
crontab -l > crontab_backup.txt 2>/dev/null || echo "# SBS GTM Automation Cron Jobs" > crontab_backup.txt

# Neue Cron Jobs hinzufügen
cat >> crontab_backup.txt << CRONEOF

# SBS GTM Automation - Daily Follow-up Check (9:00 AM)
0 9 * * * cd $PROJECT_DIR && $VENV_PYTHON follow_up_automation.py >> logs/follow_up.log 2>&1

# SBS GTM Automation - Weekly Campaign Report (Freitag 17:00)
0 17 * * 5 cd $PROJECT_DIR && $VENV_PYTHON -c "import pandas as pd; df=pd.read_csv('campaign_results.csv'); print(df.describe())" | mail -s "Weekly Report" ki@sbsdeutschland.de

# SBS GTM Automation - Backup Results (täglich 23:00)
0 23 * * * cd $PROJECT_DIR && cp campaign_results.csv backups/campaign_results_\$(date +\%Y\%m\%d).csv

CRONEOF

# Crontab installieren
crontab crontab_backup.txt

echo "✓ Cron Jobs installiert!"
echo ""
echo "Aktive Cron Jobs:"
crontab -l | grep "SBS GTM"

# Log-Verzeichnis erstellen
mkdir -p $PROJECT_DIR/logs
mkdir -p $PROJECT_DIR/backups

echo ""
echo "✓ Log-Verzeichnisse erstellt:"
echo "  - $PROJECT_DIR/logs"
echo "  - $PROJECT_DIR/backups"
