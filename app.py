import datetime
import hashlib
import random
import sqlite3
import pandas as pd
import streamlit as st

# ==========================================
# 1. إعدادات الصفحة والتصميم الملكي (Opal's Sakura Theme)
# ==========================================
st.set_page_config(
    page_title="BELLONA | بنك الروبي", page_icon="🌸", layout="centered"
)

# تصميم الـ CSS وتأثير تساقط أوراق الكرز
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700;800;900&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Cairo', sans-serif !important;
    }

    .stApp {
        background: linear-gradient(180deg, #FFFFFF 0%, #FFF0F5 50%, #FFE4E1 100%) !important;
        color: #4A0E17 !important;
        direction: rtl;
        text-align: right;
    }

    /* تأثير زهور الكرز (Sakura Animation) */
    @keyframes sakura-fall {
        0% { transform: translateY(-10vh) rotate(0deg); opacity: 0.9; }
        100% { transform: translateY(105vh) rotate(360deg); opacity: 0; }
    }
    
    .sakura-container {
        position: fixed;
        top: 0; left: 0; width: 100%; height: 100%;
        pointer-events: none;
        z-index: 0;
        overflow: hidden;
    }
    
    .petal {
        position: absolute;
        background: #FFB7C5;
        border-radius: 15px 0px 15px 0px;
        opacity: 0.7;
        animation: sakura-fall 8s linear infinite;
    }
    
    .p1 { left: 8%; width: 14px; height: 18px; animation-duration: 7s; animation-delay: 0s; }
    .p2 { left: 22%; width: 10px; height: 14px; animation-duration: 9s; animation-delay: 2s; background: #FFC0CB; }
    .p3 { left: 45%; width: 16px; height: 20px; animation-duration: 6.5s; animation-delay: 1s; }
    .p4 { left: 68%; width: 12px; height: 15px; animation-duration: 8.5s; animation-delay: 3s; background: #FFB6C1; }
    .p5 { left: 85%; width: 15px; height: 18px; animation-duration: 10s; animation-delay: 0.5s; }

    /* بطاقة الروبي المصرفية - تصميم Opal's */
    .ruby-card {
        background: rgba(255, 255, 255, 0.95);
        border: 3px solid #FF80AB;
        border-radius: 24px;
        padding: 25px;
        box-shadow: 0 12px 35px rgba(216, 27, 96, 0.15);
        margin-bottom: 25px;
        position: relative;
    }

    .card-balance {
        font-size: 3rem;
        font-weight: 900;
        color: #D81B60;
        text-shadow: 0px 3px 12px rgba(216, 27, 96, 0.2);
        margin: 10px 0;
    }

    /* الشارات والرتب */
    .badge-aurther {
        background: linear-gradient(135deg, #EC407A 0%, #D81B60 100%);
        color: #FFFFFF;
        padding: 4px 14px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 900;
        box-shadow: 0 4px 10px rgba(216, 27, 96, 0.3);
    }

    .badge-lamino {
        background: #FF80AB;
        color: #FFFFFF;
        padding: 4px 14px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 900;
        box-shadow: 0 4px 10px rgba(255, 128, 171, 0.3);
    }

    .badge-user {
        background: #FFE4E1;
        color: #C2185B;
        padding: 4px 14px;
        border-radius: 12px;
        font-size: 12px;
        font-weight: 800;
        border: 1px solid #FFC1E3;
    }

    /* الأزرار وحقول الإدخال */
    .stButton>button {
        background: linear-gradient(90deg, #EC407A 0%, #D81B60 100%) !important;
        color: #FFFFFF !important;
        font-weight: 800 !important;
        border-radius: 16px !important;
        border: none !important;
        padding: 12px 24px !important;
        box-shadow: 0 4px 18px rgba(216, 27, 96, 0.35) !important;
        width: 100%;
        transition: all 0.25s ease-in-out !important;
    }

    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 22px rgba(216, 27, 96, 0.5) !important;
    }

    .stTextInput input, .stNumberInput input, .stSelectbox div {
        background-color: #FFFFFF !important;
        color: #37474F !important;
        border: 2px solid #FFC1E3 !important;
        border-radius: 14px !important;
    }

    /* تصميم التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px !important;
        background: #FFE4E1 !important;
        padding: 10px 14px !important;
        border-radius: 22px !important;
        border: 2px solid #FF80AB !important;
        box-shadow: 0 8px 25px rgba(216, 27, 96, 0.15) !important;
        justify-content: center !important;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 14px !important;
        background-color: #FFFFFF !important;
        color: #C2185B !important;
        font-weight: 800 !important;
        border: 2px solid #FFC1E3 !important;
        padding: 8px 20px !important;
        transition: all 0.25s ease-in-out !important;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #EC407A 0%, #D81B60 100%) !important;
        color: #FFFFFF !important;
        border: 2px solid #D81B60 !important;
        box-shadow: 0 6px 18px rgba(216, 27, 96, 0.4) !important;
    }

    div[data-baseweb="tab-panel"] {
        background: rgba(255, 255, 255, 0.95) !important;
        border: 2px solid #FFC1E3 !important;
        border-radius: 24px !important;
        padding: 25px !important;
        margin-top: 15px !important;
        box-shadow: 0 10px 30px rgba(216, 27, 96, 0.1) !important;
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

  # إضافة حسابات المشرفين الافتراضية (Aurther & Lamino) برصيد 0 روبي
  admins_to_seed = [
      ("aurther", "iraq2026", "Aurther 👑", 0.0, "admin"),
      ("lamino", "iraq2026", "Lamino 🤝", 0.0, "admin"),
  ]

  for un, pw, dname, bal, role in admins_to_seed:
    c.execute("SELECT username FROM users WHERE username = ?", (un,))
    if not c.fetchone():
      c.execute(
          """
                INSERT INTO users (username, password_hash, display_name, balance, role)
                VALUES (?, ?, ?, ?, ?)
            """,
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
# 4. شاشة تسجيل الدخول
# ==========================================
if not st.session_state["logged_in"]:
  st.markdown(
      "<h1 style='text-align: center; color: #D81B60; font-weight: 900;'>🌸"
      " BELLONA BANK 🌸</h1>",
      unsafe_allow_html=True,
  )
  st.markdown(
      "<p style='text-align: center; color: #C2185B; font-weight: 700;'>✨ نظام"
      " ونقاط عملة الروبي المصرفية ✨</p>",
      unsafe_allow_html=True,
  )

  with st.form("login_form"):
    st.subheader("🔑 تسجيل الدخول إلى الحساب")
    username_in = st.text_input("اسم المستخدم (Username):")
    password_in = st.text_input("كلمة السر:", type="password")
    submit_login = st.form_submit_button("🚀 دخول الخزنة")

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

  st.warning(
      "🔒 الحسابات يتم إنشاؤها حصراً عن طريق المشرفين (Aurther / Lamino)."
  )
  st.stop()

# ==========================================
# 5. الواجهة الرئيسية
# ==========================================
refresh_session()
user = st.session_state["user_data"]

# الهيدر وزر الخروج
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
  st.markdown(
      "<h2 style='color: #D81B60; font-weight: 900;'>💎 بنك الروبي الملكي</h2>",
      unsafe_allow_html=True,
  )
with col_h2:
  if st.button("🚪 خروج"):
    st.session_state["logged_in"] = False
    st.session_state["user_data"] = None
    st.rerun()

# الشارات
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
            <span class="card-user">👤 {user['display_name']} (@{user['username']})</span>
            {role_badge}
        </div>
        <div class="card-balance">{user['balance']:,.2f} <span style="font-size: 1.5rem;">روبي 💎</span></div>
        <div style="font-size: 11px; color: #880E4F; font-weight: 600;">معرف الحساب: RB-{hashlib.md5(user['username'].encode()).hexdigest()[:8].upper()}</div>
    </div>
""",
    unsafe_allow_html=True,
)

# قائمة التبويبات
tabs_list = [
    "💸 التحويل والاستلام",
    "🎲 سحب الحظ اليومي",
    "📜 سجل المعاملات",
    "🔒 إعدادات الحساب",
]
if user["role"] == "admin":
  tabs_list.append("🛡️ لوحة المشرفين")

tabs = st.tabs(tabs_list)

# --- التبويب 1: التحويل والاستلام ---
with tabs[0]:
  st.subheader("💸 إجراء تحويل جديد")

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
        "المبلغ المراد تحويله (روبي):", min_value=0.5, step=1.0, value=5.0
    )
    transfer_note = st.text_input(
        "ملاحظة / سبب التحويل:", value="تحويل روبي 💎"
    )

    if st.button("🚀 إرسال الروبي الآن"):
      if user["balance"] < transfer_amount:
        st.error("❌ رصيدك الحالي لا يكفي لإتمام التحويل!")
      else:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            "UPDATE users SET balance = balance - ? WHERE username = ?",
            (transfer_amount, user["username"]),
        )
        c.execute(
            "UPDATE users SET balance = balance + ? WHERE username = ?",
            (transfer_amount, receiver_username),
        )

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
        st.success(f"✅ تم تحويل {transfer_amount:g} روبي إلى {selected_label}!")
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
  st.subheader("📜 سجل التحويلات والاستلام الخاص بك")

  conn = get_db()
  df_tx = pd.read_sql_query(
      """
        SELECT sender AS 'المرسل', receiver AS 'المستلم', amount AS 'المبلغ (روبي)', note AS 'الملاحظة', timestamp AS 'التاريخ والوقت'
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
    st.info("لا توجد عمليات تحويل أو استلام مسجلة بحسابك.")

# --- التبويب 4: إعدادات الحساب ---
with tabs[3]:
  st.subheader("🔒 إعدادات الحساب والأمان")

  with st.form("change_pwd_form"):
    st.write("🔑 **تغيير كلمة السر الخاصة بك**")
    curr_pwd = st.text_input("كلمة السر الحالية:", type="password")
    new_pwd = st.text_input("كلمة السر الجديدة:", type="password")
    confirm_pwd = st.text_input("تأكيد كلمة السر الجديدة:", type="password")

    if st.form_submit_button("✏️ تحديث كلمة السر"):
      conn = get_db()
      c = conn.cursor()
      c.execute(
          "SELECT password_hash FROM users WHERE username = ?",
          (user["username"],),
      )
      real_hash = c.fetchone()[0]
      conn.close()

      if hash_password(curr_pwd) != real_hash:
        st.error("❌ كلمة السر الحالية غير صحيحة!")
      elif new_pwd.strip() == "":
        st.error("❌ لا يمكن ترك كلمة السر الجديدة فارغة!")
      elif new_pwd != confirm_pwd:
        st.error("❌ كلمة السر الجديدة وتأكيدها غير متطابقين!")
      else:
        conn = get_db()
        c = conn.cursor()
        c.execute(
            "UPDATE users SET password_hash = ? WHERE username = ?",
            (hash_password(new_pwd), user["username"]),
        )
        conn.commit()
        conn.close()
        st.success("✅ تم تغيير كلمة السر بنجاح!")

# --- التبويب 5: لوحة المشرفين ---
if user["role"] == "admin":
  with tabs[4]:
    st.subheader("🛡️ لوحة إدارة الحسابات (المشرفين)")

    admin_action = st.radio(
        "اختر الإجراء المطلوب:",
        [
            "➕ إضافة عضو جديد ويوزره",
            "💰 تعديل رصيد عضو",
            "❌ حذف حساب",
            "👥 عرض قائمة الأعضاء",
        ],
        horizontal=True,
    )

    # 1. إضافة عضو جديد
    if "إضافة" in admin_action:
      with st.form("add_user_form"):
        st.write("📝 **إنشاء حساب جديد وتعيين اسم المستخدم وكلمة السر**")
        new_user = st.text_input("اسم المستخدم (Username بالعربي أو الإنجليزي):")
        new_pwd = st.text_input("كلمة السر الأولى:", type="password")
        new_dname = st.text_input("الاسم الظاهر للعضو:")
        new_bal = st.number_input(
            "الرصيد الافتتاحي (روبي):", min_value=0.0, value=0.0
        )
        new_role = st.selectbox(
            "نوع الحساب:", ["user", "admin"], format_func=lambda x: "عضو" if x == "user" else "مشرف"
        )

        if st.form_submit_button("✨ إنشاء الحساب وإعطاؤه للعضو"):
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
        amount_mod = st.number_input("المبلغ:", min_value=0.5, value=10.0)

        if st.button("✏️ تطبيق التعديل"):
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
                  f"المشرف (@{user['username']})",
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

    # 3. حذف حساب
    elif "حذف" in admin_action:
      conn = get_db()
      df_del = pd.read_sql_query(
          "SELECT username, display_name FROM users WHERE username NOT IN"
          " ('aurther', 'lamino')",
          conn,
      )
      conn.close()

      if not df_del.e
