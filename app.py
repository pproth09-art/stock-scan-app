import streamlit as st
import pandas as pd

# ตั้งค่าหน้าแอป
st.set_page_config(page_title="StockScan Pro", layout="centered")

# --- ส่วนจัดการหน่วยความจำ (Session State) ---
# ใช้สำหรับเก็บคำค้นหาที่ผู้ใช้บันทึกไว้ ไม่ให้หายไปเมื่อรีเฟรชหรือเปลี่ยนรูป
if 'saved_items' not in st.session_state:
    st.session_state.saved_items = []

st.title("📦 StockScan Auto-Fill")
st.write("จัดการสต็อกด้วยระบบบันทึกรายการโปรด")

# 1. ส่วนนำเข้าข้อมูล
uploaded_file = st.file_uploader("📸 อัปโหลดรูปใบเสร็จ", type=["jpg", "png", "jpeg"])

# ข้อมูลจำลองจากใบเสร็จ (ในอนาคตส่วนนี้จะเชื่อมกับระบบสแกนจริง)
data = [
    {"รายการ": "แสงโสมกลม (Sang Som)", "ขนาด": "0.75 ลิตร", "จำนวน": 1, "หน่วย": "ลัง"},
    {"รายการ": "โซดาร็อคเมาเท่น (ROCK)", "ขนาด": "325 ml.", "จำนวน": 2, "หน่วย": "ถาด"},
    {"รายการ": "รีเจนซี่ (Regency)", "ขนาด": "500 cc.", "จำนวน": 1, "หน่วย": "ขวด"},
    {"รายการ": "เบียร์สิงห์เล็ก (Singha)", "ขนาด": "320 ml.", "จำนวน": 7, "หน่วย": "ลัง"}
]
df = pd.DataFrame(data)

# 2. ส่วนการค้นหาและบันทึก
st.subheader("🔍 ค้นหาและบันทึกรายการโปรด")
col_search, col_btn = st.columns([3, 1])

with col_search:
    search_input = st.text_input("พิมพ์ชื่อสินค้าเพื่อค้นหาและบันทึก:", placeholder="เช่น แสงโสม...")

with col_btn:
    st.write(" ") # ระยะห่าง
    if st.button("⭐ บันทึก"):
        if search_input and search_input not in st.session_state.saved_items:
            st.session_state.saved_items.append(search_input)
            st.toast(f"บันทึก '{search_input}' เรียบร้อย!")

# 3. แสดงรายการที่บันทึกไว้ (ไม่ลบหายไป)
if st.session_state.saved_items:
    st.write("---")
    st.write("📌 **รายการที่คุณบันทึกไว้ (กดเพื่อค้นหาทันที):**")
    
    # แสดงเป็นปุ่มเล็กๆ ให้กดง่าย
    cols = st.columns(3)
    for i, item in enumerate(st.session_state.saved_items):
        if cols[i % 3].button(f"🔍 {item}", key=f"saved_{i}"):
            search_input = item # เมื่อกดปุ่ม ให้ค่าไปแสดงในช่องค้นหา

    if st.button("🗑️ ล้างรายการที่บันทึกทั้งหมด"):
        st.session_state.saved_items = []
        st.rerun()

st.write("---")

# 4. แสดงผลการค้นหา (4 คอลัมน์)
if uploaded_file and search_input:
    result = df[df['รายการ'].str.contains(search_input, case=False, na=False)]
    
    if not result.empty:
        st.subheader("📊 ผลการสแกนที่ตรงกัน")
        for index, row in result.iterrows():
            with st.expander(f"✅ {row['รายการ']}", expanded=True):
                c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                c1.write(f"ขนาด: {row['ขนาด']}")
                c2.write(f"**{row['จำนวน']}**")
                c3.write(row['หน่วย'])
                if c4.button("📋 ก๊อป", key=f"cp_{index}"):
                    st.success(f"คัดลอกเลข {row['จำนวน']} แล้ว")
    else:
        st.warning("ไม่พบสินค้าที่ตรงกับคำค้นหาในใบเสร็จนี้")
