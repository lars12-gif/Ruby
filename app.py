import datetime
import hashlib
import random
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import os
from supabase import create_client, Client

# ==========================================
# 0. إعداد الاتصال (Supabase)
# ==========================================
SUPABASE_URL = st.secrets.get("SUPABASE_URL") or os.environ.get("SUPABASE_URL")
SUPABASE_KEY = st.secrets.get("SUPABASE_KEY") or os.environ.get("SUPABASE_KEY")
OPALS_SITE_URL = "https://opal-s-app.streamlit.app/"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# 1. إعدادات الصفحة (تم إضافة كود إخفاء الشريط)
# ==========================================
st.set_page_config(page_title="BELLONA | بنك الروبي الملكي", page_icon="💎", layout="centered")

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
# 2. محرك الصوت، المؤثرات الحركية (نفس الكود الأصلي)
# ==========================================
components.html(
    """
    <script>
    (function() {
        const pDoc = window.parent.document;
        let audioCtx = null;
        function playRubySound() {
            try {
                if (!audioCtx) audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                if (audioCtx.state === 'suspended') audioCtx.resume();
                const osc = audioCtx.createOscillator();
                const gain = audioCtx.createGain();
                osc.type = 'sine'; osc.frequency.setValueAtTime(880, audioCtx.currentTime);
                osc.frequency.exponentialRampToValueAtTime(1760, audioCtx.currentTime + 0.1);
                gain.gain.setValueAtTime(0.12, audioCtx.currentTime);
                gain.gain.exponentialRampToValueAtTime(0.001, audioCtx.currentTime + 0.1);
                osc.connect(gain); gain.connect(audioCtx.destination);
                osc.start(); osc.stop(audioCtx.currentTime + 0.1);
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
                    particle.style.position = 'fixed'; particle.style.pointerEvents = 'none';
                    particle.style.zIndex = '999999'; particle.style.fontSize = (16 + Math.random() * 12) + 'px';
                    particle.style.left = e.clientX + 'px'; particle.style.top = e.clientY + 'px';
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
""", height=0)

# ==========================================
# 3. تصميم الـ CSS الملكي (نفس الكود الأصلي)
# ==========================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; }
    .stApp { background: linear-gradient(180deg, #FFFFFF 0%, #FFF0F5 45%, #FFE4E1 100%) !important; color: #4A0E17 !important; direction: rtl; text-align: right; }
    .ruby-card { background: rgba(255, 255, 255, 0.95); border: 3px solid #FF80AB; border-radius: 26px; padding: 28px; box-shadow: 0 15px 35px rgba(216, 27, 96, 0.18); margin-bottom: 25px; }
    .card-balance { font-size: 3.2rem; font-weight: 900; color: #D81B60; text-shadow: 0px 4px 15px rgba(216, 27, 96, 0.25); margin: 10px 0; }
    .badge-aurther { background: linear-gradient(135deg, #EC407A 0%, #D81B60 100%); color: #FFFFFF; padding: 5px 16px; border-radius: 14px; font-size: 13px; font-weight: 900; }
    .badge-lamino { background: linear-gradient(135deg, #FF80AB 0%, #C2185B 100%); color: #FFFFFF; padding: 5px 16px; border-radius: 14px; font-size: 13px; font-weight: 900; }
    .badge-admin { background: #EC407A; color: #FFF; padding: 4px 12px; border-radius: 10px; font-size: 12px; font-weight: 800; }
    .badge-user { background: #FFE4E1; color: #C2185B; padding: 4px 12px; border-radius: 10px; font-size: 12px; font-weight: 800; border: 1px solid #FFC1E3; }
    .stButton>button { background: linear-gradient(90deg, #EC407A 0%, #D81B60 100%) !important; color: #FFFFFF !important; font-weight: 800 !important; border-radius: 16px !important; border: none !important; padding: 12px 24px !important; width: 100%; }
    .stTextInput input { background-color: #FFFFFF !important; border: 2px solid #FFC1E3 !important; border-radius: 14px !important; }
    .ruby-site-btn { display: block; width: 100%; text-align: center; background: linear-gradient(135deg, #FF4081 0%, #D81B60 100%); color: #FFFFFF !important; font-weight: 800; padding: 12px; border-radius: 16px; text-decoration: none !important; margin-bottom: 20px; }
    .receipt-box { background: #FFF0F5; border: 2px dashed #D81B60; border-radius: 18px; padding: 18px; text-align: center; margin-top: 15px; color: #880E4F; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# 4. الدوال (Supabase)
# ==========================================
def hash_password(pwd): return hashlib.sha256(pwd.strip().encode('utf-8')).hexdigest()

def fetch_user(username):
    res = supabase.table("users").select("*").eq("username", username).execute()
    return res.data[0] if res.data else None

def refresh_session():
    if st.session_state["logged_in"]:
        st.session_state["user_data"] = fetch_user(st.session_state["user_data"]["username"])

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_data"] = None

# ==========================================
# 5. شاشة تسجيل الدخول
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown("<h1 style='text-align: center; color: #D81B60; font-weight: 900;'>🌸 BELLONA BANK 🌸</h1>", unsafe_allow_html=True)
    # زر الأوبلز الجديد في صفحة الدخول
    st.markdown(f'<a href="{OPALS_SITE_URL}" target="_blank" class="ruby-site-btn">✨ الانتقال إلى موقع نقاط التفاعل (Opal\'s) 🚀</a>', unsafe_allow_html=True)

    with st.form("login_form"):
        st.subheader("🔑 تسجيل الدخول")
        username_in = st.text_input("اسم المستخدم:")
        password_in = st.text_input("كلمة السر:", type="password")
        if st.form_submit_button("🚀 دخول الخزنة الملكية"):
            user = fetch_user(username_in.strip().lower())
            if user and (user["password_hash"] == hash_password(password_in) or user["password_hash"] == password_in):
                st.session_state["logged_in"] = True
                st.session_state["user_data"] = user
                st.rerun()
            else: st.error("❌ خطأ.")
    st.stop()

# ==========================================
# 6. الواجهة الرئيسية
# ==========================================
refresh_session()
user = st.session_state["user_data"]
col1, col2 = st.columns([3, 1])
with col1: st.markdown("## 💎 بنك الروبي الملكي")
with col2:
    if st.button("🚪 خروج"):
        st.session_state["logged_in"] = False
        st.rerun()

# الشارات
if user["username"] == "aurther": badge = '<span class="badge-aurther">👑 المشرف العام</span>'
elif user["username"] == "lamino": badge = '<span class="badge-lamino">🤝 المساعد العام</span>'
elif user["role"] == "admin": badge = '<span class="badge-admin">🛡️ مشرف</span>'
else: badge = '<span class="badge-user">💎 عضو ملكي</span>'

st.markdown(f"""
    <div class="ruby-card">
        <h3>👤 {user['display_name']}</h3>
        <div class="card-balance">{user['balance']:,.2f} 💎</div>
        <div>{badge}</div>
    </div>
""", unsafe_allow_html=True)

# زر الأوبلز في الواجهة الرئيسية
st.markdown(f'<a href="{OPALS_SITE_URL}" target="_blank" class="ruby-site-btn">✨ الانتقال إلى موقع نقاط التفاعل (Opal\'s) 🚀</a>', unsafe_allow_html=True)

tabs_list = ["💸 التحويل الفوري", "🏆 الأثرياء", "🎲 الحظ", "📜 المعاملات", "🔒 الإعدادات"]
if user["role"] == "admin": tabs_list.append("🛡️ لوحة المشرفين")
tabs = st.tabs(tabs_list)

# --- التبويب 1: التحويل ---
with tabs[0]:
    res = supabase.table("users").select("username, display_name").neq("username", user["username"]).execute()
    receivers = {f"{r['display_name']} (@{r['username']})": r['username'] for r in (res.data or [])}
    sel = st.selectbox("المستلم:", list(receivers.keys()))
    amt = st.number_input("المبلغ:", min_value=0.5, value=1.0)
    note = st.text_input("ملاحظة:")
    if st.button("🚀 تحويل"):
        if user["balance"] >= amt:
            supabase.table("users").update({"balance": user["balance"] - amt}).eq("username", user["username"]).execute()
            rec_un = receivers[sel]
            rec_data = fetch_user(rec_un)
            supabase.table("users").update({"balance": rec_data["balance"] + amt}).eq("username", rec_un).execute()
            supabase.table("transactions").insert({"sender": user["username"], "receiver": rec_un, "amount": amt, "note": note, "timestamp": str(datetime.datetime.now())}).execute()
            st.success("✅ تم")
            st.rerun()
        else: st.error("❌ رصيد غير كافٍ")

# --- التبويب 2: الأثرياء ---
with tabs[1]:
    data = supabase.table("users").select("display_name, balance").order("balance", desc=True).execute().data
    if data: st.dataframe(pd.DataFrame(data), use_container_width=True)

# --- التبويب 3: الحظ ---
with tabs[2]:
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    if user.get("last_daily_claim") == today: st.warning("⏳ استلمت مكافأتك!")
    elif st.button("✨ اطلب المكافأة"):
        won = random.randint(1, 100)
        supabase.table("users").update({"balance": user["balance"] + won, "last_daily_claim": today}).eq("username", user["username"]).execute()
        st.success(f"🎉 ربحت {won}!")
        st.rerun()

# --- التبويب 4: السجل ---
with tabs[3]:
    txs = supabase.table("transactions").select("*").or_(f"sender.eq.{user['username']},receiver.eq.{user['username']}").execute().data
    if txs: st.dataframe(pd.DataFrame(txs))

# --- التبويب 5: الإعدادات ---
with tabs[4]:
    with st.form("pwd"):
        old = st.text_input("القديمة:", type="password")
        new = st.text_input("الجديدة:", type="password")
        if st.form_submit_button("تحديث"):
            if hash_password(old) == user["password_hash"]:
                supabase.table("users").update({"password_hash": hash_password(new)}).eq("username", user["username"]).execute()
                st.success("✅ تم")
            else: st.error("❌ خطأ")

# --- التبويب 6: المشرفين ---
if user["role"] == "admin":
    with tabs[5]:
        target = st.text_input("يوزر العضو:")
        add = st.number_input("تعديل الرصيد (+ أو -):")
        if st.button("تنفيذ"):
            t_data = fetch_user(target)
            if t_data:
                supabase.table("users").update({"balance": t_data["balance"] + add}).eq("username", target).execute()
                st.success("✅ تم")
