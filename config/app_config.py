import streamlit as st

def configure_page():
    """Configure Streamlit page settings"""
    st.set_page_config(
        page_title="Student AI Prompt Engineering Hub",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def load_custom_css():
    """Load optimized CSS styling"""
    st.markdown("""
    <style>
    .main-header{font-size:2.5rem;font-weight:bold;color:#1f77b4;text-align:center;margin-bottom:2rem}
    .section-header{font-size:1.5rem;font-weight:bold;color:#ff7f0e;border-bottom:2px solid #ff7f0e;padding-bottom:0.5rem;margin-top:2rem;margin-bottom:1rem}
    .prompt-example{background-color:#e8f4fd;color:#1a1a1a;padding:1rem;border-radius:0.5rem;border-left:4px solid #1f77b4;margin:1rem 0;border:1px solid #d1ecf1}
    .tip-box{background-color:#e8f5e8;color:#1a1a1a;padding:1rem;border-radius:0.5rem;border-left:4px solid #2ca02c;margin:1rem 0;border:1px solid #c3e6cb}
    .warning-box{background-color:#fff8e1;color:#1a1a1a;padding:1rem;border-radius:0.5rem;border-left:4px solid #ffc107;margin:1rem 0;border:1px solid #f5c6cb}
    .stTextInput>div>div>input,.stTextArea>div>div>textarea,.stSelectbox>div>div>select{background-color:#ffffff!important;color:#000000!important;border:1px solid #cccccc!important}
    .streamlit-expanderContent{background-color:#ffffff;color:#000000}
    .stButton>button{background-color:#ffffff;color:#000000;border:1px solid #cccccc}
    .stButton>button:hover{background-color:#f0f0f0;color:#000000}
    </style>
    """, unsafe_allow_html=True)