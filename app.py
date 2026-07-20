import streamlit as st
import datetime
import random
import json
import os

# ================== تنظیمات صفحه ==================
st.set_page_config(
    page_title="مراقبت پس از زایمان",
    page_icon="🤱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ================== استایل CSS ==================
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    .custom-card {
        background: rgba(255, 255, 255, 0.85);
        backdrop-filter: blur(10px);
        border-radius: 20px;
        padding: 25px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        border: 1px solid rgba(255,255,255,0.3);
        margin: 10px 0;
        transition: all 0.3s ease;
    }
    .custom-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 15px 40px rgba(0,0,0,0.15);
    }
    .main-title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-shadow: none;
        margin-bottom: 20px;
    }
    .sub-title {
        text-align: center;
        font-size: 1.2rem;
        color: #555;
        margin-bottom: 30px;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 12px 30px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        width: 100%;
    }
    .stButton > button:hover {
        transform: scale(1.02);
        box-shadow: 0 6px 25px rgba(102, 126, 234, 0.6);
    }
    .stTextInput > div > div > input {
        border-radius: 30px !important;
        border: 2px solid #e0e0e0 !important;
        padding: 12px 20px !important;
        font-size: 16px !important;
        transition: all 0.3s ease !important;
        background: rgba(255,255,255,0.9) !important;
    }
    .stTextInput > div > div > input:focus {
        border-color: #667eea !important;
        box-shadow: 0 0 20px rgba(102, 126, 234, 0.2);
    }
    .doctor-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8f9ff 100%);
        border-radius: 15px;
        padding: 20px;
        margin: 10px 0;
        border-left: 5px solid #667eea;
        box-shadow: 0 4px 15px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    .doctor-card:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.1);
        transform: translateX(5px);
    }
    .code-box {
        background: #2d3436;
        color: #dfe6e9;
        padding: 15px 20px;
        border-radius: 15px;
        font-family: 'Courier New', monospace;
        font-size: 18px;
        letter-spacing: 2px;
        text-align: center;
        margin: 10px 0;
        box-shadow: inset 0 0 20px rgba(0,0,0,0.3);
    }
    .section-header {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2d3436;
        margin-bottom: 20px;
        padding-bottom: 10px;
        border-bottom: 3px solid #667eea;
        display: inline-block;
    }
    .footer {
        text-align: center;
        color: #888;
        font-size: 0.9rem;
        margin-top: 40px;
        padding: 20px;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# ================== عنوان ==================
st.markdown('<p class="main-title">🤱 مراقبت پس از زایمان</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-title">💜 همراه شما در دوران پس از زایمان</p>', unsafe_allow_html=True)

# ================== نظریه مطابقت ==================
SECRET_KEY = 137

def motabeghat(adad):
    b = 0
    u = 0
    if adad % 2 == 0:
        b = b + 1
    else:
        u = u + 1
    s = 0
    for d in str(adad):
        s = s + int(d)
    if s % 2 == 0:
        b = b + 1
    else:
        u = u + 1
    for i in range(1, int(s**0.5) + 1):
        if s % i == 0:
            jam = i + s // i
            if jam % 2 == 0:
                b = b + 1
            else:
                u = u + 1
    return b, u

def ramz_kon(harf):
    adad = ord(harf) + SECRET_KEY
    b, u = motabeghat(adad)
    return str(b) + "." + str(u)

def ramz_baz(ramz):
    b_str, u_str = ramz.split(".")
    b = int(b_str)
    u = int(u_str)
    for i in range(32, 127):
        bb, uu = motabeghat(i)
        if bb == b and uu == u:
            return chr(i - SECRET_KEY)
    return "؟"

def tarikh():
    return datetime.date.today() + datetime.timedelta(days=60)

def sakht_kod():
    kod = ""
    for _ in range(4):
        adad = random.randint(100, 999)
        b, u = motabeghat(adad)
        kod = kod + str(b) + "." + str(u) + " "
    return kod.strip()

# ================== ذخیره‌سازی ==================
DATA_FILE = "doctors.json"

def load_doctors():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return [
        {"name": "دکتر احمدی", "hospital": "بیمارستان فارابی", "type": "زنان", "code": sakht_kod()},
        {"name": "دکتر محمدی", "hospital": "بیمارستان قشم", "type": "کودکان", "code": sakht_kod()},
        {"name": "دکتر رضایی", "hospital": "بیمارستان خلیج فارس", "type": "زنان", "code": sakht_kod()}
    ]

def save_doctors(doctors):
    with open(DATA_FILE, "w") as f:
        json.dump(doctors, f)

doctor_list = load_doctors()
madar_list = []

# ================== رمز مدیر ==================
ADMIN_PASSWORD = "ahlat..mm666"

# ================== منو ==================
admin_password = st.sidebar.text_input("🔐 رمز مدیریت", type="password")
is_admin = (admin_password == ADMIN_PASSWORD)

if is_admin:
    option = st.sidebar.selectbox("📋 منو", [
        "🏠 صفحه اصلی",
        "👩 مادران",
        "👨‍⚕️ ورود پزشک",
        "👨‍⚕️ لیست پزشکان",
        "➕ افزودن پزشک",
        "✏️ ویرایش پزشک",
        "❌ حذف پزشک",
        "🔐 رمزنگاری پیام"
    ])
else:
    option = st.sidebar.selectbox("📋 منو", [
        "🏠 صفحه اصلی",
        "👩 مادران",
        "👨‍⚕️ ورود پزشک",
        "👨‍⚕️ لیست پزشکان",
        "🔐 رمزنگاری پیام"
    ])

# ================== صفحه اصلی ==================
if option == "🏠 صفحه اصلی":
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.write("💜 به برنامه مراقبت‌های پس از زایمان خوش آمدید!")
    st.write("این برنامه بر اساس **نظریه مطابقت**، یک کشف ریاضی جدید، طراحی شده است.")
    st.info("از منوی کناری گزینه مورد نظر را انتخاب کنید.")
    st.markdown('</div>', unsafe_allow_html=True)

# ================== مادران ==================
elif option == "👩 مادران":
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">👩 مادران</p>', unsafe_allow_html=True)
    
    st.subheader("🔑 ورود مادر")
    kod = st.text_input("کد خود را وارد کنید:")
    if st.button("ورود"):
        found = None
        for m in madar_list:
            if m["code"] == kod:
                found = m
                break
        if found:
            st.success(f"✅ خوش آمدید! تاریخ اعتبار: {tarikh()}")
        else:
            st.error("❌ کد نامعتبر است!")
    
    st.divider()
    st.subheader("📝 ثبت‌نام مادر جدید")
    name = st.text_input("نام مادر")
    if st.button("ثبت‌نام"):
        if name:
            new_code = sakht_kod()
            madar_list.append({"name": name, "code": new_code})
            st.success(f"✅ مادر ثبت شد!")
            st.markdown(f'<div class="code-box">کد شما: {new_code}</div>', unsafe_allow_html=True)
        else:
            st.error("❌ لطفاً نام را وارد کنید.")
    st.markdown('</div>', unsafe_allow_html=True)

# ================== ورود پزشک ==================
elif option == "👨‍⚕️ ورود پزشک":
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">👨‍⚕️ ورود پزشک</p>', unsafe_allow_html=True)
    
    doc_code = st.text_input("کد اختصاصی خود را وارد کنید:", type="password")
    if st.button("ورود"):
        found = None
        for d in doctor_list:
            if d["code"] == doc_code:
                found = d
                break
        if found:
            st.success(f"✅ خوش آمدید، {found['name']}!")
            st.info(f"🏥 بیمارستان: {found['hospital']}")
            st.info(f"📋 تخصص: {found['type']}")
            
            patients = [m for m in madar_list if m.get("zanan") == found["name"] or m.get("koodakan") == found["name"]]
            if patients:
                st.subheader("👥 بیماران شما:")
                for p in patients:
                    st.write(f"🆔 کد بیمار: {p['code']}")
            else:
                st.info("هنوز هیچ بیماری به شما اختصاص داده نشده است.")
        else:
            st.error("❌ کد نامعتبر!")
    st.markdown('</div>', unsafe_allow_html=True)

# ================== لیست پزشکان ==================
elif option == "👨‍⚕️ لیست پزشکان":
    st.markdown('<p class="section-header">👨‍⚕️ لیست پزشکان</p>', unsafe_allow_html=True)
    if not doctor_list:
        st.warning("هیچ پزشکی ثبت نشده است.")
    for doc in doctor_list:
        st.markdown(f"""
        <div class="doctor-card">
            <h3>{doc['name']}</h3>
            <p>🏥 {doc['hospital']}</p>
            <p>📋 {doc['type']}</p>
            <p>🔑 کد: <code>{doc['code']}</code></p>
        </div>
        """, unsafe_allow_html=True)

# ================== افزودن پزشک ==================
elif option == "➕ افزودن پزشک":
    if not is_admin:
        st.error("❌ شما اجازه دسترسی به این بخش را ندارید.")
    else:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-header">➕ افزودن پزشک جدید</p>', unsafe_allow_html=True)
        name = st.text_input("نام پزشک")
        hospital = st.text_input("بیمارستان")
        typ = st.selectbox("تخصص", ["زنان", "کودکان", "عمومی"])
        if st.button("افزودن"):
            if name and hospital:
                doctor_list.append({"name": name, "hospital": hospital, "type": typ, "code": sakht_kod()})
                save_doctors(doctor_list)
                st.success("✅ پزشک با موفقیت اضافه شد!")
            else:
                st.error("❌ لطفاً همه فیلدها را پر کنید!")
        st.markdown('</div>', unsafe_allow_html=True)

# ================== ویرایش پزشک ==================
elif option == "✏️ ویرایش پزشک":
    if not is_admin:
        st.error("❌ شما اجازه دسترسی به این بخش را ندارید.")
    else:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-header">✏️ ویرایش اطلاعات پزشک</p>', unsafe_allow_html=True)
        names = [doc["name"] for doc in doctor_list]
        if names:
            selected = st.selectbox("انتخاب پزشک", names)
            for doc in doctor_list:
                if doc["name"] == selected:
                    new_hospital = st.text_input("بیمارستان جدید", doc["hospital"])
                    new_type = st.selectbox("تخصص جدید", ["زنان", "کودکان", "عمومی"], index=["زنان", "کودکان", "عمومی"].index(doc["type"]))
                    if st.button("ذخیره تغییرات"):
                        doc["hospital"] = new_hospital
                        doc["type"] = new_type
                        save_doctors(doctor_list)
                        st.success("✅ اطلاعات به‌روز شد!")
                    break
        else:
            st.warning("هیچ پزشکی وجود ندارد!")
        st.markdown('</div>', unsafe_allow_html=True)

# ================== حذف پزشک ==================
elif option == "❌ حذف پزشک":
    if not is_admin:
        st.error("❌ شما اجازه دسترسی به این بخش را ندارید.")
    else:
        st.markdown('<div class="custom-card">', unsafe_allow_html=True)
        st.markdown('<p class="section-header">❌ حذف پزشک</p>', unsafe_allow_html=True)
        names = [doc["name"] for doc in doctor_list]
        if names:
            selected = st.selectbox("انتخاب پزشک برای حذف", names)
            if st.button("حذف"):
                doctor_list = [doc for doc in doctor_list if doc["name"] != selected]
                save_doctors(doctor_list)
                st.success(f"✅ پزشک {selected} حذف شد!")
        else:
            st.warning("هیچ پزشکی وجود ندارد!")
        st.markdown('</div>', unsafe_allow_html=True)

# ================== رمزنگاری پیام ==================
elif option == "🔐 رمزنگاری پیام":
    st.markdown('<div class="custom-card">', unsafe_allow_html=True)
    st.markdown('<p class="section-header">🔐 رمزنگاری پیام</p>', unsafe_allow_html=True)
    
    st.subheader("✉️ مادر: تبدیل پیام به کد")
    msg = st.text_input("پیام خود را وارد کنید (فارسی یا انگلیسی):")
    if st.button("ساخت کد"):
        if msg:
            code = ""
            for char in msg:
                code += ramz_kon(char) + " "
            st.success(f"✅ کد شما ساخته شد!")
            st.markdown(f'<div class="code-box">{code.strip()}</div>', unsafe_allow_html=True)
            st.info("📋 این کد را به پزشک خود بدهید.")
        else:
            st.error("❌ لطفاً پیام را وارد کنید.")
    
    st.divider()
    st.subheader("🔓 پزشک: تبدیل کد به پیام")
    code_input = st.text_input("کد دریافتی از مادر را وارد کنید (مثلاً 1.2 3.4):")
    if st.button("رمزگشایی"):
        if code_input:
            parts = code_input.split()
            message = ""
            for part in parts:
                message += ramz_baz(part)
            st.success(f"✅ پیام اصلی:")
            st.markdown(f'<div class="code-box" style="background: #2d3436; color: #dfe6e9;">{message}</div>', unsafe_allow_html=True)
        else:
            st.error("❌ لطفاً کد را وارد کنید.")
    st.markdown('</div>', unsafe_allow_html=True)

# ================== فوتر ==================
st.markdown("""
<div class="footer">
    💜 این برنامه بر اساس نظریه مطابقت طراحی شده است<br>
    © ۲۰۲۶ - تمامی حقوق محفوظ است
</div>
""", unsafe_allow_html=True)
