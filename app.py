import streamlit as st
import create_qr as cqr
import read_qr as rqr
import home as hm


st.set_page_config(page_title="QR Code Reader",page_icon="https://static.vecteezy.com/system/resources/previews/000/406/024/original/vector-qr-code-illustration.jpg",layout='centered')
#----------------Session state---------------
if 'read_qr' not in st.session_state:
    st.session_state.read_qr = False
if 'create_qr' not in st.session_state:
    st.session_state.create_qr = False
if 'page' not in st.session_state:
    st.session_state.page = 'Home'

with st.sidebar:
    st.markdown("## :green[Navigation]")
    page = st.radio("Go to",["🏠 Home", "🧩 Create QR", "📷 Read QR"],label_visibility="collapsed")
    st.session_state.page = page
    
if st.session_state.page == "🏠 Home":
    hm.App()  #function from home.py 

elif st.session_state.page == "🧩 Create QR":
    obj = cqr.createQR()   # function from create_qr.py
    

elif st.session_state.page == "📷 Read QR":
    rqr.readQR()   # function from read_qr.py
        
        
        
