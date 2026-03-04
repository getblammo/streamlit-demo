import os

import numpy as np
import pandas as pd
import streamlit as st

app_title = os.environ.get("APP_TITLE", "Dashboard")

st.set_page_config(page_title=app_title, layout="wide")
st.title("Data Dashboard")
st.write(f"Welcome to **{app_title}**")

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
