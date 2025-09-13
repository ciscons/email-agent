import os
import uuid
import requests
import streamlit as st
from dotenv import load_dotenv

# .env 로드
load_dotenv()
agent_api_key = os.getenv("AGENT_API_KEY")
agent_api_url = os.getenv("AGENT_URL")

st.title('이메일 에이전트')

# 세션 초기화
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

# 기존 메시지 출력
for msg in st.session_state.messages:
    with st.chat_message(msg['role']):
        st.write(msg['content'])

# 사용자 입력
prompt = st.chat_input('이메일 내용을 입력해주세요')

if prompt:
    st.chat_message('user').write(prompt)
    st.session_state.messages.append({'role': 'user', 'content': prompt})

    # API 요청
    response = requests.post(
        agent_api_url, 
        headers={'Authorization': agent_api_key}, 
        json={
            'message': prompt, 
            'session_id': st.session_state.session_id
        }
    )

    # 응답 처리
    try:
        data = response.json()
    except ValueError:  # JSONDecodeError 발생 시
        data = {"output": response.text}

    output = data.get("output") or data.get("content") or str(data)
    st.session_state.messages.append({'role': 'assistant', 'content': output})

    with st.chat_message('assistant'):
        st.write(output)
