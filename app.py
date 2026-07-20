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
    page_icon="🤱",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ================== استایل ==================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
    }
    .glass-card {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(15px);
        border-radius: 30px;
        padding: 30px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 25px 50px rgba(0,0,0,0.3);
        margin-bottom: 20px;
    }
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 50%, #4facfe 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .sub-title {
        text-align: center;
        color: rgba(255,255,255,0.7);
        font-size: 1.1rem;
        margin-bottom: 30px;
    }
    .warning-box {
        background: rgba(255, 59, 48, 0.1);
        border: 1px solid rgba(255, 59, 48, 0.3);
        border-radius: 15px;
        padding: 15px;
        color: #ff3b30;
        text-align: center;
        margin: 10px 0;
    }
    .role-selector {
        display: flex;
        justify-content: center;
        gap: 15px;
        margin: 20px 0;
    }
    .role-btn {
        background: rgba(255,255,255,0.1);
        border: 2px solid rgba(255,255,255,0.2);
        border-radius: 20px;
        padding: 12px 30px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .role-btn:hover {
        background: rgba(255,255,255,0.2);
    }
    .role-btn.active {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border-color: #f5576c;
    }
    .code-box {
        background: #2d3436;
        color: #dfe6e9;
        padding: 15px 20px;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        font-size: 18px;
        text-align: center;
        margin: 10px 0;
    }
    .doctor-card {
        background: rgba(255,255,255,0.05);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-left: 4px solid #f5576c;
    }
    .chat-container {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 20px;
        max-height: 400px;
        overflow-y: auto;
        border: 1px solid rgba(255,255,255,0.1);
    }
    .message-bubble {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        padding: 12px;
        margin: 8px 0;
        max-width: 80%;
        color: white;
    }
    .message-bubble.sent {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        margin-left: auto;
    }
    .message-bubble.received {
        background: rgba(255,255,255,0.15);
        margin-right: auto;
    }
    .message-bubble .time {
        font-size: 0.7rem;
        opacity: 0.7;
        margin-top: 5px;
    }
    .message-bubble .image-container img {
        max-width: 200px;
        border-radius: 10px;
        margin-top: 10px;
        border: 1px solid rgba(255,255,255,0.2);
    }
    .expiry-badge {
        background: rgba(255, 59, 48, 0.2);
        border: 1px solid rgba(255, 59, 48, 0.3);
        border-radius: 10px;
        padding: 4px 12px;
        font-size: 0.7rem;
        color: #ff3b30;
    }
    .input-area {
        background: rgba(255,255,255,0.05);
        border-radius: 20px;
        padding: 10px;
        margin-top: 15px;
        display: flex;
        gap: 10px;
        align-items: center;
        flex-wrap: wrap;
    }
    .input-area input, .input-area textarea {
        flex: 1;
        background: rgba(255,255,255,0.1);
        border: 1px solid rgba(255,255,255,0.2);
        border-radius: 15px;
        padding: 12px 20px;
        color: white;
        font-size: 1rem;
        min-width: 200px;
    }
    .input-area input::placeholder, .input-area textarea::placeholder {
        color: rgba(255,255,255,0.5);
    }
    .input-area button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        border: none;
        border-radius: 15px;
        padding: 12px 25px;
        color: white;
        font-weight: 600;
        cursor: pointer;
        transition: all 0.3s ease;
    }
    .input-area button:hover {
        transform: scale(1.05);
    }
    .stButton > button {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 30px !important;
        font-weight: 600 !important;
        width: 100%;
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
st.markdown('</div>', unsafe_allow_html=True)

# ================== هشدار امنیتی ==================
st.markdown("""
<div class="warning-box">
    🔒 <strong>هشدار امنیتی:</strong> برای ورود به هر بخش، به کد اختصاصی خود نیاز دارید. 
    کد خود را محرمانه نگه دارید و در اختیار دیگران قرار ندهید.
</div>
""", unsafe_allow_html=True)

# ================== پنل مادر ==================
if st.session_state.get("role") == "مادر":
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("👩 پنل مادر")
    
    if not st.session_state.get("logged_in"):
        st.markdown("""
        <div style="background: rgba(255, 193, 7, 0.1); border: 1px solid rgba(255, 193, 7, 0.3); border-radius: 15px; padding: 15px; color: #ffc107; text-align: center;">
            ⚠️ برای ورود به پنل مادر، لطفاً کد اختصاصی خود را وارد کنید. 
            اگر کد ندارید، ابتدا در بخش "ثبت‌نام" ثبت‌نام کنید.
        </div>
        """, unsafe_allow_html=True)
        
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
                st.success("✅ ورود موفق! خوش آمدید.")
                st.rerun()
            else:
                st.error("❌ کد نامعتبر است! لطفاً ابتدا ثبت‌نام کنید.")
        
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
                st.warning("⚠️ این کد را ذخیره کنید. برای هر بار ورود به آن نیاز دارید.")
    else:
        mother = st.session_state.mother
        st.success(f"👋 خوش آمدید، {mother['name']}!")
        st.info("📋 برای مشاهده پیام‌ها و ارسال پیام، از بخش زیر استفاده کنید.")
        
        # انتخاب پزشک
        doctor_codes = [doc["code"] for doc in doctor_list]
        target_doctor = st.selectbox("پزشک مورد نظر:", doctor_codes)
        
        # چت
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
        
        # ارسال پیام
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
        st.markdown("""
        <div style="background: rgba(255, 193, 7, 0.1); border: 1px solid rgba(255, 193, 7, 0.3); border-radius: 15px; padding: 15px; color: #ffc107; text-align: center;">
            ⚠️ برای ورود به پنل پزشک، ابتدا کد عمومی و سپس کد اختصاصی خود را وارد کنید.
            این کدها از طرف مدیریت در اختیار شما قرار گرفته است.
        </div>
        """, unsafe_allow_html=True)
        
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
                    st.success("✅ ورود موفق! خوش آمدید.")
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
                </div>
                """, unsafe_allow_html=True)
    else:
        if admin_pass:
            st.error("❌ رمز اشتباه است!")
    
    st.markdown('</div>', unsafe_allow_html=True)

# ================== فوتر ==================
st.markdown("""
<div style="text-align: center; color: rgba(255,255,255,0.2); font-size: 0.8rem; margin-top: 40px; padding: 20px;">
    💜 این برنامه بر اساس نظریه مطابقت طراحی شده است<br>
    © ۲۰۲۶ - تمامی حقوق محفوظ است
</div>
""", unsafe_allow_html=True)
