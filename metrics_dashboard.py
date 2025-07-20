import streamlit as st
import requests
import time

BACKEND_URL = "http://localhost:5000/metrics"

# Streamlit page setup
st.set_page_config(page_title="📊 RAG Backend Metrics", layout="centered")
st.title("📈 Real-time Metrics Dashboard")

# Placeholder for real-time updates
placeholder = st.empty()

# Auto-refresh loop
while True:
    try:
        res = requests.get(BACKEND_URL)
        if res.status_code == 200:
            data = res.json()
            total = data["total_requests"]
            errors = data["errors"]
            latency = data["average_latency_sec"]

            # Display metrics
            with placeholder.container():
                st.metric("📨 Total Requests", total)
                st.metric("❌ Errors", errors)
                st.metric("⏱️ Avg Response Time", f"{latency} sec")
        else:
            st.error("❗ Failed to fetch metrics from backend.")
    except Exception as e:
        st.error(f"⚠️ Error: {str(e)}")

    time.sleep(3)  # Refresh every 3 seconds
