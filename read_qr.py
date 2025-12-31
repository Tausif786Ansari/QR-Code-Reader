import streamlit as st
import numpy as np
import cv2
import tempfile

def readQR():
        st.title(":rainbow[QR Code Reader]")
        tabs = st.tabs(['Home','Image','Video'],default='Home')
        #----------session state-------------
        if 'data' not in st.session_state:
            st.session_state.data = None
        if 'qr_found' not in st.session_state:
            st.session_state.qr_found = False
        #----------------tabs[0]-------------------
        with tabs[0]:
            st.markdown("""
                <div>
                    <h3>Scan QR codes instantly using your camera or uploaded images.</h3>
                    This app detects and decodes QR codes in real time with high accuracy, making it easy to extract links, text, and encoded data effortlessly.
                </div>
            """,unsafe_allow_html=True)
        #----------Function To read QR Code from a video------------------
        def read_qr_code(file):
            if isinstance(file,int):
                cap = cv2.VideoCapture(0)
            else:
                cap = cv2.VideoCapture(file.name)
            qr_obj = cv2.QRCodeDetector()

            st.session_state.qr_found = False
            st.session_state.data = None
            space = st.empty()  # video placeholder
            #-------------------Loop that plays the video-------------------
            while cap.isOpened() and not st.session_state.qr_found:
                ret, frame = cap.read()
                if not ret:
                    break
                data, bbox, _ = qr_obj.detectAndDecode(frame)
                if data:
                    st.session_state.qr_found = True
                    st.session_state.data = data
                    break
                
                frame = cv2.resize(frame,(800,600))
                frame = cv2.flip(frame,1)
                space.image(frame, channels='BGR', caption="Scanning the live WebCam..." if isinstance(file,int) else "Scanning video...")

            # 🔹 Stop video & clear screen
            cap.release()
            space.empty()   # ⬅ removes video frame from UI

            # 🔹 Display QR details
            if st.session_state.qr_found:
                st.success("✅ QR Code Found!")
                st.markdown("### 📌 QR Code Details")
                st.write(f"### Content: {st.session_state.data}")
            else:
                st.error("❌ No QR Code found in the video")
        #----------------tabs[1]-------------------
        with tabs[1]:
            st.subheader(":orange[Read The QR Code from a Image]")
            img = st.file_uploader("Enter The Image of QR Code",type=["jpg","png","jpeg"])
            if img:
                img_arr = np.frombuffer(img.read(),np.uint8)
                img_qr = cv2.imdecode(img_arr,cv2.IMREAD_COLOR)
                qr_obj = cv2.QRCodeDetector()
                data,bbox,_ = qr_obj.detectAndDecode(img_qr)
                if bbox is not None:
                    st.markdown("### 📌 QR Code Details")
                    st.write(f"#### Content: {data}")
                else:
                    st.error("❌ No Valid QR Code found")
                img = cv2.resize(img_qr,None,fx=0.5,fy=0.5)
                st.divider()
                st.image(img,channels="BGR",caption="QR Code")
        #-----------------tabs[2]--------------------
        with tabs[2]:
            st.subheader(":orange[Read the QR Code from a Video]")
            source = st.pills("Select The Source", ['Video', 'WebCam'])

            if source == 'Video':
                #-----------Uploading the video-------------------
                video = st.file_uploader("Upload a video containing QR code",type=["mp4", "avi", "mov", "mkv"])

                if video:
                    #----------------Loading the video in array format----------------
                    tfile = tempfile.NamedTemporaryFile(delete=False)
                    tfile.write(video.read())
                    read_qr_code(tfile)
            elif source == 'WebCam':
                read_qr_code(0)
                        