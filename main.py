import streamlit as st
import sqlite3
import uuid
from datetime import datetime
from langchain.callbacks.base import BaseCallbackHandler
from scripts.load_rag_chain import get_rag_chain  # يجب أن يكون لديك هذا الملف جاهز

# ================= إعداد الصفحة =================
st.set_page_config(page_title="ASS ChatBot", layout="wide")

# ================= الحالة =================
if "user" not in st.session_state:
    st.session_state.user = None
if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}
if "current_chat_id" not in st.session_state:
    st.session_state.current_chat_id = None

# ================= قاعدة البيانات =================
def init_db():
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    c.execute("""
        CREATE TABLE IF NOT EXISTS conversations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT NOT NULL,
            chat_id TEXT NOT NULL,
            role TEXT CHECK(role IN ('user', 'assistant')) NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

# ================= تسجيل الدخول =================
def check_credentials(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()
    conn.close()
    return result

def save_user(username, password):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

# ================= واجهة تسجيل الدخول =================
if st.session_state.user is None:
    st.title("👥 Welcome to Thakum ChatBot")
    tab1, tab2 = st.tabs(["🔐 Login", "🆕 Create Account"])

    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if check_credentials(username, password):
                st.session_state.user = username
                st.success("Logged in successfully ✅")
                st.rerun()
            else:
                st.error("Invalid credentials ❌")

    with tab2:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Create Account"):
            if save_user(new_user, new_pass):
                st.success("Account created! Please login ✅")
            else:
                st.error("Username already exists ❌")

    st.stop()

# ================= وظائف المحادثة =================
def new_chat():
    chat_id = str(uuid.uuid4())
    st.session_state.all_chats[chat_id] = {"title": "New Chat", "messages": []}
    st.session_state.current_chat_id = chat_id

def save_message(user, chat_id, role, content):
    conn = sqlite3.connect("users.db")
    c = conn.cursor()
    c.execute(
        "INSERT INTO conversations (user, chat_id, role, content) VALUES (?, ?, ?, ?)",
        (user, chat_id, role, content)
    )
    conn.commit()
    conn.close()

# ================= واجهة المحادثة =================
rag_chain = get_rag_chain()

with st.sidebar:
    st.header("💬 Your Chats")
    if st.button("➕ New Chat"):
        new_chat()
        st.rerun()
    for chat_id, chat in st.session_state.all_chats.items():
        if st.button(chat["title"], key=chat_id):
            st.session_state.current_chat_id = chat_id
            st.experimental_rerun()
    if st.button("🚪 Logout"):
        st.session_state.user = None
        st.session_state.all_chats = {}
        st.session_state.current_chat_id = None
        st.rerun()

st.title(f"🤖 ASS ChatBot | Welcome, {st.session_state.user}")

current_chat = st.session_state.all_chats.get(st.session_state.current_chat_id)
if current_chat:
    for msg in current_chat["messages"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Ask anything...")
    if user_input:
        current_chat["messages"].append({"role": "user", "content": user_input})
        save_message(st.session_state.user, st.session_state.current_chat_id, "user", user_input)
        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                answer = rag_chain.run(user_input)
                st.markdown(answer)
                current_chat["messages"].append({"role": "assistant", "content": answer})
                save_message(st.session_state.user, st.session_state.current_chat_id, "assistant", answer)

        if current_chat["title"] == "New Chat":
            current_chat["title"] = user_input[:30]
