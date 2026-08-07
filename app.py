import datetime
import hashlib
import random
import sqlite3
import pandas as pd
import streamlit as st

# ==========================================
# 1. إعدادات الصفحة والتصميم
# ==========================================
st.set_page_config(
    page_title="BELLONA | بنك الروبي", page_icon="🌸", layout="centered"
)

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif !important; }

    .stApp {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF0F5 50%, #FFE4E1 100%) !important;
        color: #4A0E17 !important;
        direction: rtl;
        text-align: right;
    }

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
    
    .p1 { left: 8%; width: 14px; height: 18px; animation-duration: 7s; }
    .p2 { left: 25%; width: 10px; height: 14px; animation-duration: 9s; background: #FFC0CB; }
    .p3 { left: 50%; width: 16px; height: 20px; animation-duration: 6.5s; }
    .p4 { left: 75%; width: 12px; height: 15px; animation-duration: 8.5s; background: #FFB6C1; }

    .ruby-card {
        background: rgba(255, 255, 255, 0.95);
        border: 3px solid #FF80AB;
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 12px 35px rgba(216, 27, 96, 0.15);
        margin-bottom: 25px;
    }

    .card-balance {
        font-size: 3rem; font-weight: 900; color: #D81B60;
        text-shadow: 0px 3px 12px rgba(216, 27, 96, 0.2); margin: 10px 0;
    }

    .badge-aurther {
        background: linear-gradient(135deg, #EC407A 0%, #D81B60 100%);
        color: #FFFFFF; padding: 4px 14px; border-radius: 12px;
        font-size: 12px; font-weight: 900;
    }

    .badge-lamino {
        background: #FF80AB; color: #FFFFFF;
        padding: 4px 14px; border-radius: 12px;
        font-size: 12px; font-weight: 900;
    }

    .badge-user {
        background: #FFE4E1; color: #C2185B;
        padding: 4px 14px; border-radius: 12px;
        font-size: 12px; font-weight: 800; border: 1px solid #FFC1E3;
    }

    .stButton>button {
        background: linear-gradient(90deg, #EC407A 0%, #D81B60 100%) !important;
        color: #FFFFFF !important; font-weight: 800 !important;
        border-radius: 16px !important; border: none !important;
        padding: 12px 24px !important; width: 100%;
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #FFFFFF !important; color: #37474F !important;
        border: 2px solid #FFC1E3 !important; border-radius: 14px !important;
    }

    .stTabs [data-baseweb="tab-list"] {
        gap: 10px !important; background: #FFE4E1 !important;
        padding: 10px !important; border-radius: 22px !important;
        border: 2px solid #FF80AB !important; justify-content: center !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 14px !important; background-color: #FFFFFF !important;
        color: #C2185B !important; font-weight: 800 !important;
        border: 2px solid #FFC1E3 !important; padding: 8px 18px !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #EC407A 0%, #D81B60 100%) !important;
        color: #FFFFFF !important; border: 2px solid #D81B60 !important;
    }

    div[data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #FFC1E3 !important; border-radius: 24px !important;
        padding: 25px !important; margin-top: 15px !important;
    }
    </style>

    <div class="sakura-container">
        <div class="petal p1"></div>
        <div class="petal p2"></div>
        <div class="petal p3"></div>
        <div class="petal p4"></div>
    </div>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. إدارة قاعدة البيانات
# ==========================================
DB_FILE = "ruby_bank.db"


def get_db():
  return sqlite3.connect(DB_FILE, check_same_thread=False)


def hash_password(pwd):
  return hashlib.sha256(pwd.encode()).hexdigest()


def init_db():
  conn = get_db()
  c = conn.cursor()
  c.execute(
      "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY,"
      " password_hash TEXT, display_name TEXT, balance REAL DEFAULT 0, role"
      " TEXT DEFAULT 'user', last_daily_claim TEXT DEFAULT '')"
  )
  c.execute(
      "CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY"
      " AUTOINCREMENT, sender TEXT, receiver TEXT, amount REAL, note TEXT,"
      " timestamp TEXT)"
  )

  admins = [
      ("aurther", "iraq2026", "Aurther 👑", 0.0, "admin"),
      ("lamino", "iraq2026", "Lamino 🤝", 0.0, "admin"),
  ]

  for un, pw, dname, bal, role in admins:
    c.execute("SELECT username FROM users WHERE username = ?", (un,))
    if not c.fetchone():
      c.execute(
          "INSERT INTO users VALUES (?, ?, ?, ?, ?, '')",
          (un, hash_password(pw), dname, bal, role),
      )

  conn.commit()
  conn.close()


init_db()

# ==========================================
# 3. إدارة الجلسة
# ==========================================
if "logged_in" not in st.session_state:
  st.session_state["logged_in"] = False
  st.session_state["user_data"] = None


def fetch_user(username):
  conn = get_db()
  c = conn.cursor()
  c.execute(
      "SELECT username, display_name, balance, role, last_daily_claim FROM"
      " users WHERE username = ?",
      (username,),
  )
  user = c.fetchone()
  conn.close()
  if user:
    return {
        "username": user[0],
        "display_name": user[1],
        "balance": user[2],
        "role": user[3],
        "last_daily_claim": user[4],
    }
  return None


def refresh_session():
  if st.session_state["logged_in"]:
    st.session_state["user_data"] = fetch_user(
        st.session_state["user_data"]["username"]
    )


# ==========================================
# 4. تسجيل الدخول
# ==========================================
if not st.session_state["logged_in"]:
  st.markdown(
      "<h1 style='text-align: center; color: #D81B60; font-weight: 900;'>🌸"
      " BELLONA BANK 🌸</h1>",
      unsafe_allow_html=True,
  )

  with st.form("login_form"):
    st.subheader("🔑 تسجيل الدخول")
    username_in = st.text_input("اسم المستخدم:")
    password_in = st.text_input("كلمة السر:", type="password")

    if st.form_submit_button("🚀 دخول"):
      clean_un = username_in.strip().lower()
      conn = get_db()
      c = conn.cursor()
      c.execute(
          "SELECT password_hash FROM users WHERE username = ?", (clean_un,)
      )
      res = c.fetchone()
      conn.close()

      if res and res[0] == hash_password(password_in):
        st.session_state["logged_in"] = True
        st.session_state["user_data"] = fetch_user(clean_un)
        st.success("تم تسجيل الدخول بنجاح!")
        st.rerun()
      else:
        st.error("❌ بيانات الدخول غير صحيحة.")

  st.warning("🔒 الحسابات تُصنع حصراً من قبل المشرفين (Aurther / Lamino).")
  st.stop()

# ==========================================
# 5. الواجهة الرئيسية
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
  role_badge = '<span class="badge-aurther">🛡️ مشرف</span>'
else:
  role_badge = '<span class="badge-user">💎 عضو</span>'

st.markdown(
    f"""
    <div class="ruby-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span style="font-size: 1.2rem; font-weight: 800;">👤 {user['display_name']} (@{user['username']})</span>
            {role_badge}
        </div>
        <div class="card-balance">{user['balance']:,.2f} <span style="font-size: 1.5rem;">روبي 💎</span></div>
    </div>
""",
    unsafe_allow_html=True,
)

tabs_list = [
    "💸 التحويل والاستلام",
    "🎲 سحب الحظ اليومي",
    "📜 سجل المعاملات",
    "🔒 إعدادات الحساب",
]
if user["role"] == "admin":
  tabs_list.append("🛡️ لوحة المشرفين")

tabs = st.tabs(tabs_list)

# --- التبويب 1 ---
with tabs[0]:
  st.subheader("💸 تحويل روبي")
  conn = get_db()
  c = conn.cursor()
  c.execute(
      "SELECT username, display_name FROM users WHERE username != ?",
      (user["username"],),
  )
  receivers = c.fetchall()
  conn.close()

  if receivers:
    opts = {f"{r[1]} (@{r[0]})": r[0] for r in receivers}
    sel = st.selectbox("المستلم:", list(opts.keys()))
    rec_un = opts[sel]
    amt = st.number_input("المبلغ:", min_value=0.5, value=5.0)
    note = st.text_input("الملاحظة:", value="تحويل روبي 💎")

    if st.button("🚀 إرسال"):
      if user["balance"] < amt:
        st.error("❌ رصيدك غير كافٍ!")
      else:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            "UPDATE users SET balance = balance - ? WHERE username = ?",
            (amt, user["username"]),
        )
        c.execute(
            "UPDATE users SET balance = balance + ? WHERE username = ?",
            (amt, rec_un),
        )
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            "INSERT INTO transactions VALUES (NULL, ?, ?, ?, ?, ?)",
            (user["username"], rec_un, amt, note, now),
        )
        conn.commit()
        conn.close()
        st.success("✅ تم التحويل بنجاح!")
        refresh_session()
        st.rerun()

# --- التبويب 2 ---
with tabs[1]:
  st.subheader("🎲 سحب الحظ اليومي")
  today = datetime.datetime.now().strftime("%Y-%m-%d")

  if user["last_daily_claim"] == today:
    st.warning("⏳ استلمت مكافأتك اليوم بالفعل!")
  else:
    if st.button("✨ اطلب مكافأتك اليومية ✨"):
      won = random.randint(1, 100)
      conn = get_db()
      c = conn.cursor()
      c.execute(
          "UPDATE users SET balance = balance + ?, last_daily_claim = ? WHERE"
          " username = ?",
          (won, today, user["username"]),
      )
      now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      c.execute(
          "INSERT INTO transactions VALUES (NULL, 'نظام الحظ 🎲', ?, ?, 'مكافأة"
          " يومية', ?)",
          (user["username"], won, now),
      )
      conn.commit()
      conn.close()
      st.success(f"🎉 مبروك! حصلت على {won} روبي 💎")
      refresh_session()
      st.rerun()

# --- التبويب 3 ---
with tabs[2]:
  st.subheader("📜 سجل المعاملات")
  conn = get_db()
  df_tx = pd.read_sql_query(
      "SELECT sender AS 'المرسل', receiver AS 'المستلم', amount AS 'المبلغ',"
      " note AS 'الملاحظة', timestamp AS 'التاريخ' FROM transactions WHERE sender"
      " = ? OR receiver = ? ORDER BY id DESC",
      conn,
      params=(user["username"], user["username"]),
  )
  conn.close()

  if not df_tx.empty:
    st.dataframe(df_tx, use_container_width=True)
  else:
    st.info("لا توجد معاملات بعد.")

# --- التبويب 4 ---
with tabs[3]:
  st.subheader("🔒 إعدادات الحساب")
  with st.form("pwd_form"):
    c_pwd = st.text_input("كلمة السر الحالية:", type="password")
    n_pwd = st.text_input("كلمة السر الجديدة:", type="password")
    if st.form_submit_button("✏️ تغيير كلمة السر"):
      conn = get_db()
      c = conn.cursor()
      c.execute(
          "SELECT password_hash FROM users WHERE username = ?",
          (user["username"],),
      )
      real = c.fetchone()[0]
      if hash_password(c_pwd) == real and n_pwd.strip():
        c.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (hash_password(n_pwd), user["username"]),
        )
        conn.commit()
        st.success("✅ تم التغيير بنجاح!")
      else:
        st.error("❌ بيانات غير صحيحة!")
      conn.close()

# --- التبويب 5 (للمشرفين) ---
if user["role"] == "admin":
  with tabs[4]:
    st.subheader("🛡️ لوحة المشرفين")
    act = st.radio(
        "الإجراء:",
        ["➕ إضافة عضو", "💰 تعديل رصيد", "❌ حذف حساب", "👥 عرض الأعضاء"],
        horizontal=True,
    )

    if "إضافة" in act:
      with st.form("add_form"):
        un = st.text_input("اليوزر:")
        pw = st.text_input("الباسوورد:", type="password")
        dn = st.text_input("الاسم:")
        bal = st.number_input("الرصيد:", min_value=0.0, value=0.0)
        rl = st.selectbox("الرتبة:", ["user", "admin"])
        if st.form_submit_button("✨ إنشاء"):
          if un.strip() and pw.strip():
            conn = get_db()
            c = conn.cursor()
            try:
              c.execute(
                  "INSERT INTO users VALUES (?, ?, ?, ?, ?, '')",
                  (un.strip().lower(), hash_password(pw), dn.strip(), bal, rl),
              )
              conn.commit()
              st.success("✅ تم الإنشاء!")
            except:
              st.error("❌ اليوزر موجود مسبقاً!")
            conn.close()

    elif "تعديل" in act:
      conn = get_db()
      df_u = pd.read_sql_query("SELECT username FROM users", conn)
      conn.close()
      if not df_u.empty:
        usr = st.selectbox("العضو:", df_u["username"])
        tp = st.radio("العملية:", ["إضافة ➕", "خصم ➖"])
        val = st.number_input("المبلغ:", min_value=0.5, value=10.0)
        if st.button("✏️ تطبيق"):
          m = val if "إضافة" in tp else -val
          conn = get_db()
          c = conn.cursor()
          c.execute(
              "UPDATE users SET balance = balance + ? WHERE username = ?",
              (m, usr),
          )
          now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          c.execute(
              "INSERT INTO transactions VALUES (NULL, 'المشرف', ?, ?, 'تعديل"
              " إداري', ?)",
              (usr, m, now),
          )
          conn.commit()
          conn.close()
          st.success("تم التحديث!")
          st.rerun()

    elif "حذف" in act:
      conn = get_db()
      df_d = pd.read_sql_query(
          "SELECT username FROM users WHERE username NOT IN ('aurther',"
          " 'lamino')",
          conn,
      )
      conn.close()
      if not df_d.empty:
        dt = st.selectbox("الحساب:", df_d["username"])
        if st.button("🔥 حذف"):
          conn = get_db()
          c = conn.cursor()
          c.execute("DELETE FROM users WHERE username = ?", (dt,))
          conn.commit()
          conn.close()
          st.success("تم الحذف!")
          st.rerun()

    elif "عرض" in act:
      conn = get_db()
      df_all = pd.read_sql_query(
          "SELECT username AS 'اليوزر', display_name AS 'الاسم', balance AS"
          " 'الرصيد', role AS 'الرتبة' FROM users",
          conn,
      )
      conn.close()
      st.dataframe(df_all, use_container_width=True)
