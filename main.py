import streamlit as st
import pandas as pd
import numpy as np
import io
import streamlit.components.v1 as components
import datetime

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Moon Papers",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CLOSING NOTICE & REDIRECT LOGIC
# ==========================================
# Set the deadline date (3 days from Jan 5, 2026 -> Jan 8, 2026)
redirect_date = datetime.datetime(2026, 1, 8)

if datetime.datetime.now() > redirect_date:
    # ---------------------------------------------------------
    # SCENARIO A: DEADLINE PASSED (Immediate Redirect)
    # ---------------------------------------------------------
    st.markdown(
        """
        <style>
            /* Hide Streamlit UI elements during the transition */
            .stApp { display: none; }
        </style>
        <meta http-equiv="refresh" content="0; url=https://chessmastermind.github.io/moon-papers/" />
        <script>
            window.location.href = "https://chessmastermind.github.io/moon-papers/";
        </script>
        <div style="text-align: center; padding: 50px;">
            <h1>Website Closed</h1>
            <p>Redirecting to <a href="https://chessmastermind.github.io/moon-papers/">Moon Papers</a>...</p>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.stop()

else:
    # ---------------------------------------------------------
    # SCENARIO B: DEADLINE ACTIVE (Popup + Iframe)
    # ---------------------------------------------------------
    
    # 1. CSS: Hide UI & Force Dark Theme
    st.markdown("""
        <style>
            /* Hide Header, Footer, Hamburger, Toolbar */
            header, footer, [data-testid="stToolbar"], .stDeployButton {
                display: none !important;
            }
            
            /* Remove Padding/Margins for Full Screen Feel */
            .block-container {
                padding: 0 !important;
                margin: 0 !important;
                max-width: 100% !important;
            }
            
            /* Force Background Black */
            .stApp {
                background-color: #000000 !important;
            }
            
            /* Button Styling for the Popup */
            .stButton > button {
                width: 100%;
                border-radius: 8px;
                background-color: #262730;
                color: white;
                border: 1px solid #444;
            }
            .stButton > button:hover {
                border-color: #00ff00;
                color: #00ff00;
            }
        </style>
    """, unsafe_allow_html=True)

    # 2. Popup State Management
    if 'popup_closed' not in st.session_state:
        st.session_state['popup_closed'] = False

    # 3. Logic: Show Popup OR Show Website
    if not st.session_state['popup_closed']:
        # --- THE POPUP ---
        # We use a container to center the warning message
        with st.container():
            st.markdown("<br><br><br>", unsafe_allow_html=True) # Spacer
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                st.info(f"⚠️ **Notice:** This legacy link will stop working on {redirect_date.strftime('%B %d, %Y')}. Please update your bookmarks.")
                
                # The 'Got it' button
                if st.button("I understand, continue to site"):
                    st.session_state['popup_closed'] = True
                    st.rerun()

    else:
        # --- THE WEBSITE (Full Screen) ---
        # This only renders after the user clicks the button
        html_content = """
        <!DOCTYPE html>
        <html style="overflow: hidden;">
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <script data-goatcounter="https://moon-papers.goatcounter.com/count"
                    async src="//gc.zgo.at/count.js"></script>
        </head>
        <body style="margin: 0; padding: 0; background-color: #000000;">
            <iframe 
                src="https://chessmastermind.github.io/moon-papers/" 
                style="position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; border: none; z-index: 9999;"
                allowfullscreen
            ></iframe>
        </body>
        </html>
        """
        components.html(html_content, height=1000, scrolling=False)
