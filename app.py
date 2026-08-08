import datetime
import hashlib
import random
import pandas as pd
import streamlit as st
from supabase import create_client, Client

# ==========================================
# 1. الاتصال بقاعدة بيانات Supabase
# ==========================================
@st.cache_resource
def init_supabase() -> Client:
    url = st.secrets["SUPABASE_URL"]
    key = st.secrets["SUPABASE_KEY"]
    return create_client(url, key)

supabase = init_supabase()

def hash_password(pwd):
    return hashlib.sha256(pwd.encode()).hexdigest()

# ==========================================
# 2. إعدادات الصفحة والتصميم الملكي
# ==========================================
st.set_page_config(
    page_title="RUBY BANK | بنك الروبي السحابي",
    page_icon="💎",
    layout="centered",
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    
    * { font-family: 'Cairo', sans-serif !important; }

    .stApp {
        background: linear-gradient(135deg, #0F0507 0%, #1A0A0F 40%, #2D0512 80%, #120207 100%) !important;
        color: #FFFFFF !important;
        direction: rtl;
        text-align: right;
    }

    .ruby-card {
        background: linear-gradient(135deg, rgba(155, 17, 30, 0.9) 0%, rgba(210, 4, 45, 0.75) 50%, rgba(80, 0, 20, 0.95) 100%);
        border: 2px solid #FF2A5F;
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 15px 35px rgba(210, 4, 45, 0.4), inset 0 0 20px rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(12px);
        margin-bottom: 25px;
        position: relative;
    }
    
    .card-balance {
        font-size: 3rem;
        font-weight: 900;
        color: #FFFFFF;
        text-shadow: 0 0 25px #FF2A5F, 0 0 10px #FFB7C5;
        margin: 12px 0;
    }

    .card-user { font-size: 1.25rem; font-weight: 800; color: #FFC1E3; }

    .stButton>button {
        background: linear-gradient(90deg, #D2042D 0%, #E0115F 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        border: 1px solid #FF758F !important;
        padding: 12px 24px !important;
        box-shadow: 0 6px 20px rgba(210, 4, 45, 0.4) !important;
        width: 100%;
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
        border: 1px solid #7A1C30 !important;
        border-radius: 12px !important;
    }

    .badge-admin { background: #FFD700; color: #000; padding: 4px 12px; border-radius: 8px; font-weight: 900; }
    .badge-user { background: #E0115F; color: #FFF; padding: 4px 12px; border-radius: 8px; font-weight: 900; }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 3. إدارة الجلسة
# ==========================================
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user_data"] = None

def fetch_user(username):
    res = supabase.table("users").select("*").eq("username", username).execute()
    if res.data:
        u = res.data[0]
        return {
            "username": u["username"],
            "display_name": u["display_name"],
            "balance": float(u["balance"]),
            "role": u["role"],
            "last_daily_claim": u["last_daily_claim"] or "",
        }
    return None

def refresh_session():
    if st.session_state["logged_in"]:
        st.session_state["user_data"] = fetch_user(st.session_state["user_data"]["username"])

# ==========================================
# 4. شاشة تسجيل الدخول
# ==========================================
if not st.session_state["logged_in"]:
    st.markdown("<h1 style='text-align: center; color: #FF2A5F; font-weight: 900;'>💎 RUBY BANK 💎</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #FFB7C5;'>بنك الروبي السحابي | الحسابات محفوظة بشكل دائم</p>", unsafe_allow_html=True)

    with st.form("login_form"):
        st.subheader("🔑 دخول الخزنة المصرفية")
        username_in = st.text_input("اسم المستخدم (Username):")
        password_in = st.text_input("كلمة السر:", type="password")
        submit_login = st.form_submit_button("🚀 تسجيل الدخول")

        if submit_login:
            clean_un = username_in.strip().lower()
            res = supabase.table("users").select("password_hash").eq("username", clean_un).execute()

            if res.data and res.data[0]["password_hash"] == hash_password(password_in):
                st.session_state["logged_in"] = True
                st.session_state["user_data"] = fetch_user(clean_un)
                st.success("تم تسجيل الدخول بنجاح!")
                st.rerun()
            else:
                st.error("❌ اسم المستخدم أو كلمة السر غير صحيحة.")

    st.info("💡 الحسابات تُنشأ حصراً عبر المشرفين.")
    st.caption("حساب الأدمن الافتراضي: admin | كلمة السر: ruby2026")
    st.stop()

# ==========================================
# 5. الواجهة الرئيسية
# ==========================================
refresh_session()
user = st.session_state["user_data"]

col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("💎 بنك الروبي السحابي")
with col_h2:
    if st.button("🚪 خروج"):
        st.session_state["logged_in"] = False
        st.session_state["user_data"] = None
        st.rerun()

role_badge = '<span class="badge-admin">👑 مشرف</span>' if user["role"] == "admin" else '<span class="badge-user">💎 عضو</span>'
st.markdown(
    f"""
    <div class="ruby-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="card-user">👤 {user['display_name']} (@{user['username']})</span>
            {role_badge}
        </div>
        <div class="card-balance">{user['balance']:,.2f} <span style="font-size: 1.5rem;">روبي 💎</span></div>
        <div style="font-size: 11px; color: rgba(255,255,255,0.5);">معرف الحساب السحابي: RB-{hashlib.md5(user['username'].encode()).hexdigest()[:8].upper()}</div>
    </div>
""",
    unsafe_allow_html=True,
)

tabs_list = ["💸 تحويل روبي", "🎲 سحب الحظ اليومي", "📜 سجل المعاملات"]
if user["role"] == "admin":
    tabs_list.append("⚙️ لوحة الإدارة")

tabs = st.tabs(tabs_list)

# --- التبويب 1: تحويل الروبي ---
with tabs[0]:
    st.subheader("💸 تحويل الروبي إلى عضو آخر")
    
    res_users = supabase.table("users").select("username, display_name").neq("username", user["username"]).execute()
    all_receivers = res_users.data if res_users.data else []

    if all_receivers:
        options = {f"{rec['display_name']} (@{rec['username']})": rec['username'] for rec in all_receivers}
        selected_label = st.selectbox("اختر العضو المستلم:", list(options.keys()))
        receiver_username = options[selected_label]

        transfer_amount = st.number_input("المبلغ المراد تحويله (روبي):", min_value=0.5, step=1.0, value=10.0)
        transfer_note = st.text_input("ملاحظة / سبب التحويل:", value="تحويل أخوي 💎")

        if st.button("🚀 إرسال الروبي الآن"):
            if user["balance"] < transfer_amount:
                st.error("❌ رصيدك الحالي لا يكفي لإتمام هذه العملية!")
            else:
                # خصم للمرسل
                new_sender_bal = user["balance"] - transfer_amount
                supabase.table("users").update({"balance": new_sender_bal}).eq("username", user["username"]).execute()

                # إضافة للمستلم
                rec_data = supabase.table("users").select("balance").eq("username", receiver_username).execute()
                new_rec_bal = float(rec_data.data[0]["balance"]) + transfer_amount
                supabase.table("users").update({"balance": new_rec_bal}).eq("username", receiver_username).execute()

                # سجل المعاملة
                now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                supabase.table("transactions").insert({
                    "sender": user["username"],
                    "receiver": receiver_username,
                    "amount": transfer_amount,
                    "note": transfer_note,
                    "timestamp": now_str
                }).execute()

                st.balloons()
                st.success(f"✅ تم تحويل {transfer_amount:g} روبي بنجاح!")
                refresh_session()
                st.rerun()
    else:
        st.info("💡 لا يوجد أعضاء آخرين مسجلين في البنك حالياً.")

# --- التبويب 2: سحب الحظ اليومي ---
with tabs[1]:
    st.subheader("🎲 سحب الحظ اليومي")
    st.write("احصل على مكافأة عشوائية من **1 إلى 100 روبي** مرة واحدة كل 24 ساعة!")

    today_str = datetime.datetime.now().strftime("%Y-%m-%d")

    if user["last_daily_claim"] == today_str:
        st.warning("⏳ لقد استلمت مكافأتك اليومية بالفعل! عد غداً لتجربة حظك.")
    else:
        if st.button("✨ اطلب مكافأة الحظ اليومية ✨"):
            won_amount = random.randint(1, 100)
            new_bal = user["balance"] + won_amount

            supabase.table("users").update({
                "balance": new_bal,
                "last_daily_claim": today_str
            }).eq("username", user["username"]).execute()

            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            supabase.table("transactions").insert({
                "sender": "نظام الحظ 🎲",
                "receiver": user["username"],
                "amount": won_amount,
                "note": "مكافأة الحظ اليومية 🌟",
                "timestamp": now_str
            }).execute()

            st.balloons()
            st.success(f"🎉 مبروك! حصلت اليوم على **{won_amount} روبي** إضافية 💎")
            refresh_session()
            st.rerun()

# --- التبويب 3: سجل المعاملات ---
with tabs[2]:
    st.subheader("📜 سجل عمليات حسابك")
    res_tx = supabase.table("transactions").select("sender, receiver, amount, note, timestamp").or_(f"sender.eq.{user['username']},receiver.eq.{user['username']}").order("id", desc=True).execute()
    
    if res_tx.data:
        df_tx = pd.DataFrame(res_tx.data)
        df_tx.columns = ["المرسل", "المستلم", "المبلغ", "الملاحظة", "التاريخ"]
        st.dataframe(df_tx, use_container_width=True)
    else:
        st.info("لا توجد معاملات مسجلة بحسابك بعد.")

# --- التبويب 4: لوحة الإدارة ---
if user["role"] == "admin":
    with tabs[3]:
        st.subheader("⚙️ لوحة الإشراف والتحكم السحابية")
        admin_action = st.radio("اختر الإجراء المطلوب:", ["➕ إضافة عضو جديد", "💰 تعديل رصيد عضو", "👥 عرض قائمة الأعضاء", "📊 سجل كل المعاملات"], horizontal=True)

        if "إضافة" in admin_action:
            with st.form("add_user_form"):
                st.write("📝 **إنشاء حساب بنكي جديد**")
                new_user = st.text_input("اسم المستخدم (Username):")
                new_pwd = st.text_input("كلمة السر الأولى:", type="password")
                new_dname = st.text_input("الاسم الظاهر:")
                new_bal = st.number_input("الرصيد الافتتاحي (روبي):", min_value=0.0, value=50.0)
                new_role = st.selectbox("الرتبة:", ["user", "admin"])

                if st.form_submit_button("✨ إنشاء الحساب"):
                    if new_user.strip() and new_pwd.strip():
                        clean_un = new_user.strip().lower()
                        check_ex = supabase.table("users").select("username").eq("username", clean_un).execute()
                        if check_ex.data:
                            st.error("❌ اسم المستخدم مسجل مسبقاً!")
                        else:
                            supabase.table("users").insert({
                                "username": clean_un,
                                "password_hash": hash_password(new_pwd),
                                "display_name": new_dname.strip(),
                                "balance": new_bal,
                                "role": new_role
                            }).execute()
                            st.success(f"✅ تم إنشاء حساب @{clean_un} بنجاح وحفظه سحابياً!")

        elif "تعديل" in admin_action:
            res_all_users = supabase.table("users").select("username, balance").execute()
            if res_all_users.data:
                u_list = [u["username"] for u in res_all_users.data]
                target_user = st.selectbox("اختر العضو:", u_list)
                add_sub = st.radio("نوع التعديل:", ["إضافة روبي ➕", "خصم روبي ➖"])
                amount_mod = st.number_input("المبلغ:", min_value=1.0, value=10.0)

                if st.button("✏️ حفظ التعديل"):
                    mod_val = amount_mod if "إضافة" in add_sub else -amount_mod
                    curr_bal = float([u["balance"] for u in res_all_users.data if u["username"] == target_user][0])
                    
                    supabase.table("users").update({"balance": curr_bal + mod_val}).eq("username", target_user).execute()

                    now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    supabase.table("transactions").insert({
                        "sender": "إدارة البنك 👑",
                        "receiver": target_user,
                        "amount": mod_val,
                        "note": "تعديل إداري مباشر",
                        "timestamp": now_str
                    }).execute()
                    st.success("تم تحديث الرصيد وحفظه سحابياً!")
                    st.rerun()

        elif "عرض" in admin_action:
            res_users_all = supabase.table("users").select("username, display_name, balance, role, last_daily_claim").execute()
            if res_users_all.data:
                df_u = pd.DataFrame(res_users_all.data)
                df_u.columns = ["اليوزر", "الاسم", "الرصيد", "الرتبة", "آخر سحب حظ"]
                st.dataframe(df_u, use_container_width=True)

        elif "سجل" in admin_action:
            res_all_tx = supabase.table("transactions").select("*").order("id", desc=True).execute()
            if res_all_tx.data:
                st.dataframe(pd.DataFrame(res_all_tx.data), use_container_width=True)
                
