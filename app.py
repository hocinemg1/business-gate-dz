import streamlit as st
import pandas as pd
import numpy as np

# 1. إعداد الصفحة وتكوين واجهة Streamlit بمعايير عالمية
st.set_page_config(
    page_title="Business Gate DZ - المنصة العالمية للاستشارات والتحليل الجمركي",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم الواجهة والأنماط الاحترافية (CSS)
st.markdown("""
    <style>
    .main-header {
        font-size: 2.3rem;
        color: #1E3A8A;
        font-weight: 800;
        text-align: right;
        margin-bottom: 10px;
    }
    .sub-text {
        font-size: 1.1rem;
        color: #475569;
        text-align: right;
        margin-bottom: 25px;
    }
    .metric-card {
        background-color: #F8FAFC;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #E2E8F0;
    }
    </style>
""", unsafe_allow_html=True)

# 3. محرك الحسابات الجمركية والتشريعات المتقدمة (يشمل الإعفاءات، DAPS، TIC، والتعريفات الضخمة)
def advanced_customs_engine(hs_code, fob_value, currency_rate, freight, insurance, dd_rate, daps_rate, tic_rate, tpi_rate, tva_rate, exemption_type):
    """
    محرك مالي وجمركي متقدم يراعي القوانين التفصيلية والاتفاقيات الدولية والتخفيضات الاستثمارية.
    """
    fob_dzd = fob_value * currency_rate
    cif_value = fob_dzd + freight + insurance
    
    # تطبيق الإعفاءات الم, وجهات الاستثمار (مثل وكالة ترقية الاستثمار AAPI أو اتفاقيات التبادل الحر)
    effective_dd_rate = dd_rate
    if exemption_type == "إعفاء كلي في إطار الاستثمار (AAPI / ANEM)":
        effective_dd_rate = 0.0
    elif exemption_type == "تخفيض تفضيلي (اتفاقيات الشراكة / ZLECAf)":
        effective_dd_rate = dd_rate * 0.5  # تخفيض تفضيلي نموذجي
        
    customs_duty = cif_value * (effective_dd_rate / 100.0)
    
    # وعاء وطريقة حساب الرسوم الإضافية والوقائية (DAPS, TIC, TPI)
    base_taxable_daps = cif_value + customs_duty
    daps = base_taxable_daps * (daps_rate / 100.0)
    
    base_taxable_tic = cif_value + customs_duty + daps
    tic = base_taxable_tic * (tic_rate / 100.0)
    
    tpi = cif_value * (tpi_rate / 100.0)
    
    # الرسم على القيمة المضافة (TVA)
    base_tva = cif_value + customs_duty + daps + tic + tpi
    tva = base_tva * (tva_rate / 100.0)
    
    total_taxes = customs_duty + daps + tic + tpi + tva
    total_cost = cif_value + total_taxes
    
    return {
        "CIF_DZD": cif_value,
        "Customs_Duty": customs_duty,
        "Effective_DD_Rate": effective_dd_rate,
        "DAPS": daps,
        "TIC": tic,
        "TPI": tpi,
        "TVA": tva,
        "Total_Taxes": total_taxes,
        "Total_Cost": total_cost
    }

# 4. التخطيط الهيكلي للواجهة الجانبية (Navigation & Systems)
st.markdown('<div class="main-header"> بوابة التجارة والأعمال - Business Gate DZ 🌐</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-text">المنظومة الرقمية الذكية المعتمدة لإدارة العمليات الجمركية، الجباية، والتحليل الاستراتيجي العالمي (إصدار 2.5 الاحترافي)</div>', unsafe_allow_html=True)

sidebar_option = st.sidebar.radio(
    "اختر النظام المطلوب:",
    [
        "محرك تصفية البضائع العامة والتعريفات الضخمة", 
        "محرك رُجيمات السيارات (Automotive)", 
        "حاسبة تكاليف الموانئ و Incoterms", 
        "دليل التشريعات المعقدة والقواعد الستة",
        "استشراف التطورات المستقبلية والتحولات العالمية"
    ]
)

if sidebar_option == "محرك تصفية البضائع العامة والتعريفات الضخمة":
    st.subheader("📦 محرك حساب الرسوم الجمركية والجبائية (البضائع العامة والخطوط الصناعية)")
    
    col1, col2 = st.columns(2)
    with col1:
        hs_code = st.text_input("البند الجمركي الموسع (HS Code - 8 أو 10 أرقام)", "8471.30.00.00")
        description = st.text_input("وصف البضاعة بدقة", "تجهيزات خط إنتاج صناعي / أجهزة رقمية")
        fob_value = st.number_input("قيمة البضاعة بالعملة الأجنبية (FOB)", value=50000.0)
        currency = st.selectbox("العملة الأجنبية", ["EUR", "USD", "CNY", "GBP"])
        exchange_rate = st.number_input("سعر الصرف المرجعي مقابل DZD", value=145.0)
        
    with col2:
        freight = st.number_input("تكلفة الشحن الدولي (Freight - DZD)", value=450000.0)
        insurance = st.number_input("تكلفة التأمين (Insurance - DZD)", value=75000.0)
        exemption_type = st.selectbox(
            "النظام التفضيلي أو الإعفاء التشريعي:",
            [
                "النظام العام (بدون إعفاء)",
                "إعفاء كلي في إطار الاستثمار (AAPI / ANEM)",
                "تخفيض تفضيلي (اتفاقيات الشراكة / ZLECAf)"
            ]
        )
        
    st.markdown("---")
    st.subheader("معدلات الرسوم والضرائب حسب التشريعات المعمول بها")
    
    r_col1, r_col2, r_col3 = st.columns(3)
    with r_col1:
        dd_rate = st.slider("الحقوق الجمركية الأساسية (DD %)", 0.0, 30.0, 5.0)
        daps_rate = st.slider("الرسم الإضافي المؤقت الوقائي (DAPS %)", 0.0, 60.0, 0.0)
    with r_col2:
        tic_rate = st.slider("الرسم الداخلي للاستهلاك (TIC %)", 0.0, 50.0, 0.0)
        tpi_rate = st.slider("رسم الحماية المؤقت (TPI %)", 0.0, 30.0, 0.0)
    with r_col3:
        tva_rate = st.selectbox("الرسم على القيمة المضافة (TVA %)", [0.0, 9.0, 19.0], index=2)

    if st.button("تنفيذ الحساب والتحليل المالي الشامل للشحنة", type="primary"):
        results = advanced_customs_engine(
            hs_code, fob_value, exchange_rate, freight, insurance,
            dd_rate, daps_rate, tic_rate, tpi_rate, tva_rate, exemption_type
        )
        
        st.success("تم إتمام الحساب الجمركي والجبائي بنجاح وفق المعايير العالمية!")
        
        res_col1, res_col2 = st.columns(2)
        with res_col1:
            st.metric("القيمة الجمركية المحوسبة (CIF)", f"{results['CIF_DZD']:,.2f} دج")
            st.metric("الحقوق الجمركية الفعلية المحسوبة", f"{results['Customs_Duty']:,.2f} دج (معدل: {results['Effective_DD_Rate']}%)")
            st.metric("مجموع الرسوم والضرائب المستحقة", f"{results['Total_Taxes']:,.2f} دج")
        with res_col2:
            st.metric("قيمة الرسم الإضافي (DAPS)", f"{results['DAPS']:,.2f} دج")
            st.metric("الرسم على القيمة المضافة (TVA)", f"{results['TVA']:,.2f} دج")
            st.metric("التكلفة الإجمالية النهائية للاستيراد", f"{results['Total_Cost']:,.2f} دج")

elif sidebar_option == "دليل التشريعات المعقدة والقواعد الستة":
    st.subheader("📖 الإطار القانوني والمرجعي للتثمين الجمركي والمعالجة الضخمة")
    st.markdown("""
    ### 1. القواعد الست للتثمين الجمركي (منظمة الجمارك العالمية WCO):
    * **القاعدة الأولى (سعر الصفقة):** الأساس المعياري الأول المعتمد بناءً على الفاتورة التجارية والأسعار التبادلية الحقيقية.
    * **القاعدة الثانية والثالثة (بضائع مطابقة أو مماثلة):** اللجوء إلى معاملات سابقة لسلع متطابقة أو مشابهة تماماً في حالة الشك في قيمة الصفقة.
    * **القاعدة الرابعة والخامسة (طريقة الخصم والطريقة المحسوبة):** الاعتماد على أسعار إعادة البيع في الأسواق المحلية أو تكاليف الإنتاج مضافاً إليها الهوامش الربحية.
    * **القاعدة السادسة (الطريقة المرنة والاستنتاجية):** تطبيق المبادئ المرنة المتوافقة مع الاتفاقيات الدولية لتسوية التثمين المعقد.

    ### 2. التعامل مع التعريفات الضخمة والتشريعات المركبة:
    * **التكامل الضريبي:** إدارة التداخل بين الحقوق الجمركية، الرسوم الوقائية (DAPS)، والرسوم الخاصة (TIC) بوعاء تراكمي دقيق.
    * **الاستفادة من الإعفاءات:** توجيه الاستثمارات الكبرى نحو الأطر القانونية الملائمة (مثل وكالة ترقية الاستثمار AAPI) لخفض التكاليف الجمركية إلى مستواها الأدنى أو الصفرية للمعدات الموجهة للإنتاج.
    """)

elif sidebar_option == "استشراف التطورات المستقبلية والتحولات العالمية":
    st.subheader("🚀 التحولات المستقبلية في التجارة الدولية والأنظمة الجمركية الذكية")
    st.markdown("""
    * **الرقمنة الكاملة والتخليص الإلكتروني (Paperless Customs):** التحول نحو منصات رقمية تتكامل مباشرة مع الموانئ والمنظومات المصرفية (مثل BaridiMob والتحويلات الرقمية البينية).
    * **الذكاء الاصطناعي في تصنيف البنود (AI HS Coding):** اعتماد خوارزميات التعرف الذكي على طبيعة البضائع لتفادي أخطاء التعديل البشري في البنود الجمركية المعقدة.
    * **سلاسل اللوجستيات الخضراء:** فرض معايير بيئية وجمركية جديدة مرتبطة ببصمة الكربون وتكاليف الشحن المستدام.
    * **التكامل الإقليمي والقاري:** الاستفادة القصوى من اتفاقيات التجارة الحرة القارية الإفريقية (ZLECAf) لإعادة صياغة استراتيجيات الاستيراد والتصدير الصناعي.
    """)

# تذييل الصفحة الاحترافي الموحد
st.markdown("---")
st.markdown("<p style='text-align: center; color: #64748B;'>Business Gate DZ © 2026 | تطوير هندسي استشاري احترافي - النسخة العالمية الشاملة</p>", unsafe_allow_html=True)
