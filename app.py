import streamlit as st
import pandas as pd
import plotly.express as px

# Page setup
st.set_page_config(
    page_title="Global Methane Emissions Dashboard",
    page_icon="🌍",
    layout="wide"
)

# Load dataset
df = pd.read_csv("clean_methane.csv")

df["Country Name"] = df["Country Name"].astype(str).str.strip()

df = df[~df["Country Name"].str.contains(
    "Euro|World|OECD|Union|income|countries|area|IBRD|IDA|Africa|Asia|Europe",
    case=False,
    na=False
)]

# CSS styling
st.markdown("""
<style>
.block-container {
    padding-top: 2rem;
}
.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #1f2937;
}
.sub-title {
    font-size: 19px;
    color: #4b5563;
    margin-bottom: 25px;
}
.section-card {
    background-color: #f8fafc;
    padding: 18px;
    border-radius: 14px;
    border: 1px solid #e5e7eb;
    margin-bottom: 20px;
}
</style>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title"> Global Methane Emissions Dashboard</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-title">Interactive analysis using World Bank methane emissions data from 2000 to 2023.</div>',
    unsafe_allow_html=True
)

st.markdown("""
This dashboard allows users to explore methane emission trends, compare countries, identify top emitters,
and understand the distribution of methane emissions across countries.
""")

# Sidebar filters
st.sidebar.title("Filters")

country = st.sidebar.selectbox(
    "Select Country",
    sorted(df["Country Name"].unique())
)

year_range = st.sidebar.slider(
    "Select Year Range",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

st.sidebar.subheader("Compare Countries")

compare_countries = st.sidebar.multiselect(
    "Select Countries to Compare",
    sorted(df["Country Name"].unique()),
    default=["China", "India", "United States"]
)

# Filtered data
filtered_years = df[
    (df["Year"] >= year_range[0]) &
    (df["Year"] <= year_range[1])
]

filtered = filtered_years[
    filtered_years["Country Name"] == country
]

# KPI cards
kpi1, kpi2, kpi3, kpi4 = st.columns(4)

kpi1.metric("🌍 Total Countries", df["Country Name"].nunique())
kpi2.metric("📅 Years Covered", f"{df['Year'].min()}–{df['Year'].max()}")
kpi3.metric("🔥 Highest Emission", round(df["Methane"].max(), 2))
kpi4.metric("📊 Records", df.shape[0])

st.markdown("---")

# Chart 1
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader(f" Methane Emissions Trend - {country}")

fig_line = px.line(
    filtered,
    x="Year",
    y="Methane",
    markers=True,
    title=f"Methane Emissions Trend in {country}",
    labels={"Methane": "Methane Emissions", "Year": "Year"},
    template="plotly_white"
)
fig_line.update_layout(hovermode="x unified")

st.plotly_chart(fig_line, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chart 2
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader(" Global Methane Emissions Trend")

global_trend = (
    filtered_years.groupby("Year")["Methane"]
    .mean()
    .reset_index()
)

fig_global = px.line(
    global_trend,
    x="Year",
    y="Methane",
    markers=True,
    title="Global Average Methane Emissions Over Time",
    labels={"Methane": "Average Methane Emissions", "Year": "Year"},
    template="plotly_white"
)
fig_global.update_layout(hovermode="x unified")

st.plotly_chart(fig_global, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chart 3
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader(" Country Comparison")

compare_df = filtered_years[
    filtered_years["Country Name"].isin(compare_countries)
]

fig_compare = px.line(
    compare_df,
    x="Year",
    y="Methane",
    color="Country Name",
    markers=True,
    title="Comparison of Methane Emissions",
    labels={"Methane": "Methane Emissions", "Country Name": "Country"},
    template="plotly_white"
)
fig_compare.update_layout(hovermode="x unified")

st.plotly_chart(fig_compare, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chart 4
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("🏆 Top 10 Countries by Average Methane Emissions")

top10 = (
    filtered_years.groupby("Country Name")["Methane"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_bar = px.bar(
    top10,
    x="Country Name",
    y="Methane",
    text=top10["Methane"].round(1),
    title="Top 10 Countries by Average Methane Emissions",
    labels={"Methane": "Average Methane Emissions", "Country Name": "Country"},
    template="plotly_white"
)
fig_bar.update_traces(textposition="outside")
fig_bar.update_layout(xaxis_tickangle=-30)

st.plotly_chart(fig_bar, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chart 5
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader(" Distribution of Methane Emissions")

fig_hist = px.histogram(
    filtered_years,
    x="Methane",
    nbins=50,
    title="Distribution of Methane Emissions",
    labels={"Methane": "Methane Emissions"},
    template="plotly_white"
)

st.plotly_chart(fig_hist, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Chart 6
st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader(" Emissions Heatmap for Top 5 Countries")

top_countries = (
    df.groupby("Country Name")["Methane"]
    .mean()
    .sort_values(ascending=False)
    .head(5)
    .index
)

heat_df = filtered_years[
    filtered_years["Country Name"].isin(top_countries)
]

pivot_df = heat_df.pivot(
    index="Country Name",
    columns="Year",
    values="Methane"
)

fig_heat = px.imshow(
    pivot_df,
    aspect="auto",
    title="Emissions Heatmap for Top 5 Countries",
    labels=dict(x="Year", y="Country", color="Methane"),
    template="plotly_white"
)

st.plotly_chart(fig_heat, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# Insights
st.markdown("---")
st.subheader(" Key Insights")
st.markdown("""
China, the United States, and India are among the highest methane-emitting countries. 
The dashboard also shows that methane emissions vary widely between countries, with a small number of countries contributing a larger share of total emissions. 
The comparison and heatmap charts help users identify differences in emission patterns over time.
""")

# Dataset summary
st.subheader(" Dataset Summary")

summary1, summary2, summary3 = st.columns(3)
summary1.write(f"**Rows:** {df.shape[0]}")
summary2.write(f"**Columns:** {df.shape[1]}")
summary3.write(f"**Countries:** {df['Country Name'].nunique()}")

st.markdown("---")
st.caption(" Data Source: World Bank Open Data | Built with Streamlit, Pandas, and Plotly | 5DATA004C Coursework")