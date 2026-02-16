# Scripts

Utility & Deployment Scripts für SBS GTM Automation.

## Verfügbare Scripts:

### Setup & Deployment
- `setup.sh` - Initial Project Setup
- `deploy.sh` - Production Deployment
- `rollback.sh` - Deployment Rollback

### Data Management
- `backup_leads.py` - Lead Database Backup
- `sync_to_bigquery.py` - Analytics Data Sync
- `clean_old_data.py` - DSGVO-konformes Data Cleanup

### LinkedIn Automation
- `post_content.py` - Manual Content Publishing
- `generate_leads.py` - One-time Lead Generation
- `test_linkedin_connection.py` - API Connection Test

### Maintenance
- `check_health.py` - System Health Check
- `update_dependencies.sh` - Dependency Updates
- `rotate_credentials.py` - API Key Rotation

## Usage:

```bash
# Setup
./scripts/setup.sh

# Deployment
./scripts/deploy.sh production

# Lead Generation
python scripts/generate_leads.py --count=50
```

## Best Practices:
- Alle Scripts haben `--dry-run` Option
- Logging in `logs/scripts/`
- Error Handling & Rollback
- DSGVO-konforme Datenverarbeitung
