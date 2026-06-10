import streamlit as st
import pandas as pd
import plotly.express as px

# 1. إعداد الصفحة بشكل احترافي
st.set_page_config(page_title="Executive Sales Dashboard", layout="wide")

# 2. كود CSS الذكي لضبط الألوان تلقائياً
st.markdown("""
    <style>
    /* تنسيق الأرقام لتبدو كأرقام الشركات الكبرى */
    [data-testid="stMetricValue"] {
        font-size: 35px !important;
        font-weight: 800 !important;
    }
    /* ضمان وضوح العناوين مهما كان لون الخلفية */
    h1, h2, h3 {
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

st.title("📈 Executive Sales Overview")
st.markdown("---")

# 3. تحميل البيانات
try:
    df = pd.read_csv('sales.csv')
except FileNotFoundError:
    st.error("خطأ: ملف 'sales.csv' غير موجود في المجلد.")
    st.stop()

# 4. القائمة الجانبية (الفلاتر)
st.sidebar.header("🔍 Filter Dashboard")
products = st.sidebar.multiselect("Select Product:", df["Product"].unique(), default=df["Product"].unique())
df_filtered = df[df["Product"].isin(products)]

# 5. عرض مؤشرات الأداء (KPIs)
col1, col2, col3 = st.columns(3)
col1.metric("Total Revenue", f"${df_filtered['Sales'].sum():,}")
col2.metric("Units Sold", df_filtered['Quantity'].sum())
col3.metric("Avg Price", f"${df_filtered['Sales'].mean():,.2f}")

st.markdown("<br>", unsafe_allow_html=True)

# 6. الرسوم البيانية التفاعلية
c1, c2 = st.columns([2, 1])

with c1:
    st.subheader("Monthly Sales Trend")
    # نستخدم Palette جميلة ومريحة للعين
    fig = px.bar(df_filtered, x="Product", y="Sales", color="Product", 
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with c2:
    st.subheader("Market Composition")
    fig_pie = px.pie(df_filtered, values='Sales', names='Product', hole=0.6,
                     color_discrete_sequence=px.colors.qualitative.Pastel)
    st.plotly_chart(fig_pie, use_container_width=True)

# 7. عرض البيانات الخام
with st.expander("View Raw Data"):
    st.dataframe(df_filtered, use_container_width=True)