import streamlit as st
from google import genai

# 1. Page Configuration
st.set_page_config(
    page_title="حارس الطفل الرقمي | Digital Child Guardian",
    page_icon="🛡️",
    layout="centered"
)

# 2. Medium-Toned & Friendly UI Styling (Clean, Professional Pastels)
st.markdown("""
    <style>
    .stApp {
        background-color: #f4f7f6;
        color: #2c3e50;
    }
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #ffffff;
        color: #2c3e50;
        border-radius: 12px;
        border: 2px solid #cbd5e1;
    }
    .stTextInput>div>div>input:focus, .stTextArea>div>div>textarea:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 8px rgba(59, 130, 246, 0.2);
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        font-weight: bold;
        border-radius: 12px;
        height: 52px;
        border: none;
        transition: 0.3s;
        font-size: 16px;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        box-shadow: 0 6px 15px rgba(37, 99, 235, 0.3);
    }
    .main-header {
        background: linear-gradient(135deg, #e0f2fe 0%, #e8eaf6 100%);
        padding: 25px;
        border-radius: 16px;
        text-align: center;
        border: 1px solid #cbd5e1;
        margin-bottom: 25px;
    }
    </style>
""", unsafe_allow_html=True)

# 3. Header Section
st.markdown("""
    <div class="main-header">
        <h1 style='color: #1e3a8a; margin-bottom: 5px;'>🛡️ حارس الطفل الرقمي</h1>
        <p style='color: #475569; font-size: 16px; margin: 0;'>مشروع سيف الذكي لحماية أطفالنا من المخاطر والروابط الاحتيالية</p>
    </div>
""", unsafe_allow_html=True)

# Sidebar for API Key Configuration
with st.sidebar:
    st.image("https://img.icons8.com/clouds/200/security-checked.png", width=110)
    st.header("إعدادات المشرف")
    api_key_input = st.text_input("مفتاح Google Gemini API:", type="password", help="ضع مفتاحك المجاني هنا لتفعيل الذكاء الاصطناعي")
    st.markdown("---")
    st.markdown("💡 **عن المشروع:** تطبيق ذكي يحلل الرسائل ليقدم إرشاداً آمناً ولطيفاً للطفل وتنبهاً تقنياً لولي الأمر.")

# Main Input Section
col1, col2 = st.columns([2, 1])
with col1:
    user_input = st.text_area(
        "📱 أرسل أو ألصق الرسالة المشبوهة هنا:",
        placeholder="مثال: مرحباً يا بطل، لقد ربحت معنا آلاف الجواهر في لعبة روبلوكس! اضغط هنا...",
        height=130
    )

with col2:
    st.markdown("<br>", unsafe_allow_html=True)
    target_age = st.selectbox("عمر الطفل المستهدف:", ["6-8 سنوات (ثالث ابتدائي)", "9-12 سنة", "مراهقون"])
    analysis_mode = st.radio("وضع العرض:", ["عرض تفاعلي كامل", "تقرير الوالدين فقط"])

# 4. Analysis Logic with Real AI (Gemini)
if st.button("🚀 بدء الفحص والتحليل الذكي"):
    if not user_input:
        st.warning("⚠️ الرجاء كتابة أو لصق رسالة أولاً لفحصها.")
    elif not api_key_input:
        st.error("⚠️ الرجاء إدخال مفتاح Google Gemini API في القائمة الجانبية.")
    else:
        with st.spinner("🔍 جاري فحص الرابط والنص عبر خوارزميات الأمن السيبراني..."):
            try:
                client = genai.Client(api_key=api_key_input)
                
                prompt = f"""
                You are 'Digital Child Guardian' (حارس الطفل الرقمي), an AI cybersecurity app protecting a 3rd-grade child ({target_age}) from phishing, scams, and online dangers.
                Analyze this message: "{user_input}"
                
                Provide your response clearly separated into these two exact headers in Arabic:
                ### 🧒 رسالة مبسطة للطفل:
                (Friendly, reassuring or gently warning tone suitable for a third-grader, explaining in simple terms why it's safe or risky, without causing fear).
                
                ### 🚨 تقرير أمني لولي الأمر:
                (Concise technical assessment of the threat type, risk level, and recommended parental action).
                """
                
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt
                )
                
                st.success("✨ تم الانتهاء من التحليل الأمني بنجاح!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")