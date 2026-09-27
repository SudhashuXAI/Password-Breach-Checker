import hashlib
import requests
import streamlit as st
from requests.exceptions import ConnectionError, Timeout

# ---------------------------------------------------------
# Core logic (same as project.py)
# ---------------------------------------------------------

def sha(password):
    return hashlib.sha1(password.encode()).hexdigest().upper()


def sha_split(password_hash):
    prefix_sha = password_hash[:5]
    suffix_sha = password_hash[5:]
    return prefix_sha, suffix_sha


def get_breach_data(prefix_sha):
    try:
        response = requests.get(f"https://api.pwnedpasswords.com/range/{prefix_sha}", timeout=8)
        return response.text
    except Timeout:
        return None
    except ConnectionError:
        return None


def find_suffix(breach_data, suffix_sha):
    lines = breach_data.strip().split("\n")
    for line in lines:
        parts = line.split(":")
        if parts[0] == suffix_sha:
            return int(parts[1])
    return 0


# ---------------------------------------------------------
# Page config + styling
# ---------------------------------------------------------

st.set_page_config(
    page_title="Password Breach Checker",
    page_icon="🔐",
    layout="centered",
)

st.markdown(
    """
    <style>
    .main {
        background-color: #0e1117;
    }
    .title-text {
        text-align: center;
        font-size: 2.4rem;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .subtitle-text {
        text-align: center;
        color: #9aa0a6;
        font-size: 1rem;
        margin-top: 4px;
        margin-bottom: 30px;
    }
    .result-box {
        padding: 22px;
        border-radius: 14px;
        margin-top: 20px;
        text-align: center;
        font-size: 1.15rem;
        font-weight: 600;
    }
    .safe {
        background-color: rgba(46, 204, 113, 0.12);
        border: 1px solid rgba(46, 204, 113, 0.5);
        color: #2ecc71;
    }
    .breached {
        background-color: rgba(231, 76, 60, 0.12);
        border: 1px solid rgba(231, 76, 60, 0.5);
        color: #e74c3c;
    }
    .info-box {
        background-color: rgba(52, 152, 219, 0.08);
        border: 1px solid rgba(52, 152, 219, 0.35);
        padding: 14px 18px;
        border-radius: 10px;
        font-size: 0.9rem;
        color: #cfd8dc;
        margin-top: 30px;
    }
    .footer {
        text-align: center;
        color: #6b7280;
        font-size: 0.8rem;
        margin-top: 40px;
    }
    code {
        word-break: break-all;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Header
# ---------------------------------------------------------

st.markdown('<p class="title-text">🔐 Password Breach Checker</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle-text">Check if your password has been exposed in a known data breach — '
    'without ever sending it over the internet.</p>',
    unsafe_allow_html=True,
)

# ---------------------------------------------------------
# Input
# ---------------------------------------------------------

password = st.text_input("Enter a password to check", type="password", placeholder="Type a password...")

col1, col2 = st.columns([1, 1])
with col1:
    check_clicked = st.button("🔍 Check Breach Status", use_container_width=True)
with col2:
    show_details = st.checkbox("Show technical details (hash / k-anonymity)", value=False)

# ---------------------------------------------------------
# Logic + Output
# ---------------------------------------------------------

if check_clicked:
    if not password:
        st.warning("Please enter a password first.")
    else:
        with st.spinner("Checking against known breaches..."):
            password_hash = sha(password)
            prefix, suffix = sha_split(password_hash)
            breach_data = get_breach_data(prefix)

        if breach_data is None:
            st.markdown(
                '<div class="result-box breached">⚠️ Could not reach the breach database.<br>'
                'Please check your internet connection and try again.</div>',
                unsafe_allow_html=True,
            )
        else:
            count = find_suffix(breach_data, suffix)

            if count == 0:
                st.markdown(
                    '<div class="result-box safe">✅ Good news — this password was '
                    'not found in any known data breach.</div>',
                    unsafe_allow_html=True,
                )
                st.balloons()
            else:
                st.markdown(
                    f'<div class="result-box breached">🚨 This password has appeared in '
                    f'<b>{count:,}</b> known data breaches.<br>Change it immediately, '
                    f'especially if you reuse it elsewhere.</div>',
                    unsafe_allow_html=True,
                )

        if show_details:
            st.markdown("#### 🔎 How this check worked")
            st.write("**Full SHA-1 hash of your password:**")
            st.code(password_hash)
            st.write("**Prefix sent to the API (only this leaves your device):**")
            st.code(prefix)
            st.write("**Suffix kept locally, compared against the API's response:**")
            st.code(suffix)

# ---------------------------------------------------------
# Info footer
# ---------------------------------------------------------

st.markdown(
    """
    <div class="info-box">
    <b>How it stays private:</b> Your password is hashed on this device using SHA-1, then only the
    first 5 characters of that hash are sent to the Have I Been Pwned API. The API replies with every
    breached hash sharing that prefix (often hundreds of them), and the exact match is found locally —
    your full password, and even your full hash, never leave this device. This technique is called
    <b>k-anonymity</b>.
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    '<p class="footer">Built with Python + Streamlit · Powered by the '
    '<a href="https://haveibeenpwned.com/API/v3#PwnedPasswords" target="_blank">'
    'Have I Been Pwned Pwned Passwords API</a></p>'
    '<p class="footer">Made with 💻 by <b>Sudhanshu Tiwari</b></p>',
    unsafe_allow_html=True,
)