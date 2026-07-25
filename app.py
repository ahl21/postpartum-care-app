import streamlit as st
import datetime
import random
import json
import os
import re

st.set_page_config(page_title="حمایت از مادران", page_icon="🌸", layout="wide")

# ================== تصویر صفحه اصلی ==================
st.image("https://cdn.pixabay.com/photo/2020/05/30/19/29/mother-5240383_960_720.jpg", width=300)

st.markdown('<p class="main-title">🌸 حمایت از مادران</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">💜 همراه شما در دوران پس از زایمان</p>', unsafe_allow_html=True)

# ================== جدول کدهای اختصاصی حروف فارسی ==================
PERSIAN_ALPHABET = {
    "ا": {"id": "A", "signature": (1, 2)},
    "ب": {"id": "B", "signature": (2, 1)},
    "پ": {"id": "P", "signature": (1, 2)},
    "ت": {"id": "T", "signature": (3, 1)},
    "ث": {"id": "TH", "signature": (1, 2)},
    "ج": {"id": "J", "signature": (2, 2)},
    "چ": {"id": "CH", "signature": (1, 2)},
    "ح": {"id": "H", "signature": (3, 1)},
    "خ": {"id": "KH", "signature": (2, 1)},
    "د": {"id": "D", "signature": (2, 1)},
    "ذ": {"id": "Z", "signature": (1, 2)},
    "ر": {"id": "R", "signature": (2, 1)},
    "ز": {"id": "ZH", "signature": (2, 2)},
    "ژ": {"id": "JZ", "signature": (2, 1)},
    "س": {"id": "S", "signature": (1, 3)},
    "ش": {"id": "SH", "signature": (2, 1)},
    "ص": {"id": "SAD", "signature": (2, 2)},
    "ض": {"id": "ZAD", "signature": (3, 1)},
    "ط": {"id": "TA", "signature": (1, 3)},
    "ظ": {"id": "ZA", "signature": (2, 1)},
    "ع": {"id": "EIN", "signature": (1, 2)},
    "غ": {"id": "GHEIN", "signature": (3, 1)},
    "ف": {"id": "F", "signature": (1, 2)},
    "ق": {"id": "GH", "signature": (2, 2)},
    "ک": {"id": "K", "signature": (1, 2)},
    "گ": {"id": "G", "signature": (3, 1)},
    "ل": {"id": "L", "signature": (2, 1)},
    "م": {"id": "M", "signature": (2, 2)},
    "ن": {"id": "N", "signature": (1, 2)},
    "و": {"id": "V", "signature": (2, 1)},
    "ه": {"id": "HE", "signature": (2, 2)},
    "ی": {"id": "Y", "signature": (2, 1)}
}

# ================== توابع رمزنگاری بر اساس جدول اختصاصی ==================
def ramz_kon(harf):
    """تبدیل حرف فارسی به کد اختصاصی (مثلاً ا → A1,2)"""
    if harf in PERSIAN_ALPHABET:
        info = PERSIAN_ALPHABET[harf]
        harf_id = info["id"]
        b, u = info["signature"]
        # انتخاب جداکننده بر اساس مقادیر b و u
        if b > u:
            sep = "."
        elif b < u:
            sep = ","
        else:
            sep = "ـ"
        return f"{harf_id}{b}{sep}{u}"
    return harf

def ramz_baz(ramz):
    """تبدیل کد اختصاصی به حرف فارسی (مثلاً A1,2 → ا)"""
    try:
        # الگوی کد: حرف انگلیسی + عدد + جداکننده + عدد
        match = re.match(r"([A-Z]+)(\d+)([.,ـ])(\d+)", ramz)
        if match:
            harf_id = match.group(1)
            b = int(match.group(2))
            u = int(match.group(4))
            for harf, info in PERSIAN_ALPHABET.items():
                if info["id"] == harf_id and info["signature"] == (b, u):
                    return harf
        return "؟"
    except:
        return "❗"

def encode_message(msg):
    """تبدیل پیام کامل به کدهای اختصاصی"""
    code_parts = []
    for char in msg:
        if char in PERSIAN_ALPHABET:
            code_parts.append(ramz_kon(char))
        else:
            code_parts.append(char)
    return " ".join(code_parts)

def decode_message(code):
    """تبدیل کدهای اختصاصی به پیام اصلی"""
    parts = code.split()
    message = ""
    for part in parts:
        decoded = ramz_baz(part)
        message += decoded if decoded != "?" else part
    return message

# ================== ذخیره‌سازی با JSON ==================
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

def sakht_kod_madar():
    return f"M-{random.randint(10000, 99999)}"

def tarikh():
    return datetime.date.today() + datetime.timedelta(days=60)

# ================== استایل ==================
st.markdown("""
<style>
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: bold;
        color: #4a148c;
    }
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #636e72;
    }
    .glass-card {
        background: rgba(255,255,255,0.8);
        border-radius: 30px;
        padding: 25px;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .code-box {
        background: #f8f9fa;
        padding: 10px;
        border-radius: 15px;
        text-align: center;
        border: 2px solid #f06292;
        font-family: monospace;
        font-size: 1.2rem;
    }
</style>
""", unsafe_allow_html=True)

# ================== منو ==================
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
            
            st.subheader("🔐 رمزنگاری پیام (بر اساس کدهای اختصاصی)")
            tab1, tab2 = st.tabs(["✉️ تبدیل پیام به کد", "🔓 تبدیل کد به پیام"])
            with tab1:
                msg = st.text_area("پیام خود را وارد کنید (فارسی یا انگلیسی):")
                if st.button("ساخت کد"):
                    if msg:
                        code = encode_message(msg)
                        st.success("✅ کد شما ساخته شد!")
                        st.markdown(f'<div class="code-box">{code}</div>', unsafe_allow_html=True)
            with tab2:
                code_input = st.text_input("کد دریافتی را وارد کنید:")
                if st.button("رمزگشایی"):
                    if code_input:
                        message = decode_message(code_input)
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
            
            st.subheader("🔐 رمزنگاری پیام (بر اساس کدهای اختصاصی)")
            tab1, tab2 = st.tabs(["✉️ تبدیل پیام به کد", "🔓 تبدیل کد به پیام"])
            with tab1:
                msg = st.text_area("پیام خود را وارد کنید (فارسی یا انگلیسی):")
                if st.button("ساخت کد"):
                    if msg:
                        code = encode_message(msg)
                        st.success("✅ کد شما ساخته شد!")
                        st.markdown(f'<div class="code-box">{code}</div>', unsafe_allow_html=True)
            with tab2:
                code_input = st.text_input("کد دریافتی را وارد کنید:")
                if st.button("رمزگشایی"):
                    if code_input:
                        message = decode_message(code_input)
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
            
            st.subheader("🖼️ تغییر تصویر پس‌زمینه")
            new_image_url = st.text_input("لینک تصویر جدید را وارد کنید:")
            if st.button("تغییر تصویر"):
                if new_image_url:
                    st.markdown(f"""
                    <style>
                        .stApp {{
                            background: linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.85)),
                                        url('{new_image_url}');
                            background-size: cover;
                            background-position: center;
                            background-attachment: fixed;
                        }}
                    </style>
                    """, unsafe_allow_html=True)
                    st.success("✅ تصویر پس‌زمینه تغییر کرد!")
            
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
