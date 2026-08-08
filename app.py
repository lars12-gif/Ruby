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

# كود إخفاء الشريط العلوي والسفلي لـ Streamlit
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
# 2. محرك الصوت، المؤثرات الحركية (Particles & Sound FX)
# ==========================================
components.html(
    """
    <script>
    (function() {
        const pDoc = window.parent.document;
        let audioCtx = null;

        function playRubySound() {
            try {
                if (!audioCtx) {
                    audioCtx = new (window.AudioContext || window.webkitAudioContext)();
                }
                if (audioCtx.state === 'suspended') {
                    audioCtx.resume();
                }
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
""",
    height=0,
)

# ==========================================
# 3. تصميم الـ CSS الملكي والمتحرك (Opal's Ruby Luxury)
# ==========================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF0F5 45%, #FFE4E1 100%) !important;
        color: #4A0E17 !important;
        direction: rtl;
        text-align: right;
    }

    /* خلفية زهور الكرز المتحركة */
    @keyframes sakura-fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 0.9; }
        100% { transform: translateY(105vh) rotate(360deg); opacity: 0; }
    }
    
    .sakura-container {
        position: fixed; top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none; z-index: 0; overflow: hidden;
    }
    
    .petal {
        position: absolute; background: #FFB7C5;
        border-radius: 15px 0px 15px 0px; opacity: 0.7;
        animation: sakura-fall 8s linear infinite;
    }
    
    .p1 { left: 5%; width: 14px; height: 18px; animation-duration: 7s; }
    .p2 { left: 25%; width: 10px; height: 14px; animation-duration: 9s; background: #FFC0CB; }
    .p3 { left: 50%; width: 16px; height: 20px; animation-duration: 6.5s; }
    .p4 { left: 75%; width: 12px; height: 15px; animation-duration: 8.5s; background: #FFB6C1; }
    .p5 { left: 90%; width: 15px; height: 18px; animation-duration: 10s; }

    /* بطاقة الخزنة البنكية الفاخرة */
    .ruby-card {
        background: rgba(255, 255, 255, 0.95);
        border: 3px solid #FF80AB;
        border-radius: 26px;
        padding: 28px;
        box-shadow: 0 15px 35px rgba(216, 27, 96, 0.18);
        margin-bottom: 25px;
        transition: transform 0.3s ease;
    }

    .ruby-card:hover {
        transform: translateY(-3px);
    }

    .card-balance {
        font-size: 3.2rem;
        font-weight: 900;
        color: #D81B60;
        text-shadow: 0px 4px 15px rgba(216, 27, 96, 0.25);
        margin: 10px 0;
    }

    /* زر الانتقال لموقع نقاط التفاعل (الأوبلز) */
    .ruby-site-btn {
        display: block; width: 100%; text-align: center;
        background: linear-gradient(135deg, #FF4081 0%, #D81B60 100%);
        color: #FFFFFF !important; font-weight: 800; font-size: 1.1rem;
        padding: 12px 20px; border-radius: 16px; text-decoration: none !important;
        box-shadow: 0 6px 20px rgba(216, 27, 96, 0.35); transition: all 0.3s ease; margin-bottom: 20px;
    }
    .ruby-site-btn:hover {
        transform: scale(1.02); box-shadow: 0 8px 25px rgba(216, 27, 96, 0.5);
    }

    /* شارات الرتب الملكية */
    .badge-aurther {
        background: linear-gradient(135deg, #EC407A 0%, #D81B60 100%);
        color: #FFFFFF; padding: 5px 16px; border-radius: 14px;
        font-size: 13px; font-weight: 900; box-shadow: 0 4px 12px rgba(216, 27, 96, 0.35);
    }

    .badge-lamino {
        background: linear-gradient(135deg, #FF80AB 0%, #C2185B 100%);
        color: #FFFFFF; padding: 5px 16px; border-radius: 14px;
        font-size: 13px; font-weight: 900; box-shadow: 0 4px 12px rgba(255, 128, 171, 0.35);
    }

    .badge-admin {
        background: #EC407A; color: #FFF; padding: 4px 12px; border-radius: 10px; font-size: 12px; font-weight: 800;
    }

    .badge-user {
        background: #FFE4E1; color: #C2185B; padding: 4px 12px; border-radius: 10px; font-size: 12px; font-weight: 800; border: 1px solid #FFC1E3;
    }

    /* أزرار الإدخال والتفاعل */
    .stButton>button {
        background: linear-gradient(90deg, #EC407A 0%, #D81B60 100%) !important;
        color: #FFFFFF !important; font-weight: 800 !important;
        border-radius: 16px !important; border: none !important;
        padding: 12px 24px !important; box-shadow: 0 4px 18px rgba(216, 27, 96, 0.35) !important;
        width: 100%; transition: all 0.25s ease-in-out !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px); box-shadow: 0 6px 24px rgba(216, 27, 96, 0.5) !important;
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #FFFFFF !important; color: #37474F !important;
        border: 2px solid #FFC1E3 !important; border-radius: 14px !important;
    }

    /* تصميم التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px !important; background: #FFE4E1 !important;
        padding: 10px 14px !important; border-radius: 22px !important;
        border: 2px solid #FF80AB !important; box-shadow: 0 8px 25px rgba(216, 27, 96, 0.12) !important;
        justify-content: center !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 14px !important; background-color: #FFFFFF !important;
        color: #C2185B !important; font-weight: 800 !important;
        border: 2px solid #FFC1E3 !important; padding: 8px 18px !important;
        transition: all 0.25s ease-in-out !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #EC407A 0%, #D81B60 100%) !important;
        color: #FFFFFF !important; border: 2px solid #D81B60 !important;
        box-shadow: 0 6px 18px rgba(216, 27, 96, 0.4) !important;
    }

    div[data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.96) !important;
        border: 2px solid #FFC1E3 !important; border-radius: 24px !important;
        padding: 25px !important; margin-top: 15px !important;
        box-shadow: 0 10px 30px rgba(216, 27, 96, 0.08) !important;
    }

    /* إيصال التحويل المصرفي */
    .receipt-box {
        background: #FFF0F5; border: 2px dashed #D81B60;
        border-radius: 18px; padding: 18px; text-align: center;
        margin-top: 15px; color: #880E4F;
    }
    </style>

    <div class="sakura-container">
        <div class="petal p1"></div>
        <div class="petal p2"></div>
        <div class="petal p3"></div>
        <div class="petal p4"></div>
        <div class="petal p5"></div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 4. وظائف قواعد البيانات
# ==========================================
def hash_password(pwd):
    return hashlib.sha256(pwd.encode('utf-8')).hexdigest()

def fetch_user(username):
    try:
        res = supabase.table("users").select("*").eq("username", username).execute()
        if res.data:
            user = res.data[0]
            return {
                "username": user["username"],
                "display_name": user["display_name"],
                "balance": user["balance"],
                "role": user["role"],
                "last_daily_claim": user["last_daily_claim"],
            }
        return None
    except Exception as e:
        return None

def refresh_session():
    if st.session_state["logged_in"]:
        st.session_state["user_data"] = fetch_user(st.session_state["user_data"]["username"])

# ==========================================
# 5. إدارة الجلسة
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_data"] = None

# ==========================================
# 6. شاشة تسجيل الدخول
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown(
        "<h1 style='text-align: center; color: #D81B60; font-weight: 900;'>🌸 BELLONA BANK 🌸</h1>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align: center; color: #C2185B; font-weight: 700;'>✨ الخزنة المصرفية الملكية لعملة الروبي ✨</p>",
        unsafe_allow_html=True,
    )

    st.markdown(f'<a href="{OPALS_SITE_URL}" target="_blank" class="ruby-site-btn">✨ الانتقال إلى موقع نقاط التفاعل (Opal\'s) 🚀</a>', unsafe_allow_html=True)

    with st.form("login_form"):
        st.subheader("🔑 تسجيل الدخول لـ حسابك")
        username_in = st.text_input("اسم المستخدم (Username):")
        password_in = st.text_input("كلمة السر:", type="password")

        if st.form_submit_button("🚀 دخول الخزنة الملكية"):
            clean_un = username_in.strip().lower()
            
            res = supabase.table("users").select("password_hash").eq("username", clean_un).execute()
            if res.data and res.data[0]["password_hash"] == hash_password(password_in):
                st.session_state["logged_in"] = True
                st.session_state["user_data"] = fetch_user(clean_un)
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("❌ اسم المستخدم أو كلمة السر غير صحيحة.")

    st.warning("🔒 الحسابات يتم إنشاؤها حصراً عن طريق المشرفين (Aurther / Lamino).")
    st.stop()

# ==========================================
# 7. الواجهة الرئيسية
# ==========================================
refresh_session()
user = st.session_state["user_data"]

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown("<h2 style='color: #D81B60; font-weight: 900;'>💎 بنك الروبي الملكي</h2>", unsafe_allow_html=True)
with col2:
    if st.button("🚪 خروج"):
        st.session_state["logged_in"] = False
        st.session_state["user_data"] = None
        st.rerun()

# الشارات الملكية الخاصة
if user["username"] == "aurther":
    role_badge = '<span class="badge-aurther">👑 المشرف العام (Aurther)</span>'
elif user["username"] == "lamino":
    role_badge = '<span class="badge-lamino">🤝 المساعد العام (Lamino)</span>'
elif user["role"] == "admin":
    role_badge = '<span class="badge-admin">🛡️ مشرف</span>'
else:
    role_badge = '<span class="badge-user">💎 عضو ملكي</span>'

st.markdown(
    f"""
    <div class="ruby-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 1.25rem; font-weight: 800; color: #37474F;">👤 {user['display_name']} (@{user['username']})</span>
            {role_badge}
        </div>
        <div class="card-balance">{user['balance']:,.2f} <span style="font-size: 1.6rem;">روبي 💎</span></div>
        <div style="font-size: 11px; color: #880E4F; font-weight: 700;">معرف الخزنة: RB-{hashlib.md5(user['username'].encode()).hexdigest()[:8].upper()}</div>
    </div>
""",
    unsafe_allow_html=True,
)

st.markdown(f'<a href="{OPALS_SITE_URL}" target="_blank" class="ruby-site-btn">✨ الانتقال إلى موقع نقاط التفاعل (Opal\'s) 🚀</a>', unsafe_allow_html=True)

tabs_list = [
    "💸 التحويل الفوري",
    "🏆 قائمة الأثرياء",
    "🎲 سحب الحظ اليومي",
    "📜 سجل المعاملات",
    "🔒 إعدادات الحساب",
]

if user["role"] == "admin":
    tabs_list.append("🛡️ لوحة المشرفين")

tabs = st.tabs(tabs_list)

# --- تبويب التحويل (مع حل مشكلة التحديث) ---
with tabs[0]:
    st.subheader("💸 إجراء تحويل مالي سريح")

    res = supabase.table("users").select("username, display_name").neq("username", user["username"]).execute()
    receivers = res.data or []

    if receivers:
        opts = {f"{r['display_name']} (@{r['username']})": r['username'] for r in receivers}
        sel = st.selectbox("اختر العضو المستلم:", list(opts.keys()))
        rec_un = opts[sel]

        amt = st.number_input("المبلغ المراد تحويله (روبي):", min_value=0.5, value=5.0)
        note = st.text_input("سبب / ملاحظة التحويل:", value="تحويل روبي 💎")

        if st.button("🚀 تحويل الروبي الآن"):
            # تحديث البيانات قبل التأكد من الرصيد
            refresh_session()
            user = st.session_state["user_data"]
            
            if user["balance"] < amt:
                st.error("❌ رصيدك الحالي لا يكفي لإتمام التحويل!")
            else:
                # 1. خصم من المرسل
                supabase.table("users").update({"balance": user["balance"] - amt}).eq("username", user["username"]).execute()
                
                # 2. إضافة للمستلم
                res_rec = supabase.table("users").select("balance").eq("username", rec_un).execute()
                rec_bal = res_rec.data[0]["balance"]
                supabase.table("users").update({"balance": rec_bal + amt}).eq("username", rec_un).execute()

                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                # تسجيل المعاملة
                supabase.table("transactions").insert({
                    "sender": user["username"],
                    "receiver": rec_un,
                    "amount": amt,
                    "note": note,
                    "timestamp": now
                }).execute()

                st.balloons()
                st.success("✅ تم إتمام التحويل بنجاح!")
                
                # تحديث الجلسة وإعادة التحميل لإظهار الرصيد الجديد فوراً
                refresh_session()
                st.rerun()

    else:
        st.info("💡 لا يوجد أعضاء آخرين مسجلين في البنك حالياً.")

# --- تبويب السحب اليومي (مع العداد) ---
with tabs[2]:
    st.subheader("🎲 عجلة الحظ اليومية")
    st.write("جرب حظك كل 24 ساعة واحصل على مكافأة عشوائية تصل إلى **100 روبي**!")

    now = datetime.datetime.now()
    last_claim_str = user.get("last_daily_claim")
    
    can_claim = True
    remaining_time = ""
    
    if last_claim_str and last_claim_str != "":
        try:
            last_claim_dt = datetime.datetime.strptime(last_claim_str, "%Y-%m-%d %H:%M:%S")
            # نحسب 24 ساعة من آخر استلام
            diff = (last_claim_dt + datetime.timedelta(hours=24)) - now
            if diff.total_seconds() > 0:
                can_claim = False
                hours, remainder = divmod(int(diff.total_seconds()), 3600)
                minutes, seconds = divmod(remainder, 60)
                remaining_time = f"{hours} ساعة و {minutes} دقيقة و {seconds} ثانية"
        except:
            # إذا كان الفورمات قديم (YYYY-MM-DD)، نصفر العداد
            can_claim = True

    if not can_claim:
        st.warning(f"⏳ لقد استلمت مكافأتك بالفعل! يمكنك الاستلام مرة أخرى بعد: {remaining_time}")
    else:
        if st.button("✨ اطلب مكافأة الحظ اليومية ✨"):
            won = random.randint(1, 100)
            now_str = now.strftime("%Y-%m-%d %H:%M:%S")

            supabase.table("users").update({
                "balance": user["balance"] + won,
                "last_daily_claim": now_str
            }).eq("username", user["username"]).execute()

            supabase.table("transactions").insert({
                "sender": "نظام الحظ 🎲",
                "receiver": user["username"],
                "amount": won,
                "note": "مكافأة يومية 🌟",
                "timestamp": now_str
            }).execute()

            st.balloons()
            st.success(f"🎉 مبروك! ابتسم لك الحظ وحصلت على **{won} روبي** إضافية 💎")
            refresh_session()
            st.rerun()

# --- التبويب 2: قائمة الأثرياء ---
with tabs[1]:
    st.subheader("🏆 ترتيب أثرياء بنك الروبي")
    res_top = supabase.table("users").select("display_name, username, balance").order("balance", desc=True).limit(10).execute()
    df_top = pd.DataFrame(res_top.data or [])
    if not df_top.empty:
        df_top = df_top.rename(columns={"display_name": "الاسم", "username": "اليوزر", "balance": "رصيد الروبي"})
        st.dataframe(df_top, use_container_width=True)

# --- التبويب 4: سجل المعاملات ---
with tabs[3]:
    st.subheader("📜 سجل التحويلات والاستلام الخاص بك")
    res_tx = supabase.table("transactions").select("sender, receiver, amount, note, timestamp").or_(f"sender.eq.{user['username']},receiver.eq.{user['username']}").order("id", desc=True).execute()
    df_tx = pd.DataFrame(res_tx.data or [])
    if not df_tx.empty:
        df_tx = df_tx.rename(columns={"sender": "المرسل", "receiver": "المستلم", "amount": "المبلغ (روبي)", "note": "الملاحظة", "timestamp": "التاريخ والوقت"})
        st.dataframe(df_tx, use_container_width=True)

# --- التبويب 5: إعدادات الحساب ---
with tabs[4]:
    st.subheader("🔒 إعدادات الحساب والأمان")
    with st.form("pwd_form"):
        c_pwd = st.text_input("كلمة السر الحالية:", type="password")
        n_pwd = st.text_input("كلمة السر الجديدة:", type="password")
        conf_pwd = st.text_input("تأكيد كلمة السر الجديدة:", type="password")
        if st.form_submit_button("✏️ تحديث كلمة السر"):
            res_pwd = supabase.table("users").select("password_hash").eq("username", user["username"]).execute()
            if hash_password(c_pwd) == res_pwd.data[0]["password_hash"]:
                supabase.table("users").update({"password_hash": hash_password(n_pwd)}).eq("username", user["username"]).execute()
                st.success("✅ تم تحديث كلمة السر!")
            else: st.error("❌ كلمة السر الحالية خاطئة.")

# --- التبويب 6: لوحة المشرفين ---
if user["role"] == "admin":
    with tabs[5]:
        st.subheader("🛡️ لوحة التحكم والإشراف العام")
        # (بقية كود المشرفين كما هو تماماً)
        act = st.radio("اختر الإجراء:", ["➕ إضافة عضو", "💰 تعديل رصيد", "❌ حذف حساب", "👥 عرض الأعضاء"], horizontal=True)
        # ... بقية الكود هنا ...
