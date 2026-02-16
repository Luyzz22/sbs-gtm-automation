import os

pages = {
    '1_📧_Email_Automation.py': '''import streamlit as st
import pandas as pd
import sys
sys.path.append('.')
from backend.email_service import EmailService

st.set_page_config(page_title="Email Automation", page_icon="📧", layout="wide")

@st.cache_resource
def get_email_service():
    return EmailService()

email_service = get_email_service()
stats = email_service.get_stats()

st.title("📧 Email Automation")
st.metric("Emails gesamt", stats["gesamt"])

empfaenger = st.text_input("An")
betreff = st.text_input("Betreff")
text = st.text_area("Text", height=200)

if st.button("Senden"):
    if empfaenger and betreff and text:
        result = email_service.send_email(empfaenger, betreff, text)
        if result["success"]:
            st.success("Email gesendet!")
        else:
            st.error(result.get("error", "Fehler"))
''',

    '3_🎯_Lead_Generation.py': '''import streamlit as st
import sys
sys.path.append('.')
from backend.lead_service import LeadService

st.title("🎯 Leads")
lead_service = LeadService()
stats = lead_service.get_stats()

st.metric("Gesamt", stats["gesamt"])

unternehmen = st.text_input("Unternehmen")
kontakt = st.text_input("Kontakt")

if st.button("Hinzufügen"):
    if unternehmen and kontakt:
        lead_service.add_lead(unternehmen, kontakt, "", "", "", 50)
        st.success("Lead hinzugefügt!")
'''
}

for filename, content in pages.items():
    with open(f'pages/{filename}', 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"✅ {filename}")

print("\nFertig!")
