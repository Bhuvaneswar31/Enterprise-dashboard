import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ---------------------------
# CONFIG
# ---------------------------
st.set_page_config(page_title="IT SOLUTIONS Dashboard", layout="wide")

# ---------------------------
# STYLING (PRO UI)
# ---------------------------
st.markdown("""
<style>

/* 🔥 CLEAN PROFESSIONAL BACKGROUND */
.stApp {
    background:
    linear-gradient(rgba(8, 12, 20, 0.92), rgba(8, 12, 20, 0.96)),
    url("https://images.unsplash.com/photo-1519389950473-47ba0277781c");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
    color: #EAEAEA;
}

/* 🧊 GLASS KPI CARDS (CLEAR VISIBILITY) */
[data-testid="stMetric"] {
    background: rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 10px;
    backdrop-filter: blur(6px);
    border: 1px solid rgba(255,255,255,0.08);
}

/* 🧾 HEADINGS */
h1, h2, h3 {
    color: #FFFFFF;
    font-weight: 600;
}

/* 📊 CHART CONTAINERS */
.block-container {
    padding-top: 2rem;
}

/* SIDEBAR CLEAN */
section[data-testid="stSidebar"] {
    background-color: rgba(15, 20, 35, 0.95);
}

/* REMOVE ANY WEIRD TEXT EFFECTS */
.css-1offfwp {
    writing-mode: horizontal-tb !important;
}

</style>
""", unsafe_allow_html=True)
# ---------------------------
# DATA GENERATION
# ---------------------------
@st.cache_data
def generate_data():
    np.random.seed(42)

    dates = pd.date_range(start="2025-01-01", end="2026-05-01")

    cities = ["Chennai","Bangalore","Hyderabad","Mumbai","Coimbatore"]
    services = ["Web Dev","App Dev","Digital Marketing","Consulting"]
    sources = ["Organic","Paid Ads","Referral","Direct"]

    data = []

    for date in dates:
        for city in cities:
            for service in services:
                visitors = np.random.randint(100, 250)
                enquiries = int(visitors * np.random.uniform(0.2, 0.4))
                qualified = int(enquiries * np.random.uniform(0.5, 0.8))
                proposals = int(qualified * np.random.uniform(0.6, 0.9))
                conversions = int(proposals * np.random.uniform(0.4, 0.7))

                spend = visitors * np.random.randint(20, 80)
                revenue = conversions * np.random.randint(25000, 90000)

                data.append([
                    date, city, service,
                    np.random.choice(sources),
                    visitors, enquiries, qualified,
                    proposals, conversions, revenue, spend
                ])

    return pd.DataFrame(data, columns=[
        "Date","City","Service","Source",
        "Visitors","Enquiries","Qualified",
        "Proposals","Conversions","Revenue","Spend"
    ])

df = generate_data()

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.title("🔍 Filters")

date_filter = st.sidebar.date_input(
    "Date Range",
    [df["Date"].min(), df["Date"].max()]
)

city_filter = st.sidebar.multiselect("City", df["City"].unique(), df["City"].unique())
service_filter = st.sidebar.multiselect("Service", df["Service"].unique(), df["Service"].unique())
source_filter = st.sidebar.multiselect("Source", df["Source"].unique(), df["Source"].unique())

# ---------------------------
# FILTER DATA
# ---------------------------
filtered_df = df[
    (df["City"].isin(city_filter)) &
    (df["Service"].isin(service_filter)) &
    (df["Source"].isin(source_filter)) &
    (df["Date"] >= pd.to_datetime(date_filter[0])) &
    (df["Date"] <= pd.to_datetime(date_filter[1]))
]

# ---------------------------
# KPI CALCULATIONS
# ---------------------------
total_visitors = filtered_df["Visitors"].sum()
total_leads = filtered_df["Enquiries"].sum()
total_clients = filtered_df["Conversions"].sum()
total_revenue = filtered_df["Revenue"].sum()
total_spend = filtered_df["Spend"].sum()

lead_rate = total_leads / total_visitors if total_visitors else 0
conversion_rate = total_clients / total_visitors if total_visitors else 0
cac = total_spend / total_clients if total_clients else 0
roi = (total_revenue - total_spend) / total_spend if total_spend else 0

# ---------------------------
# HEADER
# ---------------------------
st.title("IT SOLUTION SaaS DASHBOARD")

# ---------------------------
# KPI ROW (COMPACT)
# ---------------------------
k1,k2,k3,k4,k5 = st.columns(5)

k1.metric("Visitors", f"{total_visitors:,}")
k2.metric("Leads", f"{total_leads:,}")
k3.metric("Clients", f"{total_clients:,}")
k4.metric("Revenue", f"₹{total_revenue:,.0f}")
k5.metric("Spend", f"₹{total_spend:,.0f}")

# ---------------------------
# ADVANCED METRICS
# ---------------------------
st.markdown("### Advanced Metrics")

m1,m2,m3,m4 = st.columns(4)

m1.metric("Lead Rate", f"{lead_rate:.2%}")
m2.metric("Conversion Rate", f"{conversion_rate:.2%}")
m3.metric("CAC", f"₹{cac:,.0f}")
m4.metric("ROI", f"{roi:.2%}")

# ---------------------------
# SIDE-BY-SIDE COMPARISON
# ---------------------------
st.markdown("### Performance Comparison")

c1, c2 = st.columns(2)

service_rev = filtered_df.groupby("Service")["Revenue"].sum().reset_index()
service_conv = filtered_df.groupby("Service")["Conversions"].sum().reset_index()

with c1:
    fig1 = px.bar(service_rev, x="Service", y="Revenue", title="Revenue by Service")
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    fig2 = px.bar(service_conv, x="Service", y="Conversions", title="Conversions by Service")
    st.plotly_chart(fig2, use_container_width=True)

# ---------------------------
# ROI PER CHANNEL
# ---------------------------
st.markdown("### ROI by Channel")

roi_channel = filtered_df.groupby("Source").agg({
    "Revenue":"sum",
    "Spend":"sum"
}).reset_index()

roi_channel["ROI"] = (roi_channel["Revenue"] - roi_channel["Spend"]) / roi_channel["Spend"]

fig3 = px.bar(roi_channel, x="Source", y="ROI", title="ROI per Channel")
st.plotly_chart(fig3, use_container_width=True)

# ---------------------------
# FORECAST (TREND BASED)
# ---------------------------
st.markdown("### Revenue Forecast")

trend = filtered_df.groupby("Date")["Revenue"].sum().reset_index()
trend["Forecast"] = trend["Revenue"].rolling(7).mean()

fig4 = px.line(trend, x="Date", y=["Revenue","Forecast"], title="Revenue vs Forecast")
st.plotly_chart(fig4, use_container_width=True)

# ---------------------------
# DRILL DOWN
# ---------------------------
st.markdown("### 🧩 Drill-down Analysis")

selected_service = st.selectbox("Select Service", filtered_df["Service"].unique())

deep_df = filtered_df[filtered_df["Service"] == selected_service]

fig5 = px.bar(deep_df.groupby("City")["Revenue"].sum().reset_index(),
              x="City", y="Revenue",
              title=f"{selected_service} Revenue by City")

st.plotly_chart(fig5, use_container_width=True)

# ---------------------------
# FUNNEL
# ---------------------------
st.markdown("### Funnel")

funnel = pd.DataFrame({
    "Stage":["Visitors","Leads","Qualified","Proposals","Clients"],
    "Count":[
        total_visitors,
        total_leads,
        filtered_df["Qualified"].sum(),
        filtered_df["Proposals"].sum(),
        total_clients
    ]
})

fig6 = px.bar(funnel, x="Stage", y="Count", title="Conversion Funnel")
st.plotly_chart(fig6, use_container_width=True)

# ---------------------------
# SMART INSIGHTS (REAL)
# ---------------------------
st.markdown("### 🧠 Business Insights")

top_service = service_rev.sort_values("Revenue", ascending=False).iloc[0]["Service"]
top_channel = roi_channel.sort_values("ROI", ascending=False).iloc[0]["Source"]
worst_channel = roi_channel.sort_values("ROI").iloc[0]["Source"]

st.success(f"""
• {top_service} dominates revenue → premium pricing or enterprise demand  
• {top_channel} delivers strongest ROI → scale this channel  
• {worst_channel} underperforms → optimize or reduce spend  
• CAC (₹{cac:,.0f}) reflects acquisition efficiency  
• Funnel drop indicates lead qualification gap  
• Forecast trend suggests {'stable growth' if trend['Forecast'].iloc[-1] > trend['Forecast'].iloc[0] else 'volatile performance'}
""")