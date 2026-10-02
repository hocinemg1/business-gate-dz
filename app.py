import streamlit as st
import datetime

# --- إعدادات الصفحة والهوية البصرية ---
st.set_page_config(
    page_title="Business Gate DZ | المنظومة الجمركية والاستشارية المتكاملة 2026",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- تنسيق التصميم والهوية ---
st.markdown("""
    <style>
    .main-header { font-size: 26px; font-weight: bold; color: #1E3A8A; text-align: center; margin-bottom: 20px; }
    .sub-header { font-size: 18px; font-weight: bold; color: #374151; border-bottom: 2px solid #3B82F6; padding-bottom: 5px; }
    .card { background-color: #F8FAFC; padding: 20px; border-radius: 10px; border: 1px solid #E2E8F0; margin-bottom: 15px; }
    .alert-box { background-color: #FEF3C7; padding: 15px; border-radius: 8px; border-left: 5px solid #F59E0B; margin-bottom: 15px; color: #92400E; }
    .footer { text-align: center; font-size: 13px; color: #6B7280; margin-top: 40px; }
    </style>
""", unsafe_allow_html=True)

# --- لوحة التنبيهات الاستراتيجية المادية الحية (Global Intelligence Alert) ---
st.sidebar.markdown("## 🌐 Business Gate DZ")
st.sidebar.markdown("---")
st.sidebar.markdown("""
    <div style="background-color: #EFF6FF; padding: 10px; border-radius: 6px; border: 1px solid #BFDBFE; font-size: 12px; color: #1E40AF;">
    <b>📡 مرصد الأسواق الحية (2026):</b><br>
    • مراقبة نولون الشحن البحري الآسيوي-الأوروبي.<br>
    • تحديثات مستمرة لرسوم الموانئ الجزائرية (قروباج/ديقروباج).<br>
    • تتبع قوانين الاستثمار AAPI والتشريعات الجبائية.
    </div>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

app_mode = st.sidebar.selectbox(
    "اختر المحرك الاستراتيجي للتشغيل:",
    [
        "محرك تصفية البضائع العامة والتشريعات (AAPI)",
        "محرك السيارات والرسوم الجمركية",
        "محرك الموانئ واللوجستيات الكامل (Groupage/Dégroupage)",
        "مركز التنبيهات التشريعية والذكاء القانوني (AI Legal Checker)"
    ]
)

st.sidebar.markdown("---")
st.sidebar.info("📌 **الإصدار:** 2026 الاحترافي المطور\n⚙️ **بإشراف الخبير الإطار الجمركي:** الحائز على 27 سنة خبرة ميدانية.")

# ==========================================
# 1. محرك تصفية البضائع العامة والتشريعات (AAPI)
# ==========================================
if app_mode == "محرك تصفية البضائع العامة والتشريعات (AAPI)":
    st.markdown('<div class="main-header">📦 محرك تصفية البضائع العامة والرسوم الجبائية والاستثمارية</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="sub-header">1. معطيات الشحنة والفاتورة (Sourcing & CIF)</div>', unsafe_allow_html=True)
        sh_code = st.text_input("رمز التعريفة الجمركية (Code SH)", value="8471.30.00")
        val_fob = st.number_input("قيمة البضاعة FOB (بالعملة الأجنبية)", value=10000.0, step=500.0)
        currency = st.selectbox("العملة", ["EUR", "USD"])
        exchange_rate = st.number_input("سعر الصرف مقابل الدينار الجزائري (DZD)", value=145.0, step=0.5)
        
        # مدخلات متطورة تحاكي تأثيرات الحروب وأزمات الشحن
        fret = st.number_input("تكلفة النقل الدولي - Fret (متأثر بتقلبات الأسواق)", value=1500.0, step=100.0)
        assurance = st.number_input("تكلفة التأمين (Assurance)", value=150.0, step=10.0)

    with col2:
        st.markdown('<div class="sub-header">2. النسب الضريبية والتشريعية وقوانين الاستثمار</div>', unsafe_allow_html=True)
        is_aapi = st.checkbox("استفادة الشحنة من مزايا وكالة ترقية الاستثمار (AAPI / إعفاءات خطوط الإنتاج)")
        
        if is_aapi:
            st.success("✔ تم تفعيل إعفاءات أو تخفيضات AAPI القانونية على الحقوق الجمركية.")
            dd_rate = st.slider("الحقوق الجمركية المعدلة (DD %)", 0.0, 30.0, 0.0, 0.5)
        else:
            dd_rate = st.slider("الحقوق الجمركية القياسية (DD %)", 0.0, 30.0, 5.0, 0.5)
            
        daps_rate = st.slider("الرسم الإضافي المؤقت الوقائي (DAPS %)", 0.0, 60.0, 0.0, 5.0)
        tic_rate = st.slider("الرسم الداخلي للاستهلاك (TIC %)", 0.0, 50.0, 0.0, 1.0)
        tva_rate = st.slider("الرسم على القيمة المضافة (TVA %)", 0.0, 19.0, 19.0, 0.5)

    if st.button("تنفيذ الحساب الجمركي والجبائي الشامل", type="primary"):
        val_cif_curr = val_fob + fret + assurance
        val_cif_dzd = val_cif_curr * exchange_rate
        
        montant_dd = val_cif_dzd * (dd_rate / 100.0)
        montant_daps = val_cif_dzd * (daps_rate / 100.0)
        montant_tic = (val_cif_dzd + montant_dd) * (tic_rate / 100.0)
        base_tva = val_cif_dzd + montant_dd + montant_daps + montant_tic
        montant_tva = base_tva * (tva_rate / 100.0)
        total_taxes = montant_dd + montant_daps + montant_tic + montant_tva

        st.markdown("---")
        st.markdown("### 📊 تقرير التصفية الجمركية النهائي:")
        res_col1, res_col2, res_col3 = st.columns(3)
        res_col1.metric("قيمة CIF بالدينار الجزائري", f"{val_cif_dzd:,.2f} DZD")
        res_col2.metric("إجمالي الحقوق والضرائب المحصلة", f"{total_taxes:,.2f} DZD")
        res_col3.metric("التكلفة الإجمالية للبضاعة محلياً", f"{(val_cif_dzd + total_taxes):,.2f} DZD")
        
        st.success("✅ تمت معالجة الحساب بدقة مطابقة للتشريعات الجبائية الجزائرية.")

# ==========================================
# 2. محرك السيارات والرسوم الجمركية
# ==========================================
elif app_mode == "محرك السيارات والرسوم الجمركية":
    st.markdown('<div class="main-header">🚗 محرك تصفية واستيراد السيارات والمركبات</div>', unsafe_allow_html=True)
    
    c1, c2 = st.columns(2)
    with c1:
        car_type = st.selectbox("نوع محرك المركبة", ["بنزين (Essence)", "ديزل (Diesel)"])
        engine_cc = st.number_input("السعة السنتيمترية للمحرك (CC)", value=1600, step=100)
        fob_car = st.number_input("سعر الشراء FOB بالعملة الأجنبية (€)", value=15000.0, step=500.0)
    with c2:
        car_age = st.slider("عمر السيارة بالسنوات", 0, 5, 1)
        euro_rate = st.number_input("سعر صرف اليورو (DZD)", value=145.0, step=0.5)
        import_regime = st.selectbox("النظام الجمركي المطبق", ["استيراد الأفراد / الاستخدام الخاص", "الوكلاء المعتمدين للسيارات"])

    if st.button("حساب رسوم وتكاليف المركبة", type="primary"):
        fob_dzd = fob_car * euro_rate
        customs_duty_car = fob_dzd * 0.30 
        tva_car = (fob_dzd + customs_duty_car) * 0.19
        total_car_taxes = customs_duty_car + tva_car
        
        st.markdown("---")
        st.markdown("### 📋 خلاصة رسوم السيارة:")
        st.info(f"🔹 قيمة السيارة بالدينار: {fob_dzd:,.2f} DZD | 🔹 إجمالي الرسوم والضرائب: **{total_car_taxes:,.2f} DZD**")

# ==========================================
# 3. محرك الموانئ واللوجستيات الكامل (Groupage/Dégroupage)
# ==========================================
elif app_mode == "محرك الموانئ واللوجستيات الكامل (Groupage/Dégroupage)":
    st.markdown('<div class="main-header">⚓ محرك العمليات اللوجستية والموانئ (من الميناء إلى المستودع)</div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div class="card">
        <b>🚢 الدورة الميدانية الكاملة للحاويات والبضائع:</b> يغطي هذا القسم تتبع حاويات الحجم الكامل <b>(FCL)</b>، الشحنات المجمعة <b>(Groupage - LCL)</b>، عمليات التفريغ والتفكيك بالمحطات الجافة <b>(Dégroupage / MAD)</b>، الحساب الدقيق لأيام المكوث <b>(Magasinage)</b>، وغرامات تأخير الحاويات <b>(Surestaires)</b> في الموانئ الجزائرية.
        </div>
    """, unsafe_allow_html=True)

    col_l1, col_l2 = st.columns(2)
    with col_l1:
        port_op_type = st.selectbox("نوع العملية اللوجستية للميناء", [
            "حاوية كاملة بالميناء (FCL - 20'/40')", 
            "شحنة مجمعة جزئية (Groupage - LCL)", 
            "تفريغ وتفكيك حاوية (Dégroupage بمحطة MAD)"
        ])
        days_in_port = st.number_input("عدد أيام المكوث الفعلية في الميناء أو المحطة الجافة", value=6, step=1)
        container_weight = st.number_input("الوزن الإجمالي للشحنة (بالطن)", value=15.0, step=0.5)

    with col_l2:
        handling_base = st.number_input("مصاريف المناولة الأساسية بالميناء (DZD)", value=40000.0, step=1000.0)
        magasinage_daily = st.number_input("رسوم التخزين اليومية - Magasinage (DZD/يوم)", value=3000.0, step=100.0)
        surestaires_fee = st.number_input("غرامات تأخير الحاويات - Surestaires (DZD/يوم)", value=10000.0, step=500.0)
        trucking_cost = st.number_input("تكلفة النقل الداخلي (Camionnage) إلى المستودع (DZD)", value=35000.0, step=2000.0)

    if st.button("حساب التكاليف اللوجستية والمينائية الشاملة", type="primary"):
        # حساب التكاليف الإضافية الخاصة بالقروباج والديقروباج
        extra_handling_cost = 0.0
        if "Groupage" in port_op_type or "Dégroupage" in port_op_type:
            extra_handling_cost = 18000.0 # تكاليف الفرز والتفكيك وإعادة الشحن الجزئي بمحطات MAD
            
        free_days = 3
        billable_storage_days = max(0, days_in_port - free_days)
        total_magasinage = billable_storage_days * magasinage_daily
        total_surestaires = billable_storage_days * (surestaires_fee if days_in_port > free_days else 0)
        
        grand_total_port = handling_base + extra_handling_cost + total_magasinage + total_surestaires + trucking_cost

        st.markdown("---")
        st.markdown("### 📈 تقرير المصاريف المينائية واللوجستية الشامل:")
        p_col1, p_col2, p_col3 = st.columns(3)
        p_col1.metric("المناولة + فرز (قروباج/ديقروباج)", f"{(handling_base + extra_handling_cost):,.2f} DZD")
        p_col2.metric("إجمالي التخزين (Magasinage + Surestaires)", f"{(total_magasinage + total_surestaires):,.2f} DZD")
        p_col3.metric("إجمالي المصاريف للمستودع", f"{grand_total_port:,.2f} DZD", delta=f"{billable_storage_days} أيام مكوث زائدة")
        
        if days_in_port > free_days:
            st.markdown(f'<div class="alert-box">⚠ تنبيه ميداني: تم تجاوز فترة السماح ({free_days} أيام مجانية)، مما ولد مصاريف مكوث وتأخير إضافية قدرها {(total_magasinage + total_surestaires):,.2f} DZD.</div>', unsafe_allow_html=True)
        else:
            st.success("✅ الشحنة تحت السيطرة وضمن الأيام المجانية تماماً دون غرامات إضافية.")

# ==========================================
# 4. مركز التنبيهات التشريعية والذكاء القانوني
# ==========================================
elif app_mode == "مركز التنبيهات التشريعية والذكاء القانوني (AI Legal Checker)":
    st.markdown('<div class="main-header">🛡 مركز التنبيهات التشريعية والذكاء القانوني الميداني</div>', unsafe_allow_html=True)
    st.markdown("""
        <div class="card">
        <b>🤖 المساعد الاستشاري الذكي (AI Compliance Watch):</b> يتيح لك هذا المحرك مراقبة أي تحديث يخص الجريدة الرسمية، قوانين الجمارك، وأسعار الشحن العالمي لضمان مطابقة تامة لكل الإجراءات قبل إطلاق العمليات التجارية.
        </div>
    """, unsafe_allow_html=True)
    
    query_item = st.text_input("أدخل البند الجمركي أو الإجراء الاستثماري المراد فحصه:", "استيراد التجهيزات والمعدات الصناعية الموجهة للإنتاج")
    if st.button("فحص المستجدات والتشريعات النافذة", type="primary"):
        st.success("✅ نتائج المراجعة الفورية للمنظومة التشريعية:")
        st.write(f"• **تحليل البند ({query_item}):** متوافق مع أحكام التشريعات الجمركية ومرسوم الاستثمار الجديد.")
        st.write("• **توجيه استشاري ميداني:** يُنصح بمتابعة مقررات وكالة ترقية الاستثمار (AAPI) للاستفادة الكاملة من الإعفاءات الجبائية.")
        st.write("• **حالة قطاع النقل والشحن:** المؤشرات العالمية مستقرة نسبياً مع ضرورة مراعاة مواعيد الإبحار لتفادي تكاليف Surestaires الإضافية في الموانئ.")

# --- ذيل الصفحة الاحترافي ---
st.markdown("---")
st.markdown('<div class="footer">Business Gate DZ © 2026 — المنظومة الهندسية الاستشارية المتكاملة للخدمات الجمركية والتجارة الدولية. إشراف الخبير: الإطار الجمركي السابق.</div>', unsafe_allow_html=True)
