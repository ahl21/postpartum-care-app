import streamlit as st
import datetime
import random
import json
import os
import base64
import io
from PIL import Image

# ================== تنظیمات صفحه ==================
st.set_page_config(
    page_title="مراقبت پس از زایمان",
    page_icon="🌸",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================== استایل جدید ==================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;700;900&display=swap');
    
    * {
        font-family: 'Vazirmatn', Tahoma, sans-serif;
    }
    
    .stApp {
        background: linear-gradient(145deg, #f8f9fc 0%, #e9ecef 100%);
    }
    
    .main-container {
        max-width: 1200px;
        margin: 0 auto;
        padding: 20px;
    }
    
    .glass-card {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border-radius: 40px;
        padding: 25px;
        border: 1px solid rgba(255, 255, 255, 0.5);
        box-shadow: 0 20px 50px rgba(0,0,0,0.05), inset 0 0 80px rgba(255,255,255,0.3);
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    
    .glass-card:hover {
        box-shadow: 0 25px 60px rgba(0,0,0,0.08);
    }
    
    .main-title {
        text-align: center;
        font-size: 3.2rem;
        font-weight: 900;
        background: linear-gradient(135deg, #2d3436 0%, #636e72 50%, #b2bec3 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none;
        letter-spacing: 2px;
        margin-bottom: 5px;
    }
    
    .sub-title {
        text-align: center;
        color: #636e72;
        font-size: 1.1rem;
        font-weight: 300;
        margin-bottom: 20px;
        letter-spacing: 1px;
    }
    
    .warning-box {
        background: rgba(255, 215, 0, 0.08);
        border: 1px solid rgba(255, 215, 0, 0.15);
        border-radius: 20px;
        padding: 12px 20px;
        color: #b7950b;
        text-align: center;
        font-size: 0.9rem;
        backdrop-filter: blur(10px);
    }
    
    .role-selector {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 15px 0;
        flex-wrap: wrap;
    }
    
    .role-btn {
        background: rgba(255,255,255,0.5);
        border: 1.5px solid rgba(0,0,0,0.05);
        border-radius: 30px;
        padding: 12px 30px;
        color: #2d3436;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        min-width: 120px;
        backdrop-filter: blur(5px);
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    
    .role-btn:hover {
        background: rgba(255,255,255,0.8);
        transform: translateY(-3px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    .role-btn.active {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        color: white;
        border-color: #2d3436;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    
    .code-box {
        background: rgba(0,0,0,0.03);
        color: #2d3436;
        padding: 12px 20px;
        border-radius: 20px;
        font-family: 'Vazirmatn', monospace;
        font-size: 1.1rem;
        text-align: center;
        margin: 10px 0;
        border: 1px solid rgba(0,0,0,0.05);
        backdrop-filter: blur(5px);
    }
    
    .doctor-card {
        background: rgba(255,255,255,0.5);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 15px 20px;
        margin: 10px 0;
        border-left: 4px solid #636e72;
        transition: all 0.3s ease;
    }
    
    .doctor-card:hover {
        background: rgba(255,255,255,0.8);
        transform: translateX(5px);
    }
    
    .doctor-card h3 {
        color: #2d3436;
        margin: 0 0 5px 0;
        font-weight: 700;
    }
    
    .doctor-card p {
        color: #636e72;
        margin: 3px 0;
        font-weight: 300;
    }
    
    .chat-container {
        background: rgba(0,0,0,0.02);
        border-radius: 25px;
        padding: 15px;
        max-height: 350px;
        overflow-y: auto;
        border: 1px solid rgba(0,0,0,0.03);
    }
    
    .message-bubble {
        background: rgba(255,255,255,0.6);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 12px 18px;
        margin: 8px 0;
        max-width: 80%;
        color: #2d3436;
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 4px 15px rgba(0,0,0,0.02);
    }
    
    .message-bubble.sent {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        color: white;
        margin-left: auto;
        border: none;
    }
    
    .message-bubble.received {
        background: rgba(255,255,255,0.8);
        margin-right: auto;
        border: 1px solid rgba(0,0,0,0.03);
    }
    
    .message-bubble .time {
        font-size: 0.6rem;
        opacity: 0.5;
        margin-top: 5px;
        font-weight: 300;
    }
    
    .message-bubble .expiry-badge {
        background: rgba(255, 215, 0, 0.1);
        border: 1px solid rgba(255, 215, 0, 0.1);
        border-radius: 10px;
        padding: 2px 10px;
        font-size: 0.6rem;
        color: #b7950b;
        display: inline-block;
        margin-top: 5px;
    }
    
    .input-area {
        background: rgba(255,255,255,0.5);
        backdrop-filter: blur(10px);
        border-radius: 25px;
        padding: 10px 15px;
        margin-top: 15px;
        display: flex;
        gap: 10px;
        align-items: center;
        flex-wrap: wrap;
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .input-area input, .input-area textarea {
        flex: 1;
        background: rgba(255,255,255,0.7);
        border: 1px solid rgba(0,0,0,0.03);
        border-radius: 20px;
        padding: 10px 15px;
        color: #2d3436;
        font-size: 0.95rem;
        min-width: 150px;
        font-family: 'Vazirmatn', sans-serif;
    }
    
    .input-area input::placeholder, .input-area textarea::placeholder {
        color: #b2bec3;
    }
    
    .input-area button {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        border: none;
        border-radius: 20px;
        padding: 10px 25px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
        font-family: 'Vazirmatn', sans-serif;
    }
    
    .input-area button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(0,0,0,0.05);
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 10px 25px !important;
        font-weight: 600 !important;
        width: 100%;
        font-family: 'Vazirmatn', sans-serif !important;
        transition: all 0.3s ease !important;
    }
    
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 10px 30px rgba(0,0,0,0.05) !important;
    }
    
    .footer {
        text-align: center;
        color: #b2bec3;
        font-size: 0.9rem;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid rgba(0,0,0,0.02);
        font-weight: 300;
        letter-spacing: 1px;
        direction: rtl;
    }
    
    .footer .highlight {
        background: linear-gradient(135deg, #2d3436 0%, #636e72 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
    }
    
    ::-webkit-scrollbar {
        width: 6px;
    }
    ::-webkit-scrollbar-track {
        background: rgba(0,0,0,0.02);
        border-radius: 10px;
    }
    ::-webkit-scrollbar-thumb {
        background: #b2bec3;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# ================== نظریه مطابقت ==================
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

def sakht_kod():
    kod = ""
    for _ in range(4):
        adad = random.randint(100, 999)
        b, u = motabeghat(adad)
        kod += str(b) + "." + str(u) + " "
    return kod.strip()

def tarikh():
    return datetime.date.today() + datetime.timedelta(days=60)

# ================== ذخیره‌سازی ==================
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
messages = data["messages"]

ADMIN_PASSWORD = "ahlat..mm666"
DOCTOR_GENERAL_CODE = "752*36+9"

# ================== عنوان ==================
st.markdown('<div class="main-container">', unsafe_allow_html=True)
st.markdown('<p class="main-title">🌸 مراقبت پس از زایمان</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">💜 همراه شما در دوران پس از زایمان</p>', unsafe_allow_html=True)

# ================== انتخاب نقش ==================
st.markdown('<div class="glass-card">', unsafe_allow_html=True)
st.markdown('<div class="role-selector">', unsafe_allow_html=True)

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

st.markdown('</div>', unsafe_allow_html=True)

# ================== هشدار ==================
st.markdown("""
<div class="warning-box">
    🔒 <strong>هشدار امنیتی:</strong> برای ورود به هر بخش، به کد اختصاصی خود نیاز دارید. 
    کد خود را محرمانه نگه دارید.
</div>
""", unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

# ================== پنل مادر ==================
if st.session_state.get("role") == "مادر":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("👩 پنل مادر")
    
    if not st.session_state.get("logged_in"):
        st.info("⚠️ برای ورود، کد اختصاصی خود را وارد کنید. اگر کد ندارید، ثبت‌نام کنید.")
        kod = st.text_input("کد خود را وارد کنید:", type="password")
        if st.button("ورود"):
            found = None
            for m in madar_list:
                if m["code"] == kod:
                    found = m
                    break
            if found:
                st.session_state.mother = found
                st.session_state.logged_in = True
                st.success("✅ ورود موفق!")
                st.rerun()
            else:
                st.error("❌ کد نامعتبر است!")
        
        st.divider()
        st.subheader("📝 ثبت‌نام مادر جدید")
        name = st.text_input("نام مادر")
        if st.button("ثبت‌نام"):
            if name:
                new_code = sakht_kod()
                new_mother = {"name": name, "code": new_code, "chats": {}}
                madar_list.append(new_mother)
                data["mothers"] = madar_list
                save_data(data)
                st.success("✅ ثبت‌نام موفق!")
                st.markdown(f'<div class="code-box">کد شما: {new_code}</div>', unsafe_allow_html=True)
                st.warning("⚠️ این کد را ذخیره کنید.")
    else:
        mother = st.session_state.mother
        st.success(f"👋 خوش آمدید، {mother['name']}!")
        
        doctor_codes = [doc["code"] for doc in doctor_list]
        target_doctor = st.selectbox("پزشک مورد نظر:", doctor_codes)
        
        chat_key = f"chat_{target_doctor}"
        if chat_key not in mother.get("chats", {}):
            if "chats" not in mother:
                mother["chats"] = {}
            mother["chats"][chat_key] = []
        
        st.markdown('<div class="chat-container">', unsafe_allow_html=True)
        for msg in mother["chats"][chat_key]:
            if datetime.datetime.fromisoformat(msg['expires']) < datetime.datetime.now():
                continue
            st.markdown(f"""
            <div class="message-bubble {'sent' if msg['sender'] == mother['name'] else 'received'}">
                <div>{msg['text']}</div>
                <div class="time">{msg['time']}</div>
                <div class="expiry-badge">⏳ {msg['expires']}</div>
            </div>
            """, unsafe_allow_html=True)
            if "image" in msg:
                st.image(base64.b64decode(msg["image"]), caption="عکس ارسالی")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="input-area">', unsafe_allow_html=True)
        new_msg = st.text_input("پیام خود را بنویسید:", key="mother_msg", placeholder="متن پیام...")
        uploaded_file = st.file_uploader("انتخاب عکس", type=["jpg", "jpeg", "png"], key="mother_photo")
        if st.button("ارسال پیام"):
            if new_msg or uploaded_file:
                msg_data = {
                    "sender": mother['name'],
                    "text": new_msg or "(عکس)",
                    "time": datetime.datetime.now().strftime("%H:%M - %Y/%m/%d"),
                    "expires": (datetime.datetime.now() + datetime.timedelta(hours=24)).isoformat()
                }
                if uploaded_file:
                    image = Image.open(uploaded_file)
                    img_byte_arr = io.BytesIO()
                    image.save(img_byte_arr, format='PNG')
                    img_base64 = base64.b64encode(img_byte_arr.getvalue()).decode()
                    msg_data["image"] = img_base64
                mother["chats"][chat_key].append(msg_data)
                data["mothers"] = madar_list
                save_data(data)
                st.success("✅ پیام ارسال شد!")
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
        
        if st.button("🚪 خروج"):
            st.session_state.logged_in = False
            st.session_state.mother = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================== پنل پزشک ==================
elif st.session_state.get("role") == "پزشک":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("👨‍⚕️ پنل پزشک")
    
    if not st.session_state.get("logged_in"):
        st.info("⚠️ ابتدا کد عمومی و سپس کد اختصاصی خود را وارد کنید.")
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
                            <div class="time">{msg['time']}</div>
                            <div class="expiry-badge">⏳ {msg['expires']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                        if "image" in msg:
                            st.image(base64.b64decode(msg["image"]), caption="عکس دریافتی")
        if not found_messages:
            st.info("📭 هیچ پیامی برای شما وجود ندارد.")
        
        if st.button("🚪 خروج"):
            st.session_state.logged_in = False
            st.session_state.doctor = None
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================== پنل مدیریت ==================
else:
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
                </
