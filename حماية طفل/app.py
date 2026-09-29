import streamlit as st
from google import genai

# 1. Page Configuration
st.set_page_config(
    page_title="حارس الطفل الرقمي",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Strict CSS Theme Override (Fixes Dark Mode contrast & illegible text)
st.markdown("""
<style>
    /* HIDE STREAMLIT BRANDING & NAVBAR */
    #MainMenu, footer, header {visibility: hidden !important;}
    .stDeployButton, [data-testid="stHeader"], [data-testid="stToolbar"], 
    [data-testid="stSidebarNav"], [data-testid="stDecoration"], 
    [data-testid="stStatusWidget"], #GithubIcon {display: none !important;}

    /* GLOBAL LIGHT BACKGROUND & FORCED DARK TEXT */
    .stApp {
        background-color: #f1f5f9 !important;
        color: #0f172a !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }

    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 680px;
    }

    /* HEADER BANNER */
    .app-header {
        background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
        color: #ffffff !important;
        padding: 28px 20px;
        border-radius: 20px;
        text-align: center;
        box-shadow: 0 10px 20px rgba(37, 99, 235, 0.2);
        margin-bottom: 24px;
    }
    .app-header h1 {
        color: #ffffff !important;
        font-size: 26px;
        font-weight: 700;
        margin-bottom: 6px;
    }
    .app-header p {
        color: #dbeafe !important;
        font-size: 15px;
        margin: 0;
    }

    /* FORCE ALL LABELS TO BE VISIBLE DARK TEXT */
    label, .stWidgetLabel, [data-testid="stWidgetLabel"] p {
        color: #1e293b !important;
        font-weight: 600 !important;
        font-size: 15px !important;
    }

    /* TEXT AREA & INPUT STYLING */
    .stTextArea textarea {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-radius: 12px !important;
        border: 2px solid #cbd5e1 !important;
        padding: 14px !important;
        font-size: 15px !important;
    }
    .stTextArea textarea::placeholder {
        color: #94a3b8 !important;
    }

    /* DROPDOWN SELECTBOX STYLING */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        color: #0f172a !important;
        border-radius: 12px !important;
        border: 2px solid #cbd5e1 !important;
    }
    div[data-baseweb="select"] * {
        color: #0f172a !important;
        background-color: #ffffff !important;
    }

    /* BUTTON STYLING */
    .stButton > button {
        width: 100%;
        background-color: #2563eb !important;
        color: #ffffff !important;
        border-radius: 12px !important;
        height: 50px !important;
        font-size: 16px !important;
        font-weight: 600 !important;
        border: none !important;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3) !important;
    }
    .stButton > button:hover {
        background-color: #1d4ed8 !important;
    }
</style>
""", unsafe_allow_html=True)

# 3. App Header Display
st.markdown("""
    <div class="app-header">
        <h1>🛡️ حارس الطفل الرقمي</h1>
        <p>نظام التوعية والتحليل الأمني الذكي لحماية الأطفال من المخاطر الرقمية</p>
    </div>
""", unsafe_allow_html=True)

# 4. API Key Resolution
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    with st.sidebar:
        st.header("⚙️ إعدادات المفتاح")
        api_key = st.text_input("مفتاح Google Gemini API:", type="password")

# 5. User Inputs
user_input = st.text_area(
    "📱 أدخل أو ألصق الرسالة/الرابط هنا:",
    placeholder="مثال: مرحباً يا بطل، لقد ربحت معنا آلاف الجواهر في لعبة روبلوكس! اضغط هنا للحصول عليها...",
    height=120
)

target_age = st.selectbox(
    "عمر الطفل المستهدف:",
    ["6-8 سنوات (ثالث ابتدائي)", "9-12 سنة", "مراهقون"]
)

# 6. Analysis Execution
if st.button("🚀 بدء الفحص والتحليل الأمني"):
    if not user_input:
        st.warning("⚠️ الرجاء كتابة أو لصق رسالة أولاً لفحصها.")
    elif not api_key:
        st.error("⚠️️ لم يتم العثور على مفتاح API في الإعدادات.")
    else:
        with st.spinner("🔍 جاري فحص الرابط والنص عبر الذكاء الاصطناعي..."):
            try:
                client = genai.Client(api_key=api_key)
                prompt = f"""
                You are 'Digital Child Guardian' (حارس الطفل الرقمي), an AI cybersecurity app protecting a child ({target_age}) from phishing, scams, and online dangers.
                Analyze this message: "{user_input}"
                
                Respond clearly separated into two sections using exact Arabic Markdown headers:
                ### 🧒 رسالة مبسطة للطفل:
                (A friendly, safe, non-scary explanation suited for this child's age group explaining why it is safe or unsafe).
                
                ### 🚨 تقرير أمني لولي الأمر:
                (Concise technical risk analysis, threat level, and actionable recommendation for parents).
                """
                
                response = client.models.generate_content(
                    model='gemini-3.8-flash',
                    contents=prompt
                )
                
                st.success("✨ تم التحليل بنجاح!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"حدث خطأ أثناء الاتصال بالذكاء الاصطناعي: {e}")
