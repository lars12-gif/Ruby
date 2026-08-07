import datetime
import hashlib
import random
import sqlite3
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. إعدادات الصفحة والتصميم الملكي (Ruby Theme)
# ==========================================
st.set_page_config(
    page_title="RUBY BANK | بنك الروبي الملكي",
    page_icon="💎",
    layout="centered",
)

# تصميم الـ CSS الخاص بالثيم الياقوتي والزجاجي
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    
    * {
        font-family: 'Cairo', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(135deg, #0F0507 0%, #1A0A0F 40%, #2D0512 80%, #120207 100%) !important;
        color: #FFFFFF !important;
        direction: rtl;
        text-align: right;
    }

    /* بطاقة الروبي الملكية */
    .ruby-card {
        background: linear-gradient(135deg, rgba(155, 17, 30, 0.9) 0%, rgba(210, 4, 45, 0.75) 50%, rgba(80, 0, 20, 0.95) 100%);
        border: 2px solid #FF2A5F;
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 15px 35px rgba(210, 4, 45, 0.4), inset 0 0 20px rgba(255, 255, 255, 0.2);
        backdrop-filter: blur(12px);
        margin-bottom: 25px;
        position: relative;
        overflow: hidden;
    }
    
    .ruby-card::before {
        content: "💎 RUBY BANK VAULT";
        position: absolute;
        top: 15px;
        left: 20px;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: 2px;
        color: rgba(255, 255, 255, 0.4);
    }

    .card-balance {
        font-size: 3rem;
        font-weight: 900;
        color: #FFFFFF;
        text-shadow: 0 0 25px #FF2A5F, 0 0 10px #FFB7C5;
        margin: 12px 0;
    }

    .card-user {
        font-size: 1.25rem;
        font-weight: 800;
        color: #FFC1E3;
    }

    /* أزرار مخصصة */
    .stButton>button {
        background: linear-gradient(90deg, #D2042D 0%, #E0115F 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        border-radius: 14px !important;
        border: 1px solid #FF758F !important;
        padding: 12px 24px !important;
        box-shadow: 0 6px 20px rgba(210, 4, 45, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100%;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 25px rgba(224, 17, 95, 0.6) !important;
    }

    /* حقول الإدخال */
    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: rgba(255, 255, 255, 0.08) !important;
        color: #FFFFFF !important;
        border: 1px solid #7A1C30 !important;
        border-radius: 12px !important;
    }

    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: #FF2A5F !important;
        box-shadow: 0 0 12px rgba(255, 42, 95, 0.5) !important;
    }

    .badge-admin {
        background: #FFD700;
        color: #000;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 900;
    }

    .badge-user {
        background: #E0115F;
        color: #FFF;
        padding: 4px 12px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 900;
    }

    /* تصميم التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: rgba(255, 255, 255, 0.05);
        padding: 10px;
        border-radius: 18px;
        border: 1px solid #500014;
        justify-content: center;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 12px;
        color: #FFB7C5 !important;
        font-weight: 700;
        padding: 8px 18px !important;
    }

    .stTabs [aria-selected="true"] {
        background: #D2042D !important;
        color: #FFFFFF !important;
        box-shadow: 0 4px 15px rgba(210, 4, 45, 0.5) !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)

# ==========================================
# 2. إدارة قاعدة البيانات (SQLite)
# ==========================================
DB_FILE = "ruby_bank.db"


def get_db():
  return sqlite3.connect(DB_FILE, check_same_thread=False)


def hash_password(pwd):
  return hashlib.sha256(pwd.encode()).hexdigest()


def init_db():
  conn = get_db()
  c = conn.cursor()

  # جدول المستخدمين
  c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            display_name TEXT NOT NULL,
            balance REAL DEFAULT 0,
            role TEXT DEFAULT 'user',
            last_daily_claim TEXT DEFAULT ''
        )
    """)

  # جدول المعاملات
  c.execute("""
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receiver TEXT,
            amount REAL,
            note TEXT,
            timestamp TEXT
        )
    """)

  # إنشاء حساب المشرف الافتراضي عند التشغيل الأول
  c.execute("SELECT * FROM users WHERE username = 'admin'")
  if not c.fetchone():
    c.execute(
        """
            INSERT INTO users (username, password_hash, display_name, balance, role)
            VALUES (?, ?, ?, ?, ?)
        """,
        (
            "admin",
            hash_password("ruby2026"),
            "المشرف العام 👑",
            10000.0,
            "admin",
        ),
    )

  conn.commit()
  conn.close()


init_db()

# ==========================================
# 3. إدارة الجلسة والوظائف الأساسية
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
# 4. شاشة تسجيل الدخول
# ==========================================
if not st.session_state["logged_in"]:
  st.markdown(
      "<h1 style='text-align: center; color: #FF2A5F; font-weight: 900;'>"
      "💎 RUBY BANK 💎</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: #FFB7C5;'>مرحباً بك في النظام"
      " المصرفي لعملة الروبي الملكية</p>",
      unsafe_allow_html=True,
  )

  with st.form("login_form"):
    st.subheader("🔑 دخول الخزنة المصرفية")
    username_in = st.text_input("اسم المستخدم (Username):")
    password_in = st.text_input("كلمة السر:", type="password")
    submit_login = st.form_submit_button("🚀 تسجيل الدخول")

    if submit_login:
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
        st.error("❌ اسم المستخدم أو كلمة السر غير صحيحة.")

  st.info("💡 الحسابات تُنشأ حصراً عبر المشرفين. تواصل مع الإدارة لاستلام حسابك.")
  st.caption("حساب الأدمن الافتراضي: admin | كلمة السر: ruby2026")
  st.stop()

# ==========================================
# 5. الواجهة الرئيسية للبنك
# ==========================================
refresh_session()
user = st.session_state["user_data"]

# الهيدر وزر الخروج
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
  st.title("💎 بنك الروبي")
with col_h2:
  if st.button("🚪 خروج"):
    st.session_state["logged_in"] = False
    st.session_state["user_data"] = None
    st.rerun()

# عرض بطاقة الروبي البنكية
role_badge = (
    '<span class="badge-admin">👑 مشرف</span>'
    if user["role"] == "admin"
    else '<span class="badge-user">💎 عضو</span>'
)
st.markdown(
    f"""
    <div class="ruby-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <span class="card-user">👤 {user['display_name']} (@{user['username']})</span>
            {role_badge}
        </div>
        <div class="card-balance">{user['balance']:,.2f} <span style="font-size: 1.5rem;">روبي 💎</span></div>
        <div style="font-size: 11px; color: rgba(255,255,255,0.5);">معرف الحساب: RB-{hashlib.md5(user['username'].encode()).hexdigest()[:8].upper()}</div>
    </div>
""",
    unsafe_allow_html=True,
)

# التبويبات المتاحة
tabs_list = [
    "💸 تحويل روبي",
    "🎲 سحب الحظ اليومي",
    "📜 سجل المعاملات",
]
if user["role"] == "admin":
  tabs_list.append("⚙️ لوحة الإدارة")

tabs = st.tabs(tabs_list)

# --- التبويب 1: تحويل الروبي ---
with tabs[0]:
  st.subheader("💸 تحويل الروبي إلى عضو آخر")

  conn = get_db()
  c = conn.cursor()
  c.execute(
      "SELECT username, display_name FROM users WHERE username != ?",
      (user["username"],),
  )
  all_receivers = c.fetchall()
  conn.close()

  if all_receivers:
    options = {f"{rec[1]} (@{rec[0]})": rec[0] for rec in all_receivers}
    selected_label = st.selectbox("اختر العضو المستلم:", list(options.keys()))
    receiver_username = options[selected_label]

    transfer_amount = st.number_input(
        "المبلغ المراد تحويله (روبي):", min_value=0.5, step=1.0, value=10.0
    )
    transfer_note = st.text_input(
        "ملاحظة / سبب التحويل:", value="تحويل أخوي 💎"
    )

    if st.button("🚀 إرسال الروبي الآن"):
      if user["balance"] < transfer_amount:
        st.error("❌ رصيدك الحالي لا يكفي لإتمام هذه العملية!")
      else:
        conn = get_db()
        c = conn.cursor()

        # خصم وإضافة
        c.execute(
            "UPDATE users SET balance = balance - ? WHERE username = ?",
            (transfer_amount, user["username"]),
        )
        c.execute(
            "UPDATE users SET balance = balance + ? WHERE username = ?",
            (transfer_amount, receiver_username),
        )

        # تسجيل السجل
        now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute(
            """
            INSERT INTO transactions (sender, receiver, amount, note, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """,
            (
                user["username"],
                receiver_username,
                transfer_amount,
                transfer_note,
                now_str,
            ),
        )

        conn.commit()
        conn.close()

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

      conn = get_db()
      c = conn.cursor()
      c.execute(
          """
            UPDATE users 
            SET balance = balance + ?, last_daily_claim = ? 
            WHERE username = ?
        """,
          (won_amount, today_str, user["username"]),
      )

      now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
      c.execute(
          """
            INSERT INTO transactions (sender, receiver, amount, note, timestamp)
            VALUES (?, ?, ?, ?, ?)
        """,
          (
              "نظام الحظ 🎲",
              user["username"],
              won_amount,
              "مكافأة الحظ اليومية 🌟",
              now_str,
          ),
      )

      conn.commit()
      conn.close()

      st.balloons()
      st.success(
          f"🎉 مبروك! حصلت اليوم على **{won_amount} روبي** إضافية 💎"
      )
      refresh_session()
      st.rerun()

# --- التبويب 3: سجل المعاملات ---
with tabs[2]:
  st.subheader("📜 سجل عمليات حسابك")

  conn = get_db()
  df_tx = pd.read_sql_query(
      """
        SELECT sender AS 'المرسل', receiver AS 'المستلم', amount AS 'المبلغ', note AS 'الملاحظة', timestamp AS 'التاريخ'
        FROM transactions 
        WHERE sender = ? OR receiver = ?
        ORDER BY id DESC
    """,
      conn,
      params=(user["username"], user["username"]),
  )
  conn.close()

  if not df_tx.empty:
    st.dataframe(df_tx, use_container_width=True)
  else:
    st.info("لا توجد معاملات مسجلة بحسابك بعد.")

# --- التبويب 4: لوحة الإدارة (للمشرفين) ---
if user["role"] == "admin":
  with tabs[3]:
    st.subheader("⚙️ لوحة الإشراف والتحكم")

    admin_action = st.radio(
        "اختر الإجراء المطلوب:",
        [
            "➕ إضافة عضو جديد",
            "💰 تعديل رصيد عضو",
            "👥 عرض قائمة الأعضاء",
            "📊 سجل كل المعاملات",
        ],
        horizontal=True,
    )

    # 1. إضافة عضو جديد
    if "إضافة" in admin_action:
      with st.form("add_user_form"):
        st.write("📝 **إنشاء حساب بنكي جديد**")
        new_user = st.text_input("اسم المستخدم (Username):")
        new_pwd = st.text_input("كلمة السر الأولى:", type="password")
        new_dname = st.text_input("الاسم الظاهر (مثال: عبد الرحمن):")
        new_bal = st.number_input(
            "الرصيد الافتتاحي (روبي):", min_value=0.0, value=50.0
        )
        new_role = st.selectbox("الرتبة:", ["user", "admin"])

        if st.form_submit_button("✨ إنشاء الحساب"):
          if new_user.strip() and new_pwd.strip():
            clean_un = new_user.strip().lower()
            conn = get_db()
            c = conn.cursor()
            try:
              c.execute(
                  """
                                INSERT INTO users (username, password_hash, display_name, balance, role)
                                VALUES (?, ?, ?, ?, ?)
                            """,
                  (
                      clean_un,
                      hash_password(new_pwd),
                      new_dname.strip(),
                      new_bal,
                      new_role,
                  ),
              )
              conn.commit()
              st.success(f"✅ تم إنشاء حساب @{clean_un} بنجاح!")
            except sqlite3.IntegrityError:
              st.error("❌ اسم المستخدم هذا مسجل مسبقاً!")
            finally:
              conn.close()

    # 2. تعديل رصيد
    elif "تعديل" in admin_action:
      conn = get_db()
      df_u = pd.read_sql_query(
          "SELECT username, display_name, balance FROM users", conn
      )
      conn.close()

      if not df_u.empty:
        target_user = st.selectbox("اختر العضو:", df_u["username"])
        add_sub = st.radio("نوع التعديل:", ["إضافة روبي ➕", "خصم روبي ➖"])
        amount_mod = st.number_input("المبلغ:", min_value=1.0, value=10.0)

        if st.button("✏️ حفظ التعديل"):
          mod_val = amount_mod if "إضافة" in add_sub else -amount_mod

          conn = get_db()
          c = conn.cursor()
          c.execute(
              "UPDATE users SET balance = balance + ? WHERE username = ?",
              (mod_val, target_user),
          )

          now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
          c.execute(
              """
                        INSERT INTO transactions (sender, receiver, amount, note, timestamp)
                        VALUES (?, ?, ?, ?, ?)
                    """,
              (
                  "إدارة البنك 👑",
                  target_user,
                  mod_val,
                  "تعديل إداري مباشر",
                  now_str,
              ),
          )

          conn.commit()
          conn.close()
          st.success("تم تعديل الرصيد بنجاح!")
          st.rerun()

    # 3. عرض كافة الأعضاء
    elif "عرض" in admin_action:
      conn = get_db()
      df_all = pd.read_sql_query(
          "SELECT username AS 'اليوزر', display_name AS 'الاسم', balance AS"
          " 'الرصيد', role AS 'الرتبة', last_daily_claim AS 'آخر سحب حظ' FROM"
          " users",
          conn,
      )
      conn.close()
      st.dataframe(df_all, use_container_width=True)

    # 4. سجل الكل
    elif "سجل" in admin_action:
      conn = get_db()
      df_all_tx = pd.read_sql_query(
          "SELECT * FROM transactions ORDER BY id DESC", conn
      )
      conn.close()
      st.dataframe(df_all_tx, use_container_width=True)
      
