import io
import os
import streamlit as st
import pandas as pd
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import arabic_reshaper
from bidi.algorithm import get_display

# إعداد الصفحة وتكوين واجهة Streamlit
st.set_page_config(
    page_title="Business Gate DZ - محرك التصفية الجمركية 2026",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تنسيق التصميم العام CSS
st.markdown("""
    <style>
    .main-header { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 20px; }
    .sub-header { font-size: 18px; font-weight: bold; color: #3B82F6; margin-top: 15px; }
    .card { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 15px; }
    .metric-box { background-color: #EFF6FF; padding: 15px; border-radius: 8px; border-left: 5px solid #3B82F6; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-header">بوابة الأعمال للخدمات الجمركية والاستثمار - Business Gate DZ (2026)</div>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center; color: #64748B;">المنظومة الاحترافية المتكاملة للتصفية الجمركية، حساب تكاليف الاستيراد، ومحرك رُجيمات السيارات وفق التشريعات الجبائية الجزائرية</p>', unsafe_allow_html=True)
st.markdown("---")

# القائمة الجانبية لاختيار الوحدة
with st.sidebar:
    st.image("https://img.icons8.com/color/96/customs.png", width=80)
    st.markdown("### خيارات المنظومة")
    app_mode = st.radio(
        "اختر النظام المطلوب:",
        ["محرك تصفية البضائع العامة", "محرك رُجيمات السيارات (Automotive)", "حاسبة تكاليف الموانئ و Incoterms"]
    )
    st.markdown("---")
    st.info("إصدار المنظومة: 2.5 (النسخة الاحترافية المعتمدة)")

# ==========================================
# الوحدة الأولى: محرك تصفية البضائع العامة
# ==========================================
if app_mode == "محرك تصفية البضائع العامة":
    st.markdown("### 📦 محرك حساب الرسوم الجمركية والجبائية للبضائع العامة")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### البيانات الأساسية للشحنة")
        hs_code = st.text_input("البند الجمركي (HS Code)", "8471.30.00")
        good_desc = st.text_input("وصف البضاعة", "أجهزة معالجة بيانات رقمية (حواسيب محمولة)")
        fob_val = st.number_input("قيمة البضاعة FOB (بالعملة الأجنبية)", min_value=0.0, value=10000.0, step=500.0)
        currency = st.selectbox("العملة", ["EUR", "USD", "CNY", "GBP"])
        
        # أسعار الصرف التقريبية 2026
        exchange_rates = {"EUR": 145.0, "USD": 135.0, "CNY": 18.5, "GBP": 172.0}
        ex_rate = st.number_input("سعر الصرف (DZD مقابل العملة)", value=exchange_rates.get(currency, 145.0), step=0.5)
        
        freight = st.number_input("تكلفة الشحن الدولي (Freight - DZD)", min_value=0.0, value=150000.0, step=10000.0)
        insurance = st.number_input("تكلفة التأمين (Insurance - DZD)", min_value=0.0, value=25000.0, step=1000.0)

    with col2:
        st.markdown("#### نسب الرسوم والضرائب (المعدلات المعمول بها)")
        dd_rate = st.slider("الحقوق الجمركية (DD %)", 0.0, 30.0, 5.0, 0.5)
        daps_rate = st.slider("الرسم الإضافي المؤقت الوقائي (DAPS %)", 0.0, 60.0, 0.0, 5.0)
        tic_rate = st.slider("الرسم الداخلي للاستهلاك (TIC %)", 0.0, 100.0, 0.0, 5.0)
        tpi_rate = st.slider("رسم الحماية المؤقت (TPI %)", 0.0, 30.0, 0.0, 5.0)
        tva_rate = st.selectbox("الرسم على القيمة المضافة (TVA %)", [19.0, 9.0, 0.0], index=0)

    if st.button("تنفيذ الحساب والتحليل المالي للشحنة", type="primary"):
        fob_dzd = fob_val * ex_rate
        cif_dzd = fob_dzd + freight + insurance
        
        # الحسابات الجمركية والجبائية
        dd_val = cif_dzd * (dd_rate / 100.0)
        daps_val = cif_dzd * (daps_rate / 100.0)
        tpi_val = cif_dzd * (tpi_rate / 100.0)
        
        # الرسم الداخلي للاستهلاك يُحسب على (CIF + DD)
        base_tic = cif_dzd + dd_val
        tic_val = base_tic * (tic_rate / 100.0)
        
        # وعاء TVA يُحسب على المجموع (CIF + DD + DAPS + TIC + TPI)
        base_tva = cif_dzd + dd_val + daps_val + tic_val + tpi_val
        tva_val = base_tva * (tva_rate / 100.0)
        
        # مساهمة التضامن ورسم المعلوماتية
        cs_val = cif_dzd * 0.004  # 0.4%
        inf_val = 2500.0          # رسم المعلوماتية الثابت
        
        total_duties = dd_val + daps_val + tic_val + tpi_val + tva_val + cs_val + inf_val
        total_cost = cif_dzd + total_duties

        st.markdown("---")
        st.markdown("### 📊 نتائج التصفية الجمركية والمالية")
        
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric("القيمة الجمركية (CIF DZD)", f"{cif_dzd:,.2f} دج")
        with m2:
            st.metric("إجمالي الحقوق والضرائب", f"{total_duties:,.2f} دج")
        with m3:
            st.metric("التكلفة الإجمالية للبضاعة", f"{total_cost:,.2f} دج")

        # تفصيل الرسوم في جدول
        df_results = pd.DataFrame({
            "العنصر الجبائي": [
                "القيمة الجمركية (CIF)",
                "الحقوق الجمركية (DD)",
                "الرسم الإضافي المؤقت (DAPS)",
                "رسم الحماية المؤقت (TPI)",
                "الرسم الداخلي للاستهلاك (TIC)",
                "مساهمة التضامن (CS)",
                "رسم المعلوماتية",
                "الرسم على القيمة المضافة (TVA)",
                "إجمالي الرسوم والضرائب المستحقة"
            ],
            "النسبة المطبقة": [
                "-", f"{dd_rate}%", f"{daps_rate}%", f"{tpi_rate}%", f"{tic_rate}%", "0.4%", "ثابت", f"{tva_rate}%", "-"
            ],
            "المبلغ بالدينار الجزائري (DZD)": [
                f"{cif_dzd:,.2f}", f"{dd_val:,.2f}", f"{daps_val:,.2f}", f"{tpi_val:,.2f}",
                f"{tic_val:,.2f}", f"{cs_val:,.2f}", f"{inf_val:,.2f}", f"{tva_val:,.2f}", f"{total_duties:,.2f}"
            ]
        })
        st.table(df_results)

# ==========================================
# الوحدة الثانية: محرك رُجيمات السيارات
# ==========================================
elif app_mode == "محرك رُجيمات السيارات (Automotive)":
    st.markdown("### 🚗 محرك حساب رسوم استيراد السيارات (حسب السعة، الوقود، والعمر)")
    
    col1, col2 = st.columns(2)
    with col1:
        vehicle_type = st.selectbox("نوع الاستيراد / النظام الجمركي", [
            "استيراد السيارات الجديدة عبر الوكلاء المعتمدين",
            "استيراد سيارات الأفراد الخواص (أقل من 3 سنوات)",
            "سيارات المعاقين والمجاهدين (إعفاءات تفضيلية)"
        ])
        engine_type = st.selectbox("نوع المحرك وقود", ["بنزين (Essence)", "ديزل (Diesel)", "هجين / كهربائي (Hybrid/EV)"])
        cc_capacity = st.number_input("السعة السنتيمترية للمحرك (CC)", min_value=800, max_value=6000, value=1600, step=100)
        vehicle_fob = st.number_input("سعر شراء السيارة FOB (بالعملة الأجنبية - EUR)", min_value=1000.0, value=18000.0, step=500.0)
        car_ex_rate = st.number_input("سعر الصرف (EUR مقابل DZD)", value=145.0, step=0.5)
        car_freight = st.number_input("تكلفة الشحن والتأمين للسيارة (DZD)", min_value=0.0, value=120000.0, step=10000.0)

    with col2:
        st.markdown("#### المحددات القانونية والجبائية للسيارات")
        car_age_years = st.slider("عمر السيارة (بالسنوات)", 0, 5, 1)
        
        # تحديد الرسوم تلقائياً حسب السعة ونوع المحرك وفق القوانين المعمول بها
        if "أقل من 3 سنوات" in vehicle_type:
            if cc_capacity <= 1800:
                auto_dd, auto_daps, auto_tic = 15.0, 30.0, 5.0
            else:
                auto_dd, auto_daps, auto_tic = 30.0, 60.0, 15.0
        elif "الوكلاء المعتمدين" in vehicle_type:
            auto_dd, auto_daps, auto_tic = 30.0, 30.0, 10.0
        else: # إعفاءات
            auto_dd, auto_daps, auto_tic = 0.0, 0.0, 0.0

        st.info(f"الرسوم المقترحة آلياً للنظام المختار:\n- الحقوق الجمركية (DD): {auto_dd}%\n- DAPS: {auto_daps}%\n- TIC: {auto_tic}%")

    if st.button("حساب الرسوم الجمركية الشاملة للسيارة", type="primary"):
        car_fob_dzd = vehicle_fob * car_ex_rate
        car_cif = car_fob_dzd + car_freight
        
        c_dd = car_cif * (auto_dd / 100.0)
        c_daps = car_cif * (auto_daps / 100.0)
        c_tic = (car_cif + c_dd) * (auto_tic / 100.0)
        c_cs = car_cif * 0.004
        c_inf = 2500.0
        
        # TVA 19%
        c_tva_base = car_cif + c_dd + c_daps + c_tic
        c_tva = c_tva_base * 0.19
        
        total_car_duties = c_dd + c_daps + c_tic + c_cs + c_inf + c_tva
        final_car_cost = car_cif + total_car_duties

        st.markdown("---")
        st.markdown("### 🚘 تفيصيل التكلفة الجمركية للسيارة")
        
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("قيمة CIF السيارة", f"{car_cif:,.2f} دج")
        with c2:
            st.metric("إجمالي رسوم الترخيص والجمارك", f"{total_car_duties:,.2f} دج")
        with c3:
            st.metric("التكلفة النهائية بالجزائر", f"{final_car_cost:,.2f} دج")

        df_car = pd.DataFrame({
            "مكون الرسوم الجبائية": ["قيمة CIF", "الحقوق الجمركية (DD)", "DAPS", "TIC", "مساهمة التضامن (CS)", "رسم المعلوماتية", "الرسم على القيمة المضافة (TVA)", "الإجمالي العام"],
            "المبلغ بالدينار": [
                f"{car_cif:,.2f}", f"{c_dd:,.2f}", f"{c_daps:,.2f}", f"{c_tic:,.2f}",
                f"{c_cs:,.2f}", f"{c_inf:,.2f}", f"{c_tva:,.2f}", f"{total_car_duties:,.2f}"
            ]
        })
        st.table(df_car)

# ==========================================
# الوحدة الثالثة: حساب تكاليف الموانئ و Incoterms
# ==========================================
elif app_mode == "حاسبة تكاليف الموانئ و Incoterms":
    st.markdown("### ⚓ حاسبة تكاليف الموانئ، المناولة، وغرامات التأخير (Incoterms 2020)")
    
    col1, col2 = st.columns(2)
    with col1:
        incoterm = st.selectbox("قاعدة التجارة الدولية (Incoterms 2020)", ["EXW", "FOB", "CFR", "CIF", "DDP"])
        container_type = st.selectbox("نوع الحاوية أو الشحنة", ["حاوية 20 قدم (20' FCL)", "حاوية 40 قدم (40' FCL)", "بضائع مفككة (LCL)"])
        port_days_storage = st.number_input("عدد أيام المكوث في المخزن (Magasinage)", min_value=1, value=10)
        delay_days = st.number_input("عدد أيام تأخير الحاويات بالميناء (Surestaries)", min_value=0, value=3)
    
    with col2:
        st.markdown("#### تقديرات مصاريف الميناء (الجزائر)")
        handling_fee = st.number_input("تكلفة المناولة والعبور بالميناء (DZD)", value=45000.0, step=5000.0)
        daily_storage_rate = 1500.0 if "20" in container_type else 2800.0
        daily_surestarie_rate = 12000.0 if "20" in container_type else 20000.0

    if st.button("حساب تكاليف الميناء والمصاريف الإضافية", type="primary"):
        total_storage = port_days_storage * daily_storage_rate
        total_surestaries = delay_days * daily_surestarie_rate
        total_port_expenses = handling_fee + total_storage + total_surestaries

        st.markdown("---")
        p1, p2, p3 = st.columns(3)
        with p1:
            st.metric("مصاريف المناولة والعبور", f"{handling_fee:,.2f} دج")
        with p2:
            st.metric("تكلفة التخزين (Magasinage)", f"{total_storage:,.2f} دج")
        with p3:
            st.metric("غرامات التأخير (Surestaries)", f"{total_surestaries:,.2f} دج")

        st.success(f"إجمالي المصاريف المينائية الإضافية المستحقة: **{total_port_expenses:,.2f} دج**")

st.markdown("---")
st.markdown("<p style='text-align: center; color: #94A3B8;'>Business Gate DZ - جميع الحقوق محفوظة © 2026 | تطوير هندسي استشاري احترافي</p>", unsafe_allow_html=True)
