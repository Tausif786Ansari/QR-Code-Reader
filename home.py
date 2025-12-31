import streamlit as st

def App():
    st.title(":blue[QR Studio]")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("""
        ### Create • Scan • Decode QR Codes Instantly

        A modern Streamlit application to **generate and read QR codes**
        from **images, videos, and live webcam** using OpenCV.
        """)

        st.markdown(
            "[🌐 GitHub](https://github.com/Tausif786Ansari) &nbsp;&nbsp; "
            "[💼 LinkedIn](https://www.linkedin.com/in/tausif-ansari-10nov2001/)"
        ,unsafe_allow_html=True)

    with col2:
        st.image(
            r"C:\Users\Tausif Ansari\Downloads\Copilot_20251229_002613.png",
            width=180
        )
    st.divider()
    st.markdown("### ✨ Key Features")
    cols = st.columns(3)
    with cols[0]:
        st.markdown("#### 🧩Create QR")
        st.write("Generate QR codes from text, URLs, or custom data.")

    with cols[1]:
        st.markdown("#### 📷Read QR")
        st.write("Scan QR codes from images, videos, or webcam.")

    with cols[2]:
        st.markdown("#### ⚡Fast & Accurate")
        st.write("Powered by OpenCV for real-time detection.")
    
    st.divider()
    st.markdown("### 🔍 How It Works")
    st.markdown("""
        1️⃣ Choose **Create QR** or **Read QR** from the sidebar  
        2️⃣ Upload an image/video or use your webcam  
        3️⃣ Instantly get decoded QR content  
        4️⃣ Download or reuse QR codes easily  
    """)
    
    st.divider()
    st.markdown("## 🎯 Use Cases")
    cols = st.columns(3)
    with cols[0]:
        st.write("🏢 Business cards & URLs")

    with cols[1]:
        st.write("📦 Product labels")

    with cols[2]:
        st.write("🎟 Event tickets & passes")
    
    st.divider()
    st.markdown("## 🛠 Tech Stack")
    ts = st.columns(4)
    ts[0].write("🐍 Python")
    ts[1].write("🎯 Streamlit")
    ts[2].write("👁 OpenCV")
    ts[3].write("📦 NumPy")
    
    st.divider()
    st.markdown(
        """
        <div style="text-align:center; color:gray;">
            Built with ❤️ by <b>Tausif Ansari</b><br>
            QR Studio • Streamlit Project
        </div>
        """,
        unsafe_allow_html=True)




 