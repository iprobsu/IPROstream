import streamlit as st

def login_page():
    st.markdown("""
        <style>
            .login-container {
                max-width: 400px;
                margin: 120px auto;
                padding: 30px;
                border-radius: 16px;
                background-color: rgba(32, 33, 36, 0.75);
                box-shadow: 0 0 15px rgba(0, 255, 170, 0.2);
                text-align: center;
            }
            .login-logo {
                width: 90px;
                filter: drop-shadow(0 0 10px #00ffaa);
                animation: bounce 2s infinite;
            }
            .login-header {
                color: white;
                font-size: 1.4rem;
                margin-top: 10px;
            }
            @keyframes bounce {
                0%, 100% { transform: translateY(0); }
                50% { transform: translateY(-10px); }
            }
        </style>
        <div class="login-container">
            <img src="assets/logo.png" class="login-logo" alt="Logo" />
            <h2 class="login-header">🔐 Welcome to IPRO Cloud</h2>
        </div>
    """, unsafe_allow_html=True)

    with st.form("login_form"):
        username = st.text_input("👤 Username")
        password = st.text_input("🔒 Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            if username == "admin" and password == "admin123":
                st.session_state.logged_in = True
                st.session_state.role = "Admin"
            elif username == "mod" and password == "mod123":
                st.session_state.logged_in = True
                st.session_state.role = "Moderator"
            else:
                st.error("❌ Invalid username or password")
