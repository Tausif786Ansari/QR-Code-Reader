import streamlit as st
import base64
import json
import uuid
import os
import qrcode
from io import BytesIO

# ------------------ Ensure profiles dir ------------------
os.makedirs("profiles", exist_ok=True)
    
# ------------------ Helper: Image → Base64 ------------------
def image_to_base64(uploaded_file):
    return base64.b64encode(uploaded_file.getvalue()).decode("utf-8")
       
#--------------Main Function-------------------------------
def createQR():
    #-------------------Session State--------------------------
    if "youtube" not in st.session_state:
        st.session_state.youtube = False
    if "linkedin" not in st.session_state:
        st.session_state.linkedin = False
    if "facebook" not in st.session_state:
        st.session_state.facebook = False
    if "instagram" not in st.session_state:
        st.session_state.instagram = False
    if 'profile_photo' not in st.session_state:
        st.session_state.profile_photo = None
    if 'profile_created' not in st.session_state:
        st.session_state.profile_created = False
    if 'profile_id' not in st.session_state:
        st.session_state.profile_id = None
    if "qr_bytes" not in st.session_state:
        st.session_state.qr_bytes = None
    if 'qr_created' not in st.session_state:
        st.session_state.qr_created = False

    # ------------------ UI ------------------
    st.title(":rainbow[Create QR Code]")
    st.subheader(":orange[Personal Information]")
    profile_data = {}
    # ---------- Profile Image ----------
    with st.expander("Add Profile Image"):
        photo = st.file_uploader("Upload your photo",type=["png", "jpg", "jpeg"])
        if photo:
            st.image(photo, width=150)
            st.session_state.profile_photo = photo
            profile_data["profile_image"] = image_to_base64(st.session_state.profile_photo)
            
    # ---------- Name ----------
    with st.expander("Add Name"):
        cols = st.columns(2)
        with cols[0]:
            fname = st.text_input("Enter First Name",max_chars=20)
        with cols[1]:
            lname = st.text_input("Enter Last Name",max_chars=20)
        profile_data["name"] = {"first": fname, "last": lname}
            
    # ---------- Phone ----------
    with st.expander("Add Phone Detail"):
        cols = st.columns(2)
        with cols[0]:
            phoneType = st.text_input("Enter Label",placeholder="Work/Personal",max_chars=20)
        with cols[1]:
            phoneNo = st.number_input("Enter the Number",placeholder=8134992573,min_value=1000000000,max_value=9999999999)
        profile_data["phone"] = {"label": phoneType, "number": phoneNo}
        
    # ---------- Email ----------
    with st.expander("Add Email Detail"):
        cols = st.columns(2)
        with cols[0]:
            emailLabel = st.text_input("Enter Label",placeholder="Work/Personal Email",max_chars=20)
        with cols[1]:
            email = st.text_input("Email",placeholder="name123@gmail.com")
        profile_data["email"] = {"label": emailLabel, "email": email}   
         
    # ---------- Website ----------
    with st.expander("Add Website Detail"):
        cols = st.columns(2)
        with cols[0]:
            webLabel = st.text_input("Enter Label",placeholder="My Portfolio",max_chars=20)
        with cols[1]:
            webLink = st.text_input("Website Link",placeholder="www.linkedin/Tausif.com")
        profile_data["website"] = {"label": webLabel, "url": webLink}
        
    # ---------- Location ----------
    with st.expander("Add Location Detail"):
        cols = st.columns(3)
        with cols[0]:
            street = st.text_input("Street/Locality",placeholder="Kukatpally",max_chars=20)
        with cols[1]:
            HouseNo = st.number_input("House No",placeholder=358,min_value=1,max_value=500)
        with cols[2]:
            postCode = st.number_input("Postal Code",placeholder=493221,min_value=100000,max_value=999999)
        colls = st.columns(2)
        with colls[0]:
            city = st.text_input("City",placeholder="Hyderabad",max_chars=20)
        with colls[1]:
            state = st.text_input("State",placeholder="Telangana",max_chars=20)
        country = st.text_input("Country",placeholder="India",max_chars=20)
        profile_data["location"] = {"street": street,"house_no": HouseNo,"postcode": postCode,
                                    "city": city,"state": state,"country": country,}
        
    # ---------- Social Networks ----------
    socials = {}
    with st.expander("Social Networks"):
        colles = st.columns(4)
        #----------Instagram--------------
        with colles[0]:
            st.image(r"C:\Users\Tausif Ansari\Downloads\1715965947instagram-logo-png (1).png",width=50)
            if st.button("Instagram"):
                st.session_state.instagram = not st.session_state.instagram
        if st.session_state.instagram:       
            with st.expander("📸 Instagram Details", expanded=True):
                cols = st.columns(2)
                with cols[0]:
                    ig_url = st.text_input("Instagram Username / URL")
                with cols[1]:
                    ig_text = st.text_input("Display Text", value="Follow me on Instagram")
                socials["instagram"] = {"url": ig_url, "text": ig_text}
        #----------Facebook-----------------
        with colles[1]:
            st.image(r"C:\Users\Tausif Ansari\Downloads\facebook-logo.png",width=50)
            if st.button("📘 Facebook"):
                st.session_state.facebook = not st.session_state.facebook
        if st.session_state.facebook:
            with st.expander("📘 Facebook Details", expanded=True):
                cols = st.columns(2)
                with cols[0]:
                    fb_url = st.text_input("Facebook Username / URL")
                with cols[1]:
                    fb_text = st.text_input("Display Text", value="Follow me on Facebook")
                    socials["facebook"] = {"url": fb_url, "text": fb_text}
        #--------------YouTube------------------
        with colles[2]:
            st.image(r"C:\Users\Tausif Ansari\Downloads\1701508703YouTube-Icon-PNG.png",width=50)
            if st.button("▶ YouTube"):
                st.session_state.youtube = not st.session_state.youtube
        if st.session_state.youtube:
            with st.expander("▶ YouTube Details", expanded=True):
                cols = st.columns(2)
                with cols[0]:
                    yt_url = st.text_input("YouTube Channel URL")
                with cols[1]:
                    yt_text = st.text_input("Display Text", value="Subscribe to my channel")
                socials["youtube"] = {"url": yt_url, "text": yt_text}
        #----------------Linkedin-----------------
        with colles[3]:
            st.image(r"C:\Users\Tausif Ansari\Downloads\1715491541linkedin-logo-transparent.png",width=50)
            if st.button("💼 LinkedIn"):
                st.session_state.linkedin = not st.session_state.linkedin
        if st.session_state.linkedin:
            with st.expander("💼 LinkedIn Details", expanded=True):
                cols = st.columns(2)
                with cols[0]:
                    li_url = st.text_input("LinkedIn Profile URL")
                with cols[1]:
                    li_text = st.text_input("Display Text", value="Connect with me on LinkedIn")
                socials["linkedin"] = {"url": li_url, "text": li_text}
                
    # ------------------ Save Profile ------------------
    cols = st.columns(3)
    with cols[0]:
        if st.button("Create Profile & Save"):
            if len(socials) != 4:
                st.warning("Fill Social Informations")
            elif len(profile_data) != 6:
                st.warning("Fill The Details")
            else:
                profile_id = str(uuid.uuid4())
                profile_data = {"id": profile_id, **{k: v for k, v in profile_data.items() if k != "id" and k != "socials"}, "socials": socials}
                with open(f"profiles/{profile_id}.json", "w") as f:
                    json.dump(profile_data, f, indent=4)

                st.session_state.profile_created = True
                st.session_state.profile_id = profile_id
                
    if st.session_state.profile_created:
        st.success("🎉 Profile saved successfully!")           
    #----------------Creating QR Code------------------------
    with cols[1]:
        if st.session_state.profile_created:
            if st.button("Generate QR Code"):
                profile_url = f"http://localhost:8501/profile_view?id={st.session_state.profile_id}"
                qr = qrcode.make(profile_url)
                buf = BytesIO()
                qr.save(buf,format="PNG")
                buf.seek(0)
                st.session_state.qr_bytes = buf.getvalue()
                st.session_state.qr_created = True
                
    #---------------Downloading QR Code---------------------
    with cols[2]:
        if st.session_state.qr_created:
            st.download_button(
                label="⬇ Download QR (PNG)",
                data=st.session_state.qr_bytes,
                file_name="my_qr.png",
                mime="image/png"
            )
    #-----------------Displaying QR Code-------------------
    if st.session_state.qr_created:
        st.image(st.session_state.qr_bytes, caption="Scan Me")
        st.code(profile_url)


             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
             
                    
            
   