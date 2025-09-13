powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

#가상환경활성화
.venv\Scripts\Activate
streamlit run email_agent.py
