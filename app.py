import streamlit as st
from components.auth import login_page
from components.navigation import navigation_bar
from utils.load_data import load_ip_data
import pages.home as home
import pages.edit as edit
import pages.summary as summary

# --- Set Page Config ---
st.set_page_config(page_title="IP Masterlist Dashboard", layout="wide")

# --- Session State Initialization ---
defaults = {
    "logged_in": False,
    "role": None,
    "page": "Home",
    "dark_mode": False,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

# --- LOGIN PAGE: Stop app if not logged in ---
if not st.session_state.logged_in:
    login_page()
    st.stop()

# --- DARK MODE TOGGLE ---
dark_mode_color = "#e8eaed" if not st.session_state.dark_mode else "#ffffff"
st.session_state.dark_mode = st.sidebar.toggle("🌗 Dark Mode", value=st.session_state.dark_mode)

# --- NAVIGATION BAR ---
navigation_bar()

# --- LOAD DATA ---
df = load_ip_data()

# --- PAGE ROUTER ---
if st.session_state.page == "Home":
    home.render(df)
elif st.session_state.page == "Edit":
    edit.render(df)
elif st.session_state.page == "Summary":
    summary.render(df)
