from streamlit.web import cli as stcli
import sys

def application(environ, start_response):
    sys.argv = ["streamlit", "run", "frontend/main_app.py", "--server.port=8501"]
    stcli.main()
