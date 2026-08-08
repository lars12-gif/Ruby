import datetime
import hashlib
import math
import random
import os
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
from supabase import create_client, Client

# ==========================================
# 0. إعداد الاتصال بـ Supabase
# ==========================================
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.environ.get("SUPABASE_KEY")
OPALS_SITE_URL = "https://opal-s-app.streamlit.app/"

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ خطأ في الاتصال. يرجى التأكد من إعدادات الـ Secrets لـ Supabase.")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# 1. إعدادات الصفحة
# ==========================================
st.set_page_config(
    page_title="BELLONA | بنك الروبي الملكي",
    page_icon="💎",
    layout="centered",
)

hide_streamlit_style = """
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {padding-top: 1rem !important;}
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ==========================================
# 2. محرك الصوت والمؤثرات (Particles & Sound FX)
# ==========================================
components.html(
    """
    <script>
    (function() {
        const pDoc = window.parent.document;
        let audioCtx = null;
        function playRubySound() {
            try {
                if (!audioCtx) { audioCtx = new (window.AudioContext || window.webkitAudioContext)(); }
                if (audioCtx.state === 'suspended') { audioCtx.resume(); }
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(880, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(1760, audioCtx.currentTime + 0.1);
                gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
                osc.connect(gain);
                gain.connect(audioCtx.destination);
                osc.start();
                osc.stop(audioCtx.currentTime + 0.1);
            } catch(e) {}
        }
        if (!window.parent.rubyParticlesAdded) {
            window.parent.rubyParticlesAdded = true;
            pDoc.addEventListener('click', function(e) {
                playRubySound();
                const symbols = ['💎', '🌸', '✨', '👑', '💖', '🌺'];
                for (let i = 0; i < 7; i++) {
                    const particle = pDoc.createElement('div');
                    particle.innerText = symbols[Math.floor(Math.random() * symbols.length)];
                    particle.style.position = 'fixed';
                    particle.style.pointerEvents = 'none';
                    particle.style.zIndex = '999999';
                    particle.style.fontSize = (16 + Math.random() * 12) + 'px';
                    particle.style.left = e.clientX + 'px';
                    particle.style.top = e.clientY + 'px';
                    particle.style.transition = 'all 0.75s cubic-bezier(0.1, 0.8, 0.3, 1)';
                    particle.style.opacity = '1';
                    pDoc.body.appendChild(particle);
                    const dx = (Math.random() - 0.5) * 160;
                    const dy = (Math.random() - 0.5) * 160 - 30;
                    const rot = (Math.random() - 0.5) * 360;
                    requestAnimationFrame(() => {
                        particle.style.transform = `translate(${dx}px, ${dy}px) rotate(${rot}deg) scale(1.4)`;
                        particle.style.opacity = '0';
                    });
                    setTimeout(() => particle.remove(), 750);
                }
            });
        }
    })();
    </script>
""", height=0, )

# ==========================================
# 3. تصميم الـ CSS
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; }
    .stApp { background: linear-gradient(180deg, #FFFFFF 0%, #FFF0F5 45%, #FFE4E1 100%) !important; color: #4A0E17 !important; direction: rtl; text-align: right; }
    .ruby-card { background: rgba(255, 255, 255, 0.95); border: 3px solid #FF80AB; border-radius: 26px; padding: 28px; box-shadow: 0 15px 35px rgba(216, 27, 96, 0.18); margin-bottom: 25px; }
    .card-balance { font-size: 3.2rem; font-weight: 900; color: #D81B60; text-shadow: 0px 4px 15px rgba(216, 27, 96, 0.25); margin: 10px 0; }
    .ruby-site-btn { display: block; width: 100%; text-align: center; background: linear-gradient(135deg, #FF4081 0%, #D81B60 100%); color: #FFFFFF !important; font-weight: 800; font-size: 1.1rem; padding: 12px 20px; border-radius: 16px; text-decoration: none !important; margin-bottom: 20px; }
    .stButton>button { background: linear-gradient(90deg, #EC407A 0%, #D81B60 100%) !important; color: #FFFFFF !important; font-weight: 800 !important; border-radius: 16px !important; border: none !important; padding: 12px 24px !important; width: 100%; }
    .receipt-box { background: #FFF0F5; border: 2px dashed #D81B60; border-radius: 18px; padding: 18px; text-align: center; margin-top: 15px; color: #880E4F; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. وظائف القواعد
# ==========================================
def hash_password(pwd): return hashlib.sha256(pwd.encode('utf-8')).hexdigest()

def fetch_user(username):
    try:
        res = supabase.table("users").select("*").eq("username", username).execute()
        return res.data[0] if res.data else None
    except: return None

def refresh_session():
    if st.session_state.get("logged_in"):
        st.session_state["user_data"] = fetch_user(st.session_state["user_data"]["username"])

# ==========================================
# 5. تسجيل الدخول
# ==========================================
if "logged_in" not in st.session_state: st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    st.markdown("<h1 style='text-align: center; color: #D81B60; font-weight: 900;'>🌸 BELLONA BANK 🌸</h1>", unsafe_allow_html=True)
    with st.form("login_form"):
        username_in = st.text_input("اسم المستخدم:")
        password_in = st.text_input("كلمة السر:", type="password")
        if st.form_submit_button("🚀 دخول الخزنة الملكية"):
            res = supabase.table("users").select("password_hash").eq("username", username_in.strip().lower()).execute()
            if res.data and res.data[0]["password_hash"] == hash_password(password_in):
                st.session_state["logged_in"] = True
                st.session_state["user_data"] = fetch_user(username_in.strip().lower())
                st.rerun()
            else: st.error("❌ بيانات خاطئة.")
    st.stop()

# ==========================================
# 6. الواجهة
# ==========================================
refresh_session()
user = st.session_state["user_data"]

# عرض الرصيد
st.markdown(f"""
    <div class="ruby-card">
        <div class="card-balance">{user['balance']:,.2f} <span style="font-size: 1.6rem;">روبي 💎</span></div>
    </div>
""", unsafe_allow_html=True)

tabs = st.tabs(["💸 تحويل", "🎲 سحب يومي", "📜 سجل"])

# التحويل
with tabs[0]:
    res = supabase.table("users").select("username, display_name").neq("username", user["username"]).execute()
    receivers = res.data or []
    if receivers:
        opts = {f"{r['display_name']} (@{r['username']})": r['username'] for r in receivers}
        rec_un = opts[st.selectbox("اختر المستلم:", list(opts.keys()))]
        amt = st.number_input("المبلغ:", min_value=0.5, value=5.0)
        if st.button("🚀 تحويل"):
            if user["balance"] < amt: st.error("❌ رصيدك غير كافٍ!")
            else:
                # 1. خصم المرسل
                supabase.table("users").update({"balance": user["balance"] - amt}).eq("username", user["username"]).execute()
                # 2. إضافة المستلم
                res_rec = supabase.table("users").select("balance").eq("username", rec_un).execute()
                supabase.table("users").update({"balance": res_rec.data[0]["balance"] + amt}).eq("username", rec_un).execute()
                # 3. تسجيل
                supabase.table("transactions").insert({"sender": user["username"], "receiver": rec_un, "amount": amt, "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}).execute()
                refresh_session()
                st.success("✅ تم التحويل!")
                st.rerun()

# السحب اليومي
with tabs[1]:
    now = datetime.datetime.now()
    last_claim_str = user.get("last_daily_claim")
    
    can_claim = True
    remaining_time = ""
    
    if last_claim_str:
        try:
            last_claim_dt = datetime.datetime.strptime(last_claim_str, "%Y-%m-%d %H:%M:%S")
            diff = (last_claim_dt + datetime.timedelta(hours=24)) - now
            if diff.total_seconds() > 0:
                can_claim = False
                hours, remainder = divmod(int(diff.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                remaining_time = f"{hours}س {minutes}د {seconds}ث"
        except: pass

    if not can_claim:
        st.warning(f"⏳ يمكنك الاستلام بعد: {remaining_time}")
    else:
        if st.button("✨ اطلب مكافأة الحظ"):
            won = random.randint(1, 100)
            supabase.table("users").update({"balance": user["balance"] + won, "last_daily_claim": now.strftime("%Y-%m-%d %H:%M:%S")}).eq("username", user["username"]).execute()
            refresh_session()
            st.success(f"🎉 مبروك! ربحت {won} روبي")
            st.rerun()

# سجل
with tabs[2]:
    st.write("سجل المعاملات...")
    res_tx = supabase.table("transactions").select("*").or_(f"sender.eq.{user['username']},receiver.eq.{user['username']}").order("id", desc=True).execute()
    st.dataframe(pd.DataFrame(res_tx.data or []))

if st.button("🚪 خروج"):
    st.session_state["logged_in"] = False
    st.rerun()
