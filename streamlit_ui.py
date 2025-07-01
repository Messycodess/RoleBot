import streamlit as st
import requests
import jwt  # pip install pyjwt

# === Backend URLs ===
BASE_URL = "http://localhost:8000"
LOGIN_URL = f"{BASE_URL}/login"
CHAT_URL = f"{BASE_URL}/chat"

# === Initialize session state ===
if "jwt" not in st.session_state:
    st.session_state.jwt = None
    st.session_state.username = ""
    st.session_state.role = ""

# === Decode role from JWT (without verification) ===
def extract_role_from_token(token):
    try:
        decoded = jwt.decode(token, options={"verify_signature": False})
        return decoded.get("role", "general")
    except Exception as e:
        return "general"

# === Login Page ===
def login():
    st.title("🔐 Role-Based ChatBot Login")
    st.write("Please log in with your credentials.")

    username = st.text_input("👤 Username")
    password = st.text_input("🔒 Password", type="password")

    if st.button("Login"):
        if not username or not password:
            st.error("Username and password are required.")
            return

        try:
            response = requests.post(LOGIN_URL, data={
                "username": username,
                "password": password
            })

            if response.status_code == 200:
                result = response.json()
                st.session_state.jwt = result["access_token"]
                st.session_state.username = username
                st.session_state.role = extract_role_from_token(result["access_token"])

                st.success("✅ Login successful!")
                st.rerun()
            else:
                st.error("❌ Login failed. Check credentials.")
        except Exception as e:
            st.error(f"🚫 Login error: {e}")

# === Chat UI ===
def chat():
    st.title("🤖 Smart RoleBot")
    st.markdown(f"👋 Hello, **{st.session_state.username}** (`{st.session_state.role}`)")

    # Optional suggestions based on role
    suggestions = {
        "hr": "💡 Try asking: *What are the leave policies?*",
        "finance": "💡 Try asking: *Show me Q1 budget summary*",
        "marketing": "💡 Try asking: *Latest campaign performance?*",
        "engineering": "💡 Try asking: *Explain the current system architecture*"
    }

    if st.session_state.role in suggestions:
        st.info(suggestions[st.session_state.role])

    query = st.text_area("💬 Your question:")

    if st.button("Ask"):
        headers = {"Authorization": f"Bearer {st.session_state.jwt}"}
        try:
            response = requests.post(CHAT_URL, json={"query": query}, headers=headers)
            if response.status_code == 200:
                answer = response.json()["answer"]
                st.success(answer)
            else:
                st.error(f"❌ Error {response.status_code}: {response.text}")
        except Exception as e:
            st.error(f"❌ Request failed: {e}")

    if st.button("Logout"):
        for key in ["jwt", "username", "role"]:
            st.session_state[key] = None
        st.rerun()

# === App Entrypoint ===
if st.session_state.jwt:
    chat()
else:
    login()
