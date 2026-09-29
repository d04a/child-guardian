import streamlit as st
from google import genai

# 1. Page Configuration
st.set_page_config(
    page_title="حارس الطفل الرقمي",
    page_icon="🛡️",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# 2. Complete CSS Customization (Clean UI + Hides Streamlit GitHub/Footer Elements)
st.markdown("""
<style>
    /* HIDE ALL DEFAULT STREAMLIT HEADERS, FOOTERS & GITHUB ICONS */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none !important;}
    [data-testid="stHeader"] {display: none !important;}
    [data-testid="stToolbar"] {display: none !important;}
    [data-testid="stSidebarNav"] {display: none !important;}
    [data-testid="stDecoration"] {display: none !important;}
    [data-testid="stStatusWidget"] {display: none !important;}
    #GithubIcon {visibility: hidden !important;}

    /* GLOBAL CLEAN PASTEL THEMING */
    .stApp {
        background: #f1f5f9;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* CENTERED MAIN CONTAINER */
    .block-container {
        padding-top: 2rem !important;
        padding-bottom: 2rem !important;
        max-width: 680px;
    }
    
    /* APP HEADER BANNER */
    .app-header {
        background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
        color: white;
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

    /* INPUT FIELD STYLING */
    .stTextArea textarea {
        border-radius: 14px !important;
        border: 2px solid #cbd5e1 !important;
        padding: 14px !important;
        font-size: 15px !important;
        background-color: #ffffff !important;
        color: #0f172a !important;
    }
    .stTextArea textarea:focus {
        border-color: #3b82f6 !important;
        box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.2) !important;
    }

    /* SELECTBOX STYLING */
    div[data-baseweb="select"] > div {
        border-radius: 12px !important;
        border: 2px solid #cbd5e1 !important;
        background-color: #ffffff !important;
    }

    /* PRIMARY BUTTON STYLING */
    .stButton > button {
        width: 100%;
        background: #2563eb;
        color: white;
        border-radius: 12px;
        height: 50px;
        font-size: 17px;
        font-weight: 600;
        border: none;
        transition: all 0.2s ease-in-out;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
    }
    .stButton > button:hover {
        background: #1d4ed8;
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
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

# 4. API Key Resolution (Uses Secrets directly, fallback to sidebar if missing)
api_key = None
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    with st.sidebar:
        st.header("⚙️ إعدادات المفتاح")
        api_key = st.text_input("مفتاح Google Gemini API:", type="password")

# 5. User Input Controls
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
        st.error("⚠️ لم يتم العثور على مفتاح API في الإعدادات.")
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
