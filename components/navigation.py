import streamlit as st

def navigation_bar():
    st.sidebar.image("assets/logo.png", width=80)
    st.sidebar.markdown("## 📚 IPROstream")
    st.sidebar.markdown("---")

    pages = {
        "Home": "🏠 Home",
        "Edit": "✏️ Edit Data",
        "Summary": "📊 Summary"
    }

    for key, label in pages.items():
        if st.sidebar.button(label, key=key):
            st.session_state.page = key
            st.experimental_rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"🔒 Role: **{st.session_state.role}**")
    if st.sidebar.button("🔓 Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()
