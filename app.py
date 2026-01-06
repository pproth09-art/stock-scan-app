import streamlit as st
import pandas as pd

# ตั้งค่าหน้าแอป
st.set_page_config(page_title="StockScan Pro", layout="centered")

# --- ส่วนจัดการหน่วยความจำ (Session State) ---
# บันทึกรายการคำที่ต้องการค้นหาไว้ตลอดการใช้งาน
if 'saved_keywords' not in st.session_state:
    st.session_state.saved_keywords = ["แสงโสม", "โซดาร็อค", "รีเจนซี่"] # ตั้งค่าเริ่มต้นไว้ให้

st.title("📦 StockScan Auto-Fill")
st.write("เลือกรายการที่คุณบันทึกไว้เพื่อดูจำนวนจากใบเสร็จทันที")

# 1. ส่วนเพิ่มคำค้นหาใหม่ (บันทึกไว้โชว์)
with st.expander("➕ เพิ่ม/จัดการรายการที่ค้นหาบ่อย"):
    new_word = st.text_input("ใส่ชื่อสินค้าที่ต้องการบันทึก:")
    if st.button("บันทึกรายการนี้"):
        if new_word and new_word not in st.session_state.saved_keywords:
            st.session_state.saved_keywords.append(new_word)
            st.rerun()
    
    if st.button("🗑️ ล้างรายการที่บันทึกทั้งหมด"):
        st.session_state.saved_keywords = []
        st.rerun()

st.write("---")

# 2. ส่วนแสดงปุ่มรายการที่บันทึกไว้ (แสดงโชว์ไว้ตลอด)
st.subheader("📌 รายการที่คุณต้องการค้นหา")
selected_keyword = None

# สร้างปุ่มรายการโปรดแบบเรียงกัน
cols = st.columns(3) # แบ่งเป็น 3 คอลัมน์เพื่อให้ปุ่มเรียงสวยงาม
for i, word in enumerate(st.session_state.saved_keywords):
    if cols[i % 3].button(f"🔍 {word}", key=f"btn_{word}", use_container_width=True):
        selected_keyword = word

st.write("---")

# 3. ส่วนนำเข้าข้อมูลใบเสร็จ
uploaded_file = st.file_uploader("📸 อัปโหลดรูปใบส่งสินค้า", type=["jpg", "png", "jpeg"])

# ข้อมูลจำลอง (ในแอปจริงส่วนนี้จะมาจาก OCR)
data = [
    {"รายการ": "แสงโสมกลม (Sang Som)", "ขนาด": "0.75 ลิตร", "จำนวน": 1, "หน่วย": "ลัง"},
    {"รายการ": "โซดาร็อคเมาเท่น (ROCK)", "ขนาด": "325 ml.", "จำนวน": 2, "หน่วย": "ถาด"},
    {"รายการ": "รีเจนซี่ (Regency)", "ขนาด": "500 cc.", "จำนวน": 1, "หน่วย": "ขวด"},
    {"รายการ": "เบียร์สิงห์เล็ก", "ขนาด": "320 ml.", "จำนวน": 7, "หน่วย": "ลัง"}
]
df = pd.DataFrame(data)

# 4. แสดงผลลัพธ์เมื่อกดปุ่มรายการโปรด
if uploaded_file and selected_keyword:
    st.subheader(f"📊 ผลลัพธ์สำหรับ: {selected_keyword}")
    # ค้นหาคำที่ตรงกันใน DataFrame
    result = df[df['รายการ'].str.contains(selected_keyword, case=False, na=False)]
    
    if not result.empty:
        for index, row in result.iterrows():
            # แสดง 4 คอลัมน์ รายการ | ขนาด | จำนวน | หน่วย
            with st.container():
                c1, c2, c3, c4 = st.columns([2, 1, 1, 1])
                c1.write(f"**{row['รายการ']}**")
                c2.write(row['ขนาด'])
                c3.write(f"**{row['จำนวน']}**")
                c4.write(row['หน่วย'])
                
                if st.button(f"📋 คัดลอก {row['จำนวน']}", key=f"cp_{index}"):
                    st.success(f"ก๊อปปี้เลข {row['จำนวน']} แล้ว!")
            st.write("---")
    else:
        st.warning(f"ใบเสร็จนี้ไม่มีรายการ '{selected_keyword}'")

elif not uploaded_file:
    st.info("👆 กรุณาอัปโหลดรูปใบเสร็จก่อนเริ่มค้นหา")
