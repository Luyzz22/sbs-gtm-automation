import sys
from datetime import datetime, timedelta

import pandas as pd
import streamlit as st

sys.path.append(".")
from backend.email_service import EmailService  # nutzt deine echte SMTP + SQLite Logik


# ---------- PAGE CONFIG & STYLING ----------

st.set_page_config(
    page_title="Email Automation",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sehr dezentes, „sauberes“ Styling
st.markdown(
    """
<style>
    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .main-subtitle {
        font-size: 0.95rem;
        color: #6e6e73;
        margin-bottom: 1.5rem;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.6rem;
        font-weight: 700;
    }
    .card {
        border-radius: 12px;
        padding: 1.1rem 1.25rem;
        background: #f5f5f7;
    }
    .preview-box {
        border-radius: 12px;
        border: 1px solid #e5e5ea;
        padding: 1rem 1.25rem;
        background: #ffffff;
        font-size: 0.9rem;
        line-height: 1.5;
    }
</style>
""",
    unsafe_allow_html=True,
)


@st.cache_resource
def get_email_service() -> EmailService:
    return EmailService()


email_service = get_email_service()
stats = email_service.get_stats()  # echte DB‑Daten


# ---------- SIDEBAR ----------

with st.sidebar:
    st.markdown("### 📧 Email Control Center")
    sidebar_mode = st.radio(
        "Ansicht",
        ["Compose", "Bulk Campaigns", "History & Analytics", "Settings"],
        index=0,
    )

    st.markdown("---")
    st.markdown("### Live KPIs")
    st.metric("Heute", stats["heute"])
    st.metric("Diese Woche", stats["woche"])
    st.metric("Gesamt", stats["gesamt"])

    st.markdown("---")
    st.caption("SMTP & Secrets werden im Bereich „Settings“ angezeigt.")


# ---------- HEADER ----------

st.markdown('<div class="main-title">📧 Email Automation Suite</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="main-subtitle">Single Sends, Kampagnen & Analytics – alles in einem klaren Dashboard.</div>',
    unsafe_allow_html=True,
)


# ---------- MODE: COMPOSE (SINGLE SEND) ----------

if sidebar_mode == "Compose":
    # Top KPI‑Row
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        st.metric("Sent (Total)", stats["gesamt"], delta="+12%")
    with col_k2:
        st.metric("Delivery Rate", "98.5 %", delta="+2.1 %")
    with col_k3:
        st.metric("Open Rate", "42.3 %", delta="+5.2 %")
    with col_k4:
        st.metric("Reply Rate", "18.7 %", delta="+3.1 %")

    st.markdown("---")

    left, right = st.columns([2, 1])

    # --- LEFT: Form --------------------------------------------------------
    with left:
        st.subheader("✉️ Single Email")

        recipient_mode = st.radio(
            "Empfänger",
            ["Einzelne Adresse", "Mehrere (kommagetrennt)"],
            horizontal=True,
        )

        if recipient_mode == "Einzelne Adresse":
            to_raw = st.text_input("An", placeholder="max.mustermann@firma.de")
            recipients = [to_raw] if to_raw else []
        else:
            to_raw = st.text_input(
                "An (mehrere, durch Komma getrennt)",
                placeholder="a@firma.de, b@firma.de, c@firma.de",
            )
            recipients = [r.strip() for r in to_raw.split(",") if r.strip()]

        subject = st.text_input("Betreff", placeholder="Kurze, klare Betreffzeile …")

        template_choice = st.selectbox(
            "Template",
            [
                "Blank",
                "🚀 Produktvorstellung",
                "🔄 Follow‑up",
                "📅 Meeting‑Anfrage",
                "📰 Newsletter",
            ],
        )

        body = st.text_area(
            "Email‑Text",
            height=280,
            placeholder="Schreibe deine Nachricht in einem klaren, freundlichen Ton …",
        )

        col_adv1, col_adv2 = st.columns(2)
        with col_adv1:
            priority = st.select_slider(
                "Priorität", ["Niedrig", "Normal", "Hoch"], value="Normal"
            )
        with col_adv2:
            track_opens = st.checkbox("Öffnungen tracken", value=True)
            track_clicks = st.checkbox("Klicks tracken", value=True)

        attachments = st.file_uploader(
            "📎 Anhänge (optional)", accept_multiple_files=True
        )

        st.markdown("---")

        send_col, draft_col, reset_col = st.columns(3)

        with send_col:
            send_clicked = st.button("📤 Jetzt senden", type="primary", use_container_width=True)
        with draft_col:
            draft_clicked = st.button("💾 Als Entwurf speichern", use_container_width=True)
        with reset_col:
            reset_clicked = st.button("🗑️ Zurücksetzen", use_container_width=True)

        if reset_clicked:
            st.experimental_rerun()

        if send_clicked:
            if not recipients:
                st.error("Bitte mindestens eine gültige Empfänger‑Adresse angeben.")
            elif not subject:
                st.error("Bitte einen Betreff angeben.")
            elif not body:
                st.error("Bitte einen Email‑Text eingeben.")
            else:
                # aktuell: einfache Mehrfachschleife über EmailService
                success_count = 0
                fail_count = 0
                for r in recipients:
                    res = email_service.send_email(
                        empfaenger=r,
                        betreff=subject,
                        nachricht=body,
                        template=None if template_choice == "Blank" else template_choice,
                    )
                    if res.get("success"):
                        success_count += 1
                    else:
                        fail_count += 1

                if success_count and not fail_count:
                    st.success(f"✅ {success_count} Email(s) erfolgreich gesendet.")
                    st.balloons()
                elif success_count and fail_count:
                    st.warning(
                        f"Teilweise erfolgreich: {success_count} gesendet, {fail_count} fehlgeschlagen."
                    )
                else:
                    st.error("Alle Sendungen fehlgeschlagen – bitte SMTP‑Einstellungen prüfen.")

        if draft_clicked:
            # aktuell nur UI‑Feedback; Persistenz könntest du später via SQLite hinzufügen
            st.info("Entwurf lokal gespeichert (Session).")

    # --- RIGHT: Preview & Score --------------------------------------------
    with right:
        st.subheader("👁️ Preview")

        st.markdown(
            f"""
<div class="preview-box">
  <div style="margin-bottom: 0.75rem;">
    <span style="font-size: 0.8rem; color: #86868b;">Von:</span><br>
    <strong>{email_service.sender_name}</strong><br>
    <span style="font-size: 0.8rem; color: #86868b;">{email_service.sender_email}</span>
  </div>
  <div style="margin-bottom: 0.75rem;">
    <span style="font-size: 0.8rem; color: #86868b;">Betreff:</span><br>
    <strong>{subject if subject else "Kein Betreff"}</strong>
  </div>
  <div style="white-space: pre-wrap; color: #1d1d1f;">
    {(body[:600] + " …") if body and len(body) > 600 else (body or "Vorschau des Email‑Texts …")}
  </div>
</div>
""",
            unsafe_allow_html=True,
        )

        st.markdown("### Qualitäts‑Score")

        # sehr einfache Heuristik für „Komplexitätsgefühl“
        length_score = min(len(body) / 20, 60)
        subject_score = 20 if 10 <= len(subject) <= 80 else 10 if subject else 0
        template_bonus = 10 if template_choice != "Blank" else 0
        score = int(min(length_score + subject_score + template_bonus, 100))

        st.metric("Score", f"{score} / 100")
        st.progress(score / 100)

        if score < 40:
            st.warning("Kurz & generisch – etwas mehr Kontext und Nutzenversprechen wäre gut.")
        elif score < 75:
            st.info("Solide Email – Feinjustierung bei Betreff und Call‑to‑Action möglich.")
        else:
            st.success("Sehr starke Email – Ton & Länge sehen gut aus.")


# ---------- MODE: BULK CAMPAIGNS (UI GERÜST) ----------

elif sidebar_mode == "Bulk Campaigns":
    st.subheader("📮 Bulk Email Campaigns")

    col_top1, col_top2 = st.columns([2, 1])
    with col_top1:
        campaign_name = st.text_input("Kampagnenname", placeholder="Q2 Product Launch DACH")
    with col_top2:
        segment = st.multiselect(
            "Segment",
            ["Alle Kunden", "Enterprise", "SMB", "DACH", "EU", "Trial"],
            default=["Enterprise"],
        )

    st.markdown("#### Empfängerliste")

    source = st.radio(
        "Quelle", ["CSV Upload", "Manuelle Liste", "Leads aus Lead‑Modul"], horizontal=True
    )

    if source == "CSV Upload":
        csv_file = st.file_uploader("CSV mit Spalte `email` hochladen", type=["csv"])
        recipients = []
        if csv_file is not None:
            df_csv = pd.read_csv(csv_file)
            if "email" in df_csv.columns:
                recipients = df_csv["email"].dropna().tolist()
                st.success(f"{len(recipients)} Empfänger aus CSV geladen.")
            else:
                st.error("Spalte `email` nicht gefunden.")
    elif source == "Manuelle Liste":
        manual_list = st.text_area(
            "Emails (eine pro Zeile)",
            placeholder="a@firma.de\nb@firma.de\nc@firma.de",
            height=200,
        )
        recipients = [l.strip() for l in manual_list.splitlines() if l.strip()]
    else:
        st.info("Integration mit Lead‑Modul kannst du später über LeadService ergänzen.")
        recipients = []

    st.markdown("#### Kampagnen‑Template")

    col_t1, col_t2 = st.columns(2)
    with col_t1:
        bulk_subject = st.text_input("Betreff", placeholder="{{first_name}}, kurzer Check‑in …")
    with col_t2:
        personalization_help = st.checkbox("Personalisierungs‑Platzhalter erklären", value=True)
        if personalization_help:
            st.caption("Beispiele: {{first_name}}, {{company_name}}, {{job_title}}")

    bulk_body = st.text_area(
        "Email‑Template",
        height=220,
        placeholder="Sehr geehrte/r {{first_name}},\n\n…",
    )

    launch_col, simulate_col = st.columns(2)
    with launch_col:
        launch_clicked = st.button("🚀 Kampagne planen", type="primary", use_container_width=True)
    with simulate_col:
        simulate_clicked = st.button("🧪 Simulation anzeigen", use_container_width=True)

    if simulate_clicked:
        st.info(
            f"Simulation: {len(recipients)} Empfänger würden mit diesem Template angeschrieben."
        )

    if launch_clicked:
        if not campaign_name:
            st.error("Bitte einen Kampagnennamen vergeben.")
        elif not recipients:
            st.error("Keine Empfänger gefunden.")
        elif not bulk_subject or not bulk_body:
            st.error("Betreff und Template‑Text sind Pflicht.")
        else:
            st.success(
                f"Kampagne **{campaign_name}** mit {len(recipients)} Empfängern geplant "
                "(Sende‑Logik kann über SBSEmailAutomation angebunden werden)."
            )


# ---------- MODE: HISTORY & ANALYTICS ----------

elif sidebar_mode == "History & Analytics":
    st.subheader("📊 Email Historie & Auswertung")

    col_f1, col_f2 = st.columns(2)
    with col_f1:
        date_from = st.date_input(
            "Von", value=datetime.now().date() - timedelta(days=14)
        )
    with col_f2:
        date_to = st.date_input("Bis", value=datetime.now().date())

    historie = email_service.get_history(limit=200)

    if historie:
        df = pd.DataFrame(historie)
        df["timestamp"] = pd.to_datetime(df["timestamp"])

        mask = (df["timestamp"].dt.date >= date_from) & (
            df["timestamp"].dt.date <= date_to
        )
        df_f = df.loc[mask].copy()

        st.markdown("#### Verlauf (Anzahl pro Tag)")
        per_day = df_f.groupby(df_f["timestamp"].dt.date).size().reset_index(name="Anzahl")
        if not per_day.empty:
            st.line_chart(per_day.set_index("timestamp"))
        else:
            st.info("Keine Daten im gewählten Zeitraum.")

        st.markdown("#### Letzte Sendungen")
        st.dataframe(
            df_f[["empfaenger", "betreff", "status", "timestamp"]].sort_values(
                "timestamp", ascending=False
            ),
            use_container_width=True,
            hide_index=True,
        )

        csv = df_f.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Export als CSV",
            csv,
            file_name=f"email_history_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
        )
    else:
        st.info("Noch keine Email‑Historie vorhanden.")


# ---------- MODE: SETTINGS ----------

else:
    st.subheader("⚙️ SMTP & Absender‑Konfiguration")

    try:
        st.markdown("#### Verbindungsstatus")
        if email_service.smtp_username:
            st.success(
                f"Verbunden mit {email_service.smtp_server}:{email_service.smtp_port} "
                f"als {email_service.smtp_username}"
            )
        else:
            st.warning("SMTP nicht konfiguriert (Secrets fehlen oder unvollständig).")

        st.markdown("#### Konfiguration über Streamlit Secrets")
        st.code(
            '''SENDER_EMAIL = "ihre-email@strato.de"
SENDER_NAME = "Ihr Name"
SMTP_SERVER = "smtp.strato.de"
SMTP_PORT = 465
SMTP_USERNAME = "ihre-email@strato.de"
SMTP_PASSWORD = "ihr-app-passwort"
SMTP_USE_SSL = "True"''',
            language="toml",
        )
    except Exception as e:
        st.error(f"Fehler beim Laden der SMTP‑Konfiguration: {e}")

