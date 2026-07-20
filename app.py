import streamlit as st
import datetime
import random
import json
import os
import base64
import io
from PIL import Image

st.set_page_config(page_title="مراقبت پس از زایمان", page_icon="🌸", layout="wide")

BACKGROUND_IMAGE_URL = "https://cdn.pixabay.com/photo/2020/05/30/19/29/mother-5240383_960_720.jpg"

st.markdown(f"""
<style>
    * {{ font-family: Tahoma, sans-serif; }}
    .stApp {{
        background: linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.85)),
                    url('{BACKGROUND_IMAGE_URL}');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    .main-title {{
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #4a148c;
        text-shadow: 2px 2px 8px rgba(255,255,255,0.8);
        background: rgba(255,255,255,0.3);
        padding: 15px;
        border-radius: 20px;
        backdrop-filter: blur(5px);
        display: inline-block;
        margin: 0 auto;
    }}
    .glass-card {{
        background: rgba(255,255,255,0.75);
        backdrop-filter: blur(15px);
        -webkit-backdrop-filter: blur(15px);
        border-radius: 30px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.12);
        margin-bottom: 20px;
        border: 1px solid rgba(255,255,255,0.3);
        transition: all 0.3s ease;
    }}
    .glass-card:hover {{
        box-shadow: 0 12px 48px rgba(0,0,0,0.18);
        transform: translateY(-2px);
    }}
    .code-box {{
        background: rgba(255,255,255,0.6);
        padding: 12px 20px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #f06292;
        font-family: monospace;
        font-size: 1.2rem;
        color: #880e4f;
        backdrop-filter: blur(5px);
    }}
    .doctor-card {{
        background: rgba(255,255,255,0.6);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 15px 20px;
        margin: 10px 0;
        border-left: 4px solid #f06292;
        transition: all 0.3s ease;
    }}
    .doctor-card:hover {{
        background: rgba(255,255,255,0.8);
        transform: translateX(5px);
    }}
    .chat-container {{
        background: rgba(255,255,255,0.4);
        border-radius: 20px;
        padding: 15px;
        max-height: 350px;
        overflow-y: auto;
        border: 1px solid rgba(255,255,255,0.3);
        backdrop-filter: blur(5px);
    }}
    .message-bubble {{
        background: rgba(255,255,255,0.7);
        border-radius: 15px;
        padding: 10px 15px;
        margin: 8px 0;
        max-width: 80%;
        color: #4a148c;
        backdrop-filter: blur(5px);
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
    }}
    .message-bubble.sent {{
        background: #f06292;
        color: white;
        margin-left: auto;
    }}
    .message-bubble.received {{
        background: rgba(255,255,255,0.8);
        margin-right: auto;
        border: 1px solid #f8bbd0;
    }}
    .footer {{
        text-align: center;
        color: #4a148c;
        margin-top: 40px;
        padding: 20px;
        border-top: 2px solid rgba(244, 143, 177, 0.3);
        font-weight: 500;
        background: rgba(255,255,255,0.3);
        backdrop-filter: blur(5px);
        border-radius: 20px;
    }}
    .footer .highlight {{
        color: #c2185b;
        font-weight: 700;
    }}
    .stButton > button {{
        background: linear-gradient(145deg, #f06292, #ec407a) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 10px 25px !important;
        font-weight: 600 !important;
        width: 100%;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(236, 64, 122, 0.3);
    }}
    .stButton > button:hover {{
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(236, 64, 122, 0.4);
    }}
</style>
""", unsafe_allow_html=True)

SECRET_KEY = 137

def motabeghat(adad):
    b = 0
    u = 0
    if adad % 2 == 0:
        b += 1
    else:
        u += 1
    s = sum(int(d) for d in str(adad))
    if s % 2 == 0:
        b += 1
    else:
        u += 1
    for i in range(1, int(s**0.5) + 1):
        if s % i == 0:
            jam = i + s // i
            if jam % 2 == 0:
                b += 1
            else:
                u += 1
    return b, u

def ramz_kon(harf):
    adad = ord(harf) + SECRET_KEY
    b, u = motabeghat(adad)
    return str(b) + "." + str(u)

def ramz_baz(ramz):
    try:
        b_str, u_str = ramz.split(".")
        b = int(b_str)
        u = int(u_str)
        for i in range(32, 127):
            bb, uu = motabeghat(i)
            if bb == b and uu == u:
                return chr(i - SECRET_KEY)
        return "؟"
    except:
        return "❗"

def sakht_kod_madar():
    return f"M-{random.randint(10000, 99999)}"

def tarikh():
    return datetime.date.today() + datetime.timedelta(days=60)

DATA_FILE = "data.json"

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {
        "doctors": [
            {"name": "دکتر احمدی", "hospital": "بیمارستان فارابی", "type": "زنان", "code": "DrAhmadi2024"},
            {"name": "دکتر محمدی", "hospital": "بیمارستان قشم", "type": "کودکان", "code": "DrMohammadi2024"},
            {"name": "دکتر رضایی", "hospital": "بیمارستان خلیج فارس", "type": "زنان", "code": "DrRezaei2024"}
        ],
        "mothers": [],
        "messages": []
    }

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

data = load_data()
doctor_list = data["doctors"]
madar_list = data["mothers"]

ADMIN_PASSWORD = "ahlat..mm666"
DOCTOR_GENERAL_CODE = "752*36+9"
MOTHER_GENERAL_CODE = "MOTHER2024"

st.markdown('<p class="main-title">🌸 مراقبت پس از زایمان</p>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("👩 مادر", use_container_width=True):
        st.session_state.role = "مادر"
        st.session_state.logged_in = False
        st.rerun()
with col2:
    if st.button("👨‍⚕️ پزشک", use_container_width=True):
        st.session_state.role = "پزشک"
        st.session_state.logged_in = False
        st.rerun()
with col3:
    if st.button("⚙️ مدیریت", use_container_width=True):
        st.session_state.role = "مدیر"
        st.session_state.logged_in = False
        st.rerun()

# ================== پنل مادر ==================
if st.session_state.get("role") == "مادر":
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("👩 پنل مادر")
        if not st.session_state.get("logged_in"):
            general_code = st.text_input("کد عمومی مادران را وارد کنید:", type="password")
            if general_code == MOTHER_GENERAL_CODE:
                st.success("✅ کد عمومی صحیح است!")
                mother_code = st.text_input("کد اختصاصی خود را وارد کنید:", type="password")
                if st.button("ورود به پنل"):
                    found = None
                    for m in madar_list:
                        if m["code"] == mother_code:
                            found = m
                            break
                    if found:
                        st.session_state.mother = found
                        st.session_state.logged_in = True
                        st.success("✅ ورود موفق!")
                        st.rerun()
                    else:
                        st.error("❌ کد اختصاصی نامعتبر است!")
            else:
                if general_code:
                    st.error("❌ کد عمومی اشتباه است!")
            st.divider()
            st.subheader("📝 ثبت‌نام مادر جدید")
            name = st.text_input("نام مادر")
            if st.button("ثبت‌نام"):
                if name:
                    new_code = sakht_kod_madar()
                    new_mother = {"name": name, "code": new_code, "chats": {}}
                    madar_list.append(new_mother)
                    data["mothers"] = madar_list
                    save_data(data)
                    st.success("✅ ثبت‌نام موفق!")
                    st.markdown(f'<div class="code-box">کد عمومی: {MOTHER_GENERAL_CODE}</div>', unsafe_allow_html=True)
                    st.markdown(f'<div class="code-box">کد اختصاصی شما: {new_code}</div>', unsafe_allow_html=True)
                    st.warning("⚠️ این کدها را ذخیره کنید.")
        else:
            mother = st.session_state.mother
            st.success(f"👋 خوش آمدید، {mother['name']}!")
            st.info(f"🔑 کد اختصاصی شما: {mother['code']}")
            
            st.subheader("🔐 رمزنگاری پیام")
            tab1, tab2 = st.tabs(["✉️ تبدیل پیام به کد", "🔓 تبدیل کد به پیام"])
            with tab1:
                msg = st.text_area("پیام خود را وارد کنید:")
                if st.button("ساخت کد"):
                    if msg:
                        code = ""
                        for char in msg:
                            code += ramz_kon(char) + " "
                        st.success("✅ کد شما ساخته شد!")
                        st.markdown(f'<div class="code-box">{code.strip()}</div>', unsafe_allow_html=True)
            with tab2:
                code_input = st.text_input("کد دریافتی را وارد کنید:")
                if st.button("رمزگشایی"):
                    if code_input:
                        parts = code_input.split()
                        message = ""
                        for part in parts:
                            message += ramz_baz(part)
                        st.success("✅ پیام اصلی:")
                        st.markdown(f'<div class="code-box">{message}</div>', unsafe_allow_html=True)
            
            st.subheader("💬 چت با پزشک")
            doctor_codes = [doc["code"] for doc in doctor_list]
            target_doctor = st.selectbox("پزشک مورد نظر:", doctor_codes)
            chat_key = f"chat_{target_doctor}"
            if chat_key not in mother.get("chats", {}):
                mother["chats"][chat_key] = []
            for msg in mother["chats"][chat_key]:
                if datetime.datetime.fromisoformat(msg['expires']) < datetime.datetime.now():
                    continue
                st.markdown(f"""
                <div class="message-bubble {'sent' if msg['sender'] == mother['name'] else 'received'}">
                    <div>{msg['text']}</div>
                    <div style="font-size: 0.7rem; opacity: 0.6;">{msg['time']}</div>
                </div>
                """, unsafe_allow_html=True)
            new_msg = st.text_input("پیام خود را بنویسید:")
            if st.button("ارسال پیام"):
                if new_msg:
                    msg_data = {
                        "sender": mother['name'],
                        "text": new_msg,
                        "time": datetime.datetime.now().strftime("%H:%M - %Y/%m/%d"),
                        "expires": (datetime.datetime.now() + datetime.timedelta(hours=24)).isoformat()
                    }
                    mother["chats"][chat_key].append(msg_data)
                    data["mothers"] = madar_list
                    save_data(data)
                    st.success("✅ پیام ارسال شد!")
                    st.rerun()
            if st.button("🚪 خروج"):
                st.session_state.logged_in = False
                st.session_state.mother = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ================== پنل پزشک ==================
elif st.session_state.get("role") == "پزشک":
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("👨‍⚕️ پنل پزشک")
        if not st.session_state.get("logged_in"):
            general_code = st.text_input("کد عمومی پزشکان را وارد کنید:", type="password")
            if general_code == DOCTOR_GENERAL_CODE:
                st.success("✅ کد عمومی صحیح است!")
                doctor_code = st.text_input("کد اختصاصی خود را وارد کنید:", type="password")
                if st.button("ورود به پنل"):
                    found = None
                    for d in doctor_list:
                        if d["code"] == doctor_code:
                            found = d
                            break
                    if found:
                        st.session_state.doctor = found
                        st.session_state.logged_in = True
                        st.success("✅ ورود موفق!")
                        st.rerun()
                    else:
                        st.error("❌ کد اختصاصی نامعتبر است!")
            else:
                if general_code:
                    st.error("❌ کد عمومی اشتباه است!")
        else:
            doctor = st.session_state.doctor
            st.success(f"👋 خوش آمدید، {doctor['name']}!")
            
            st.subheader("🔐 رمزنگاری پیام")
            tab1, tab2 = st.tabs(["✉️ تبدیل پیام به کد", "🔓 تبدیل کد به پیام"])
            with tab1:
                msg = st.text_area("پیام خود را وارد کنید:")
                if st.button("ساخت کد"):
                    if msg:
                        code = ""
                        for char in msg:
                            code += ramz_kon(char) + " "
                        st.success("✅ کد شما ساخته شد!")
                        st.markdown(f'<div class="code-box">{code.strip()}</div>', unsafe_allow_html=True)
            with tab2:
                code_input = st.text_input("کد دریافتی را وارد کنید:")
                if st.button("رمزگشایی"):
                    if code_input:
                        parts = code_input.split()
                        message = ""
                        for part in parts:
                            message += ramz_baz(part)
                        st.success("✅ پیام اصلی:")
                        st.markdown(f'<div class="code-box">{message}</div>', unsafe_allow_html=True)
            
            st.subheader("📩 پیام‌های دریافتی")
            found_messages = False
            for mother in madar_list:
                for chat_key, msgs in mother.get("chats", {}).items():
                    if doctor["code"] in chat_key:
                        for msg in msgs:
                            if datetime.datetime.fromisoformat(msg['expires']) < datetime.datetime.now():
                                continue
                            found_messages = True
                            st.markdown(f"""
                            <div class="message-bubble received">
                                <div>👤 {msg['sender']}</div>
                                <div>{msg['text']}</div>
                                <div style="font-size: 0.7rem; opacity: 0.6;">{msg['time']}</div>
                            </div>
                            """, unsafe_allow_html=True)
            if not found_messages:
                st.info("📭 هیچ پیامی برای شما وجود ندارد.")
            if st.button("🚪 خروج"):
                st.session_state.logged_in = False
                st.session_state.doctor = None
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

# ================== پنل مدیریت ==================
else:
    with st.container():
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("⚙️ پنل مدیریت")
        admin_pass = st.text_input("رمز مدیریت:", type="password")
        if admin_pass == ADMIN_PASSWORD:
            st.success("✅ دسترسی مدیریت فعال شد!")
            tab1, tab2, tab3 = st.tabs(["➕ افزودن پزشک", "❌ حذف پزشک", "👨‍⚕️ لیست پزشکان"])
            with tab1:
                name = st.text_input("نام پزشک")
                hospital = st.text_input("بیمارستان")
                typ = st.selectbox("تخصص", ["زنان", "کودکان", "عمومی"])
                if st.button("افزودن"):
                    if name and hospital:
                        new_code = f"Dr{name.replace(' ', '')}2024"
                        doctor_list.append({"name": name, "hospital": hospital, "type": typ, "code": new_code})
                        data["doctors"] = doctor_list
                        save_data(data)
                        st.success("✅ پزشک اضافه شد!")
                        st.info(f"کد اختصاصی: {new_code}")
            with tab2:
                names = [doc["name"] for doc in doctor_list]
                if names:
                    selected = st.selectbox("انتخاب پزشک", names)
                    if st.button("حذف"):
                        doctor_list = [doc for doc in doctor_list if doc["name"] != selected]
                        data["doctors"] = doctor_list
                        save_data(data)
                        st.success("✅ حذف شد!")
            with tab3:
                for doc in doctor_list:
                    st.markdown(f"""
                    <div class="doctor-card">
                        <h3>{doc['name']}</h3>
                        <p>🏥 {doc['hospital']}</p>
                        <p>📋 {doc['type']}</p>
                        <p>🔑 کد: <code>{doc['code']}</code></p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            if admin_pass:
                st.error("❌ رمز اشتباه است!")
        st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div class="footer">
    ✨ <span class="highlight">ریاضی و پزشکی، با تکنولوژی به هم پیوند خوردند</span> ✨<br>
    <span style="font-size: 0.8rem; opacity: 0.6;">بر اساس نظریه مطابقت | © ۲۰۲۶</span>
</div>
""", unsafe_allow_html=True)
