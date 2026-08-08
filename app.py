import datetime
import hashlib
import random
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import os
from supabase import create_client, Client

# ==========================================
# 0. إعداد الاتصال بـ Supabase ورابط الموقع
# ==========================================
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
OPALS_SITE_URL = "https://opal-s-app.streamlit.app/"

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("⚠️ خطأ: لم يتم ضبط متطلبات Supabase في متغيرات البيئة (Environment Variables).")
    st.stop()

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# ==========================================
# 1. إعدادات الصفحة وإخفاء الشريط العلوي
# ==========================================
st.set_page_config(
    page_title="BELLONA | بنك الروبي الملكي",
    page_icon="💎",
    layout="centered",
)

# إخفاء الشريط العلوي والقائمة لـ Streamlit
hide_streamlit_style = """
    <style>
    header {visibility: hidden;}
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .block-container {
        padding-top: 1.5rem !important;
    }
    </style>
"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# ==========================================
# 2. محرك الصوت والمؤثرات الحركية (Particles & Sound FX)
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

    /* زر الانتقال لموقع نقاط التفاعل */
    .ruby-site-btn {
        display: block;
        width: 100%;
        text-align: center;
        background: linear-gradient(135deg, #FF4081 0%, #D81B60 100%);
        color: #FFFFFF !important;
        font-weight: 800;
        font-size: 1.1rem;
        padding: 12px 20px;
        border-radius: 16px;
        text-decoration: none !important;
        box-shadow: 0 6px 20px rgba(216, 27, 96, 0.35);
        transition: all 0.3s ease;
        margin-bottom: 20px;
    }

    .ruby-site-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 8px 25px rgba(216, 27, 96, 0.5);
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
# 4. دالّات التعامل مع قاعدة البيانات
# ==========================================
def hash_password(pwd):
    return hashlib.sha256(pwd.strip().encode('utf-8')).hexdigest()

def fetch_user(username):
    res = supabase.table("users").select("*").eq("username", username).execute()
    if res.data:
        return res.data[0]
    return None

# ==========================================
# 5. إدارة الجلسة
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_data"] = None

def refresh_session():
    if st.session_state["logged_in"]:
        st.session_state["user_data"] = fetch_user(
            st.session_state["user_data"]["username"]
        )

# ==========================================
# 6. شاشة تسجيل الدخول + زر موقع نقاط التفاعل الرئيسية
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

    st.markdown(
        f'<a href="{OPALS_SITE_URL}" target="_blank" class="ruby-site-btn">✨ الانتقال إلى موقع نقاط التفاعل (Opal\'s) 🚀</a>',
        unsafe_allow_html=True,
    )

    with st.form("login_form"):
        st.subheader("🔑 تسجيل الدخول لـ حسابك")
        username_in = st.text_input("اسم المستخدم (Username):")
        password_in = st.text_input("كلمة السر:", type="password")

        if st.form_submit_button("🚀 دخول الخزنة الملكية"):
            clean_un = username_in.strip().lower()
            clean_pwd = password_in.strip()
            u_data = fetch_user(clean_un)

            if u_data and (u_data["password_hash"] == hash_password(clean_pwd) or u_data["password_hash"] == clean_pwd):
                st.session_state["logged_in"] = True
                st.session_state["user_data"] = u_data
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("❌ اسم المستخدم أو كلمة السر غير صحيحة.")

    st.warning("🔒 الحسابات يتم إنشاؤها حصراً عن طريق المشرفين (Aurther / Lamino).")
    st.stop()

# ==========================================
# 7. الواجهة الرئيسية (بعد تسجيل الدخول)
# ==========================================
refresh_session()
user = st.session_state["user_data"]

col1, col2 = st.columns([3, 1])
with col1:
    st.markdown(
        "<h2 style='color: #D81B60; font-weight: 900;'>💎 بنك الروبي الملكي</h2>",
        unsafe_allow_html=True,
    )
with col2:
    if st.button("🚪 خروج"):
        st.session_state["logged_in"] = False
        st.session_state["user_data"] = None
        st.rerun()

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

st.markdown(
    f'<a href="{OPALS_SITE_URL}" target="_blank" class="ruby-site-btn">✨ الانتقال إلى موقع نقاط التفاعل (Opal\'s) 🚀</a>',
    unsafe_allow_html=True,
)

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

# --- التبويب 1: التحويل الفوري الإيصال ---
with tabs[0]:
    st.subheader("💸 إجراء تحويل مالي سريع")

    res = supabase.table("users").select("username, display_name").neq("username", user["username"]).execute()
    receivers = res.data or []

    if receivers:
        opts = {f"{r['display_name']} (@{r['username']})": r['username'] for r in receivers}
        sel = st.selectbox("اختر العضو المستلم:", list(opts.keys()))
        rec_un = opts[sel]

        amt = st.number_input("المبلغ المراد تحويله (روبي):", min_value=0.5, value=5.0)
        note = st.text_input("سبب / ملاحظة التحويل:", value="تحويل روبي 💎")

        if st.button("🚀 تحويل الروبي الآن"):
            if user["balance"] < amt:
                st.error("❌ رصيدك الحالي لا يكفي لإتمام التحويل!")
            else:
                supabase.table("users").update({"balance": user["balance"] - amt}).eq("username", user["username"]).execute()
                rec_data = fetch_user(rec_un)
                supabase.table("users").update({"balance": rec_data["balance"] + amt}).eq("username", rec_un).execute()

                now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                supabase.table("transactions").insert({
                    "sender": user["username"],
                    "receiver": rec_un,
                    "amount": amt,
                    "note": note,
                    "timestamp": now
                }).execute()

                st.balloons()
                st.success("✅ تم إتمام التحويل بنجاح!")

                st.markdown(
                    f"""
                    <div class="receipt-box">
                        <h4>📜 إيصال تحويل رقمي معتمد</h4>
                        <p><b>المرسل:</b> @{user['username']} | <b>المستلم:</b> @{rec_un}</p>
                        <p><b>المبلغ المحول:</b> <span style="font-size: 20px; font-weight: 900; color: #D81B60;">{amt:g} روبي 💎</span></p>
                        <p><small>التاريخ والوقت: {now}</small></p>
                    </div>
                """,
                    unsafe_allow_html=True,
                )

                refresh_session()
    else:
        st.info("💡 لا يوجد أعضاء آخرين مسجلين في البنك حالياً.")

# --- التبويب 2: قائمة الأثرياء والإحصائيات ---
with tabs[1]:
    st.subheader("🏆 ترتيب أثرياء بنك الروبي")

    res = supabase.table("users").select("display_name, username, balance").order("balance", desc=True).limit(10).execute()
    users_list = res.data or []

    all_users = supabase.table("users").select("balance").execute().data or []
    total_balance = sum(u["balance"] for u in all_users)
    total_count = len(all_users)

    col_s1, col_s2 = st.columns(2)
    with col_s1:
        st.metric(
            label="🌐 إجمالي الروبي المتداول",
            value=f"{total_balance:,.1f} 💎",
        )
    with col_s2:
        st.metric(label="👥 عدد حسابات الأعضاء", value=f"{total_count}")

    st.markdown("---")
    if users_list:
        df_top = pd.DataFrame(users_list)
        df_top.columns = ["الاسم", "اليوزر", "رصيد الروبي"]
        st.dataframe(df_top, use_container_width=True)

# --- التبويب 3: سحب الحظ اليومي ---
with tabs[2]:
    st.subheader("🎲 عجلة الحظ اليومية")
    st.write("جرب حظك كل 24 ساعة واحصل على مكافأة عشوائية تصل إلى **100 روبي**!")

    today = datetime.datetime.now().strftime("%Y-%m-%d")

    if user.get("last_daily_claim") == today:
        st.warning("⏳ لقد استلمت مكافأتك اليومية بالفعل! عد غداً لتجربة حظك.")
    else:
        if st.button("✨ اطلب مكافأة الحظ اليومية ✨"):
            won = random.randint(1, 100)
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            supabase.table("users").update({
                "balance": user["balance"] + won,
                "last_daily_claim": today
            }).eq("username", user["username"]).execute()

            supabase.table("transactions").insert({
                "sender": "نظام الحظ 🎲",
                "receiver": user["username"],
                "amount": won,
                "note": "مكافأة يومية 🌟",
                "timestamp": now
            }).execute()

            st.balloons()
            st.success(f"🎉 مبروك! ابتسم لك الحظ وحصلت على **{won} روبي** إضافية 💎")
            refresh_session()
            st.rerun()

# --- التبويب 4: سجل المعاملات ---
with tabs[3]:
    st.subheader("📜 سجل التحويلات والاستلام الخاص بك")

    res = supabase.table("transactions").select("*").or_(
        f"sender.eq.{user['username']},receiver.eq.{user['username']}"
    ).order("id", desc=True).execute()
    
    tx_list = res.data or []

    if tx_list:
        df_tx = pd.DataFrame(tx_list)[["sender", "receiver", "amount", "note", "timestamp"]]
        df_tx.columns = ["المرسل", "المستلم", "المبلغ (روبي)", "الملاحظة", "التاريخ والوقت"]
        st.dataframe(df_tx, use_container_width=True)
    else:
        st.info("لا توجد عمليات تحويل أو استلام مسجلة بحسابك.")

# --- التبويب 5: إعدادات الحساب ---
with tabs[4]:
    st.subheader("🔒 إعدادات الحساب والأمان")

    with st.form("pwd_form"):
        st.write("🔑 **تغيير كلمة السر الخاصة بك**")
        c_pwd = st.text_input("كلمة السر الحالية:", type="password")
        n_pwd = st.t
