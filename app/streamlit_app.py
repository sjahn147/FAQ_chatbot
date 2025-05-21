import streamlit as st
import requests
import json
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="FAQ 챗봇",
    page_icon="💬",
    layout="wide"
)

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = []
if "context_id" not in st.session_state:
    st.session_state.context_id = None

# API 엔드포인트 설정
API_URL = "http://localhost:8001/api/chat"

# 스타일 설정
st.markdown("""
<style>
    .stTextInput>div>div>input {
        font-size: 16px;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
    }
    .chat-message.user {
        background-color: #2b313e;
    }
    .chat-message.assistant {
        background-color: #475063;
    }
    .chat-message .content {
        display: flex;
        flex-direction: row;
        align-items: flex-start;
    }
    .chat-message .avatar {
        width: 40px;
        height: 40px;
        border-radius: 50%;
        margin-right: 1rem;
    }
    .chat-message .message {
        flex: 1;
    }
</style>
""", unsafe_allow_html=True)

# 헤더
st.title("💬 FAQ 챗봇")
st.markdown("---")

# 사이드바
with st.sidebar:
    st.header("ℹ️ 안내")
    st.markdown("""
    ### 사용 방법
    1. 질문을 입력하세요
    2. Enter를 누르거나 전송 버튼을 클릭하세요
    3. 챗봇이 답변을 제공합니다
    
    ### 주의사항
    - 대화는 30분 후 자동으로 만료됩니다
    - 새로운 대화를 시작하려면 페이지를 새로고침하세요
    """)
    
    if st.button("대화 초기화"):
        st.session_state.messages = []
        st.session_state.context_id = None
        st.rerun()

# 채팅 인터페이스
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 사용자 입력
if prompt := st.chat_input("질문을 입력하세요..."):
    # 사용자 메시지 추가
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # API 호출
    try:
        response = requests.post(
            API_URL,
            json={
                "message": prompt,
                "context_id": st.session_state.context_id
            }
        )
        response.raise_for_status()
        data = response.json()
        
        # 컨텍스트 ID 저장
        st.session_state.context_id = data["context_id"]
        
        # 챗봇 응답 추가
        st.session_state.messages.append({"role": "assistant", "content": data["response"]})
        with st.chat_message("assistant"):
            st.markdown(data["response"])
            
    except Exception as e:
        st.error(f"오류가 발생했습니다: {str(e)}")
        st.session_state.messages.append({"role": "assistant", "content": "죄송합니다. 오류가 발생했습니다. 다시 시도해주세요."})
        with st.chat_message("assistant"):
            st.markdown("죄송합니다. 오류가 발생했습니다. 다시 시도해주세요.") 