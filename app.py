import streamlit as st
import datetime
import random
import json
import os
import base64
import io
from PIL import Image

st.set_page_config(page_title="مراقبت پس از زایمان", page_icon="🌸", layout="wide")

st.markdown("""
<style>
    * { font-family: Tahoma, sans-serif; }
    .stApp { background: #f0f2f6; }
    .main-title { text-align: center; font-size: 3rem; font-weight: bold; color: #2d3436; }
    .glass-card { background: white; border-radius: 20px; padding: 20px; box-shadow: 0 4px 12px rgba(0,0,0,0.1); margin-bottom: 20px; }
    .role-btn { background: #e0e0e0; border-radius: 30px; padding: 10px 20px; text-align: center; cursor: pointer; }
    .role-btn:hover { background: #d0d0d0; }
    .code-box { background: #f8f9fa; padding: 10px; border-radius: 10px; text-align: center; border: 1px solid #ddd; }
    .doctor-card { background: #f8f9fa; padding: 15px; border-radius: 15px; margin: 10px 0; border-left: 4px solid #2d3436; }
    .chat-container { background: #f8f9fa; border-radius: 15px; padding: 15px; max-height: 350px; overflow-y: auto; }
    .message-bubble { background: white; border-radius: 15px; padding: 10px 15px; margin: 8px 0; max-width: 80%; }
    .message-bubble.sent { background: #2d3436; color: white; margin-left: auto; }
    .message-bubble.received { background: #e9ecef; margin-right: auto; }
    .footer { text-align: center; color: #636e72; margin-top: 40px; padding: 20px; border-top: 1px solid #ddd; }
    .footer .highlight { font-weight: bold; color: #2d3436; }
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

def sakht_kod():
    kod = ""
    for _ in range(4):
        adad = random.randint(100, 999)
        b, u = motabeghat(adad)
        kod += str(b) + "." + str(u) + " "
    return kod.strip()

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

if st.session_state.get("role") == "مادر":
    with st.container():
        st.subheader("👩 پنل مادر")
        if not st.session_state.get("logged_in"):
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
        else:
            mother = st.session_state.mother
            st.success(f"👋 خوش آمدید، {mother['name']}!")
            doctor_codes = [doc["code"] for doc in doctor_list]
            target_doctor = st.selectbox("پزشک مورد نظر:", doctor_codes)
            chat_key = f"chat_{target_doctor}"
            if chat_key not in mother.get("chats", {}):
                mother["chats"][chat_key] = []
            with st.container():
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

elif st.session_state.get("role") == "پزشک":
    with st.container():
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

else:
    with st.container():
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

st.markdown("""
<div class="footer">
    ✨ <span class="highlight">ریاضی و پزشکی، با تکنولوژی به هم پیوند خوردند</span> ✨<br>
    <span style="font-size: 0.8rem; opacity: 0.6;">بر اساس نظریه مطابقت | © ۲۰۲۶</span>
</div>
""", unsafe_allow_html=True)
