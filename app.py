import streamlit as st
from services.auth import authenticate
from services.db import init_db, get_db
from services.calculations import landed_cost
from services.audit import audit
from services.legal import seed_sources, source_rows
from services.crm import add_client, list_clients, add_dossier, list_dossiers

st.set_page_config(
    page_title="Business Gate DZ | Enterprise",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

init_db()
seed_sources()

# ---------------- Brand / CSS ----------------
st.markdown("""
<style>
:root { --navy:#0A1F44; --gold:#C8A951; --cyan:#00C2CB; }
.block-container {padding-top: 1.2rem; max-width: 1500px;}
.bg-title {font-size:2.2rem;font-weight:800;color:#0A1F44;margin-bottom:0;}
.bg-sub {color:#64748b;margin-top:-8px;}
.badge {padding:4px 9px;border-radius:20px;background:#eef2ff;font-size:.8rem;}
</style>
""", unsafe_allow_html=True)

if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    st.markdown('<p class="bg-title">Business Gate DZ</p>', unsafe_allow_html=True)
    st.markdown('<p class="bg-sub">Enterprise Customs • Trade • Tourism • Investment • Compliance</p>', unsafe_allow_html=True)
    st.divider()
    with st.form("login"):
        username = st.text_input("اسم المستخدم")
        password = st.text_input("كلمة المرور", type="password")
        submitted = st.form_submit_button("دخول", type="primary")
        if submitted:
            user = authenticate(username, password)
            if user:
                st.session_state.user = user
                audit("LOGIN", "SYSTEM", username)
                st.rerun()
            else:
                st.error("بيانات الدخول غير صحيحة.")
    st.info("النسخة الافتراضية مهيأة لحساب المدير الأول. غيّر كلمة المرور قبل الاستخدام الفعلي.")
    st.stop()

user = st.session_state.user
with st.sidebar:
    st.markdown("## ⚖️ Business Gate DZ")
    st.caption(f"المستخدم: {user['username']} • الدور: {user['role']}")
    menu = st.radio("المنظومة", [
        "لوحة القيادة","العملاء","الملفات","التكلفة الجمركية",
        "السياحة والسفر","رحلات الأعمال والتوريد","الاستثمار",
        "المطابقة والامتثال","المصادر القانونية","التدقيق"
    ])
    st.divider()
    if st.button("تسجيل الخروج"):
        audit("LOGOUT", "SYSTEM", user["username"])
        st.session_state.user = None
        st.rerun()

st.markdown('<p class="bg-title">Business Gate DZ</p>', unsafe_allow_html=True)
st.markdown('<p class="bg-sub">منصة تشغيلية خاصة لإدارة التجارة الدولية والخدمات الجمركية والسياحية والاستثمارية</p>', unsafe_allow_html=True)

if menu == "لوحة القيادة":
    c1,c2,c3,c4 = st.columns(4)
    clients = list_clients()
    dossiers = list_dossiers()
    c1.metric("العملاء", len(clients))
    c2.metric("الملفات", len(dossiers))
    c3.metric("المصادر القانونية", len(source_rows()))
    c4.metric("حالة النظام", "PROTECTED")
    st.divider()
    st.subheader("دورة العمل المقترحة")
    st.write("Lead → Client → Dossier → Quote → Payment → Service Delivery → Compliance → Invoice → Follow-up")
    st.warning("هذا النظام أداة قرار ومراقبة مهنية. لا يعتبر بديلاً عن التحقق النهائي من النص الرسمي الساري أو قرار الإدارة المختصة.")

elif menu == "العملاء":
    st.subheader("CRM — العملاء")
    with st.form("client"):
        a,b = st.columns(2)
        name = a.text_input("اسم العميل / الشركة")
        phone = b.text_input("الهاتف")
        email = a.text_input("البريد")
        country = b.text_input("الدولة", value="Algeria")
        if st.form_submit_button("حفظ العميل"):
            cid = add_client(name, phone, email, country)
            audit("CREATE_CLIENT","CLIENT",cid)
            st.success(f"تم الحفظ: {cid}")
    st.dataframe(list_clients(), use_container_width=True, hide_index=True)

elif menu == "الملفات":
    st.subheader("Dossiers — ملف موحد للعميل")
    clients = list_clients()
    names = {x["name"]: x["id"] for x in clients}
    if not names:
        st.info("أضف عميلاً أولاً.")
    else:
        with st.form("dossier"):
            client_name = st.selectbox("العميل", list(names))
            service = st.selectbox("الخدمة", [
                "Customs","Import/Export","Tourism","Business Travel",
                "Sourcing","Investment","Logistics","Compliance"
            ])
            title = st.text_input("عنوان الملف")
            if st.form_submit_button("إنشاء ملف"):
                did = add_dossier(names[client_name], service, title)
                audit("CREATE_DOSSIER","DOSSIER",did)
                st.success(f"تم إنشاء الملف: {did}")
    st.dataframe(list_dossiers(), use_container_width=True, hide_index=True)

elif menu == "التكلفة الجمركية":
    st.subheader("Landed Cost Engine")
    st.caption("المحرك لا يفترض نسباً قانونية. أدخل النسب الموثقة من قاعدة التعريفة أو مصدر رسمي.")
    a,b,c = st.columns(3)
    fob = a.number_input("FOB", min_value=0.0)
    freight = b.number_input("الشحن", min_value=0.0)
    insurance = c.number_input("التأمين", min_value=0.0)
    d,e,f = st.columns(3)
    dd = d.number_input("DD %", min_value=0.0, max_value=100.0)
    daps = e.number_input("DAPS %", min_value=0.0, max_value=100.0)
    tic = f.number_input("TIC %", min_value=0.0, max_value=100.0)
    tva = st.number_input("TVA %", min_value=0.0, max_value=100.0, value=19.0)
    if st.button("احسب", type="primary"):
        result = landed_cost(fob, freight, insurance, dd, daps, tic, tva)
        st.json(result)
        audit("CALCULATE_LANDED_COST","CALCULATION",json.dumps(result, ensure_ascii=False))

elif menu == "السياحة والسفر":
    st.subheader("Tourism Agency — إدارة الرحلات")
    st.write("إدارة عروض السفر، المسافرين، الفنادق، الرحلات، النقل، التأمين، التأشيرات، البرامج، المدفوعات والعقود.")
    a,b,c = st.columns(3)
    a.metric("Modules","Flights / Hotels / Visa")
    b.metric("Operations","Transfers / Insurance")
    c.metric("Commercial","Quotes / Payments")
    st.info("أضف الموردين والأسعار والعقود في مرحلة البيانات التشغيلية قبل إصدار عرض للعميل.")

elif menu == "رحلات الأعمال والتوريد":
    st.subheader("B2B Business Travel & Sourcing")
    st.write("ملف رحلة أعمال: الهدف، الموردون، اجتماعات B2B، الأسواق، المترجم، النقل، الفندق، التأشيرة، الاستشارة الجمركية، العينات، وتقرير ما بعد الرحلة.")
    st.code("Algeria → Guangzhou / Istanbul → Meetings → Sourcing → Customs Review → Landed Cost → Follow-up")

elif menu == "الاستثمار":
    st.subheader("Investment Facilitation")
    st.write("Investor → Project → Registration → Incentive Eligibility → Equipment → Import → Logistics → Compliance → Follow-up")
    st.warning("لا يتم اعتبار أي إعفاء أو حافز مضموناً بمجرد اختيار AAPI؛ الأهلية والنظام والحالة والتسجيل والنص الساري يجب التحقق منها.")

elif menu == "المطابقة والامتثال":
    st.subheader("Compliance Gate")
    checks = [
        "HS classification verified",
        "Commercial activity compatible",
        "Origin verified",
        "Invoice / Incoterm verified",
        "Conformity documents checked",
        "Prior authorization checked where applicable",
        "Customs/tax rates sourced",
        "Investment incentive eligibility verified",
        "Effective date checked",
        "Human legal review completed",
    ]
    for item in checks:
        st.checkbox(item, key=item)
    st.error("لا تستخدم كلمة «متوافق كلياً» إلا بعد اكتمال الأدلة والمراجعة البشرية.")

elif menu == "المصادر القانونية":
    st.subheader("Legal Source Registry")
    st.caption("المصادر أدناه مرجعية؛ يجب تحديثها ومراجعتها عند تغير النصوص.")
    st.dataframe(source_rows(), use_container_width=True, hide_index=True)

elif menu == "التدقيق":
    st.subheader("Audit Trail")
    with get_db() as con:
        rows = con.execute("SELECT ts, action, entity, ref, user FROM audit_log ORDER BY id DESC LIMIT 200").fetchall()
    st.dataframe([dict(r) for r in rows], use_container_width=True, hide_index=True)
