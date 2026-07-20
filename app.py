import streamlit as st
import datetime
import random

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

if 'doctor_list' not in st.session_state:
    st.session_state.doctor_list = [
        {"name": "Dr.Ahmadi", "hospital": "Farabi Hospital", "type": "زنان", "code": sakht_kod()},
        {"name": "Dr.Mohamadi", "hospital": "Qeshm Hospital", "type": "کودکان", "code": sakht_kod()},
        {"name": "Dr.Rezaei", "hospital": "khalij Fars Hospital", "type": "زنان", "code": sakht_kod()}
    ]

if 'madar_list' not in st.session_state:
    st.session_state.madar_list = []

st.set_page_config(page_title="مراقبت پس از زایمان", page_icon="🤱")
st.title("🤱 مراقبت پس از زایمان")

menu = st.sidebar.selectbox(
    "📋 منو",
    ["🏠 صفحه اصلی", "👩 مادران", "👨‍⚕️ لیست پزشکان", "➕ افزودن پزشک",
     "✏️ ویرایش پزشک", "❌ حذف پزشک", "🔐 رمزنگاری پیام"]
)

if menu == "🏠 صفحه اصلی":
    st.write("به برنامه مراقبت‌های پس از زایمان خوش آمدید!")
    st.info("از منوی کناری گزینه مورد نظر را انتخاب کنید.")

elif menu == "👩 مادران":
    st.subheader("👩 ورود مادر")
    kod = st.text_input("کد خود را وارد کنید:")
    if st.button("ورود"):
        found = None
        for m in st.session_state.madar_list:
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
            st.session_state.madar_list.append({"name": name, "code": new_code})
            st.success(f"✅ مادر ثبت شد! کد: `{new_code}`")
        else:
            st.error("❌ لطفاً نام را وارد کنید.")

elif menu == "👨‍⚕️ لیست پزشکان":
    st.subheader("👨‍⚕️ لیست پزشکان")
    if not st.session_state.doctor_list:
        st.warning("هیچ پزشکی ثبت نشده است.")
    for doc in st.session_state.doctor_list:
        with st.container():
            st.write(f"**{doc['name']}**")
            st.write(f"🏥 {doc['hospital']}")
            st.write(f"📋 {doc['type']}")
            st.write(f"🔑 کد: `{doc['code']}`")
            st.divider()

elif menu == "➕ افزودن پزشک":
    st.subheader("➕ افزودن پزشک جدید")
    name = st.text_input("نام پزشک")
    hospital = st.text_input("بیمارستان")
    typ = st.selectbox("تخصص", ["زنان", "کودکان", "عمومی"])
    if st.button("افزودن"):
        if name and hospital:
            new_doc = {
                "name": name,
                "hospital": hospital,
                "type": typ,
                "code": sakht_kod()
            }
            st.session_state.doctor_list.append(new_doc)
            st.success(f"✅ پزشک {name} با موفقیت اضافه شد!")
        else:
            st.error("❌ لطفاً همه فیلدها را پر کنید!")

elif menu == "✏️ ویرایش پزشک":
    st.subheader("✏️ ویرایش اطلاعات پزشک")
    names = [doc["name"] for doc in st.session_state.doctor_list]
    if names:
        selected = st.selectbox("انتخاب پزشک", names)
        for doc in st.session_state.doctor_list:
            if doc["name"] == selected:
                new_hospital = st.text_input("بیمارستان جدید", doc["hospital"])
                new_type = st.selectbox("تخصص جدید", ["زنان", "کودکان", "عمومی"],
                                       index=["زنان", "کودکان", "عمومی"].index(doc["type"]))
                if st.button("ذخیره تغییرات"):
                    doc["hospital"] = new_hospital
                    doc["type"] = new_type
                    st.success("✅ اطلاعات به‌روز شد!")
                break
    else:
        st.warning("هیچ پزشکی وجود ندارد!")

elif menu == "❌ حذف پزشک":
    st.subheader("❌ حذف پزشک")
    names = [doc["name"] for doc in st.session_state.doctor_list]
    if names:
        selected = st.selectbox("انتخاب پزشک برای حذف", names)
        if st.button("حذف"):
            st.session_state.doctor_list = [doc for doc in st.session_state.doctor_list if doc["name"] != selected]
            st.success(f"✅ پزشک {selected} حذف شد!")
    else:
        st.warning("هیچ پزشکی وجود ندارد!")

elif menu == "🔐 رمزنگاری پیام":
    st.subheader("✉️ مادر: تبدیل پیام به کد")
    msg = st.text_input("پیام خود را وارد کنید (فقط حروف انگلیسی):")
    if st.button("ساخت کد"):
        if msg:
            code = ""
            for char in msg:
                code += ramz_kon(char) + " "
            st.success(f"✅ کد شما: `{code.strip()}`")
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
            st.success(f"✅ پیام اصلی: **{message}**")
        else:
            st.error("❌ لطفاً کد را وارد کنید.")