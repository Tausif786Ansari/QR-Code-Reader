import streamlit as st
import json
import base64
from pathlib import Path
from io import BytesIO
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import pandas as pd

# ---------------- Page Config ----------------
st.set_page_config(page_title="Digital Profile", page_icon="👤")

# ---------------- Load Profile ----------------
BASE_DIR = Path(__file__).resolve().parent.parent
PROFILES_DIR = BASE_DIR / "profiles"

pid = st.query_params.get("id")

if not pid:
    st.error("Invalid QR Code")
    st.stop()

profile_path = PROFILES_DIR / f"{pid}.json"

if not profile_path.exists():
    st.error("Profile not found")
    st.stop()

with open(profile_path, "r", encoding="utf-8") as f:
    profile = json.load(f)

# ---------------- UI ----------------
st.title("Digital Profile")

#-----------css on profile----------
st.markdown(
    f"""
    <img src="data:image/jpeg;base64,{profile['profile_image']}"
         style="width:160px;height:160px;border-radius:50%;object-fit:cover;">
    """,
    unsafe_allow_html=True
)
# # ---------- Profile Image ----------
# if profile.get("profile_image"):
#     image_bytes = base64.b64decode(profile["profile_image"])
#     st.image(image_bytes, width=160)

# ---------- Name ----------
first = profile["name"]["first"]
last = profile["name"]["last"]
name = f"{first} {last}"
st.subheader(name)

# ---------- Details ----------
st.write("📞", profile["phone"]["number"])
st.write("📧", profile["email"]["email"])

if profile.get("website"):
    st.write("🌐", profile["website"]["url"])

loc = profile.get("location", {})
location_text = ", ".join(filter(None, [
    loc.get("city"),
    loc.get("state"),
    loc.get("country")
]))
if location_text:
    st.write("📍", location_text)

st.dataframe(profile['socials'])

st.divider()

# ---------------- vCard ----------------
def create_vcard(p):
    first = p["name"]["first"]
    last = p["name"]["last"]

    lines = [
        "BEGIN:VCARD",
        "VERSION:3.0",
        f"N:{last};{first};;;",
        f"FN:{first} {last}",
        f"TEL;TYPE=CELL:{p['phone']['number']}",
        f"EMAIL:{p['email']['email']}",
    ]

    # Website
    if p.get("website"):
        lines.append(f"URL:{p['website']['url']}")

    # Address
    loc = p.get("location", {})
    if loc:
        adr = ";".join(map(str, [
            "",
            "",
            loc.get("street", ""),
            loc.get("city", ""),
            loc.get("state", ""),
            loc.get("postcode", ""),
            loc.get("country", ""),
        ]))
        lines.append(f"ADR;TYPE=HOME:{adr}")

    # Social profiles
    socials = p.get("socials", {})
    for platform, data in socials.items():
        lines.append(
            f"X-SOCIALPROFILE;TYPE={platform}:{data['url']}"
        )

    lines.append("END:VCARD")

    return "\r\n".join(lines)

vcard_data = create_vcard(profile)
cols = st.columns(2)
with cols[0]:
    st.download_button(
        "📇 Download vCard",
        vcard_data,
        file_name=f"{name}.vcf",
        mime="text/vcard"
    )

# ---------------- PDF ----------------
def create_pdf(p):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer)
    styles = getSampleStyleSheet()
    story = []

    # ---------- Name ----------
    first = p["name"]["first"]
    last = p["name"]["last"]
    name = f"{first} {last}"
    story.append(Paragraph(f"<b>{name}</b>", styles["Title"]))
    story.append(Spacer(1, 12))

    # ---------- Contact ----------
    story.append(Paragraph(f"📞 <b>Phone:</b> {p['phone']['number']}", styles["Normal"]))
    story.append(Paragraph(f"📧 <b>Email:</b> {p['email']['email']}", styles["Normal"]))

    if p.get("website"):
        story.append(
            Paragraph(f"🌐 <b>Website:</b> {p['website']['url']}", styles["Normal"])
        )

    story.append(Spacer(1, 10))

    # ---------- Location ----------
    loc = p.get("location", {})
    location_text = ", ".join(filter(None, [
        loc.get("city"),
        loc.get("state"),
        loc.get("country")
    ]))

    if location_text:
        story.append(
            Paragraph(f"📍 <b>Location:</b> {location_text}", styles["Normal"])
        )

    story.append(Spacer(1, 12))

    # ---------- Socials ----------
    socials = p.get("socials", {})
    if socials:
        story.append(Paragraph("<b>Social Profiles</b>", styles["Heading2"]))
        story.append(Spacer(1, 8))

        for platform, data in socials.items():
            line = f"{platform.title()}: {data['text']} ({data['url']})"
            story.append(Paragraph(line, styles["Normal"]))

    # ---------- Build PDF ----------
    doc.build(story)
    buffer.seek(0)
    return buffer

pdf_buffer = create_pdf(profile)
with cols[1]:
    st.download_button(
        "📄 Download PDF",
        pdf_buffer,
        file_name=f"{name}.pdf",
        mime="application/pdf"
    )
