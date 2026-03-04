import os
from hashlib import sha256

import numpy as np
import pandas as pd
import streamlit as st

app_title = os.environ.get("APP_TITLE", "Dashboard")

st.set_page_config(page_title=app_title, layout="wide")

# --- Simple session-based auth ---

USERS_DB: dict[str, dict] = {}  # email -> {name, email, password_hash}


def hash_pw(pw: str) -> str:
    return sha256(pw.encode()).hexdigest()


def auth_ui():
    """Show login/signup forms. Returns True if authenticated."""
    if st.session_state.get("authenticated"):
        return True

    tab_login, tab_signup = st.tabs(["Login", "Sign Up"])

    with tab_signup:
        st.subheader("Sign Up")
        with st.form("signup_form"):
            name = st.text_input("Name", key="signup_name")
            email = st.text_input("Email", key="signup_email")
            password = st.text_input("Password", type="password", key="signup_password")
            submitted = st.form_submit_button("Sign Up")
            if submitted:
                if not name or not email or not password:
                    st.error("All fields are required.")
                elif email in USERS_DB:
                    st.error("Email already registered.")
                else:
                    USERS_DB[email] = {
                        "name": name,
                        "email": email,
                        "password_hash": hash_pw(password),
                    }
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = email
                    st.session_state["user_name"] = name
                    st.rerun()

    with tab_login:
        st.subheader("Login")
        with st.form("login_form"):
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_password")
            submitted = st.form_submit_button("Login")
            if submitted:
                user = USERS_DB.get(email)
                if user and user["password_hash"] == hash_pw(password):
                    st.session_state["authenticated"] = True
                    st.session_state["user_email"] = email
                    st.session_state["user_name"] = user["name"]
                    st.rerun()
                else:
                    st.error("Invalid credentials.")

    return False


# --- Main app ---

if not auth_ui():
    st.stop()

# Authenticated — show dashboard
st.sidebar.write(f"Logged in as **{st.session_state['user_name']}**")
if st.sidebar.button("Logout"):
    st.session_state.clear()
    st.rerun()

st.title("Data Dashboard")
st.write(f"Welcome to **{app_title}**, {st.session_state['user_name']}!")

# Sample data
np.random.seed(42)
dates = pd.date_range(start="2025-01-01", periods=90, freq="D")
df = pd.DataFrame(
    {
        "date": dates,
        "revenue": np.random.uniform(1000, 5000, size=90).cumsum(),
        "users": np.random.randint(50, 300, size=90).cumsum(),
        "sessions": np.random.randint(100, 800, size=90),
    }
)

st.subheader("Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${df['revenue'].iloc[-1]:,.0f}")
col2.metric("Total Users", f"{df['users'].iloc[-1]:,}")
col3.metric("Avg Sessions", f"{df['sessions'].mean():,.0f}")

st.subheader("Raw Data")
st.dataframe(df, use_container_width=True)

st.subheader("Revenue Over Time")
st.line_chart(df.set_index("date")["revenue"])

st.subheader("Users Over Time")
st.line_chart(df.set_index("date")["users"])
