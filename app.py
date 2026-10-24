import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# LogiSight 360 — runs locally from the project folder.
st.set_page_config(page_title="LogiSight 360", page_icon="🚚", layout="wide")

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "Last mile Delivery Data.csv"

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
.stApp{background:radial-gradient(ellipse at 65% 0%,#102c5b 0%,transparent 40%),linear-gradient(135deg,#030d20,#061832 55%,#041126);color:#f3f7ff}
[data-testid="stHeader"]{background:rgba(3,13,31,.95)}
.block-container{max-width:1900px;padding-top:1rem;padding-bottom:2rem}
h1{font-size:2.1rem!important;font-weight:800!important;letter-spacing:-1px}
h2,h3,p,label{color:#f3f7ff}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#061a37,#04132b 65%,#080d2a);border-right:1px solid #164b88}
[data-testid="stSidebar"]>div:first-child{padding:1rem .8rem}
[data-testid="stSidebar"] [data-testid="stRadio"]>div{gap:7px}
[data-testid="stSidebar"] [data-testid="stRadio"] label{padding:9px 11px;border-radius:13px;border:1px solid transparent;background:rgba(12,39,77,.5)}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover{background:#123b72;border-color:#267fff}
[data-testid="stSidebar"] [data-testid="stRadio"] label:has(input:checked){background:linear-gradient(105deg,#076bff,#4351ff 60%,#8b3dff);border-color:#65a9ff;box-shadow:0 0 23px #0067ff55}
[data-testid="stSidebar"] [data-testid="stRadio"] label p{color:white!important;font-weight:600}
[data-testid="stMetric"]{min-height:112px;padding:15px;border-radius:17px;border:1px solid #167bff;background:linear-gradient(135deg,#0b3d87,#081b3b);box-shadow:0 8px 25px #004bbb20}
[data-testid="stMetricLabel"] p{color:#d3e5ff!important;font-size:.82rem}
[data-testid="stMetricValue"]{color:white!important;font-weight:800}
[data-testid="stPlotlyChart"]{border:1px solid #164b80;border-radius:17px;background:linear-gradient(145deg,#0a2345,#05152d);padding:4px}
[data-testid="stVerticalBlockBorderWrapper"]{border:1px solid #194a7b;border-radius:16px;background:linear-gradient(145deg,#091f3e,#06152d)}
[data-testid="stMultiSelect"]>div>div,[data-testid="stTextInput"] input,[data-testid="stDateInput"] input{background:#0a2143!important;color:white!important;border:1px solid #285b91!important;border-radius:10px!important}
[data-baseweb="tag"]{background:linear-gradient(90deg,#086fff,#5b49f5)!important}
.stButton button,.stDownloadButton button{color:white!important;background:linear-gradient(100deg,#0878ff,#783cff)!important;border:0!important;border-radius:11px!important;font-weight:700}
hr{border-color:#173b65}
.brand-sub{font-size:10px;letter-spacing:1.2px;color:#9cc7ef;margin-top:4px}
.glowline{height:2px;background:linear-gradient(90deg,#08d7f5,#167aff,#8b3cff,transparent);margin:16px 0}
.sidebar-art{margin-top:22px;padding:16px 10px;border-radius:18px;background:radial-gradient(circle at 30% 20%,#00b8ff28,transparent 55%),linear-gradient(145deg,#0a2851,#11113b);border:1px solid #16477b;text-align:center}
.sidebar-art .truck{font-size:50px;filter:drop-shadow(0 0 12px #087cff)}
.sidebar-art .slogan{font-size:16px;font-weight:800;line-height:1.4}.sidebar-art .slogan span{color:#a18bff}
.eyebrow{color:#35d9ff;font-size:10px;letter-spacing:2px;font-weight:800}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_dataset(file_path, modified_time):
    data = pd.read_csv(file_path)
    data.columns = data.columns.str.strip()
    required = ["Order_ID","Agent_Age","Agent_Rating","Order_Date","Weather","Traffic","Vehicle","Area","Delivery_Time","Category"]
    missing = [c for c in required if c not in data.columns]
    if missing:
        raise ValueError("These expected columns are missing: " + ", ".join(missing))
    for c in ["Agent_Age","Agent_Rating","Delivery_Time","Store_Latitude","Store_Longitude","Drop_Latitude","Drop_Longitude"]:
        if c in data.columns:
            data[c] = pd.to_numeric(data[c], errors="coerce")
    data["Order_Date"] = pd.to_datetime(data["Order_Date"], errors="coerce")
    for c in ["Weather","Traffic","Vehicle","Area","Category"]:
        data[c] = data[c].astype("string").str.strip()
    data["Weather"] = data["Weather"].fillna("Unknown")
    return data

if not DATA_PATH.exists():
    st.error("CSV file not found. Place 'Last mile Delivery Data.csv' beside app.py.")
    st.code(f"Expected location:\n{DATA_PATH}")
    st.stop()

try:
    df = load_dataset(str(DATA_PATH), DATA_PATH.stat().st_mtime)
except Exception as exc:
    st.error(f"Could not load the dataset: {exc}")
    st.stop()

# Sidebar
with st.sidebar:
    st.markdown('<div style="font-size:29px">🚚 <b>LogiSight <span style="color:#26dff3">360</span></b></div><div class="brand-sub">LAST-MILE DELIVERY INTELLIGENCE</div><div class="glowline"></div>', unsafe_allow_html=True)
    st.markdown("#### ✦ NAVIGATION")
    page = st.radio("Navigation", ["🏠  Dashboard","📊  Delay Analysis","🚚  Vehicle Performance","👤  Agent Performance","🗺️  Area Insights","📦  Category Analysis","🗂️  Data Explorer"], label_visibility="collapsed")
    st.markdown('<div class="glowline"></div>', unsafe_allow_html=True)
    st.markdown("#### 📁 DATASET")
    st.markdown(f"**{len(df):,}** original records  \n**{df.shape[1]}** columns")
    st.markdown('<div class="sidebar-art"><div class="truck">🚚</div><div class="slogan">Smarter Deliveries<br><span>Better Insights</span></div><div style="color:#75baff;font-size:10px;letter-spacing:1px;margin-top:10px">DATA-DRIVEN DECISIONS</div></div>', unsafe_allow_html=True)

st.markdown('<div class="eyebrow">LOGISIGHT 360　/　ANALYTICS WORKSPACE</div>', unsafe_allow_html=True)
st.title("Delivery Intelligence Dashboard")
st.markdown('<p style="color:#b9cfea;margin-top:-8px">Explore delivery patterns, compare operational conditions and identify areas for investigation.</p>', unsafe_allow_html=True)

# Main dashboard and right-side filters
main, filter_panel = st.columns([4.5, 1.12], gap="medium")
with filter_panel:
    with st.container(border=True):
        st.markdown("### 🔻 Filters")
        if st.button("↺ Reset filters", use_container_width=True):
            for key in ["date_range","filter_Weather","filter_Traffic","filter_Vehicle","filter_Area","filter_Category","order_search","agent_age_range","agent_rating_range"]:
                st.session_state.pop(key, None)
            st.rerun()
        valid_dates = df["Order_Date"].dropna()
        if not valid_dates.empty:
            date_range = st.date_input("Date range", value=(valid_dates.min().date(),valid_dates.max().date()), min_value=valid_dates.min().date(), max_value=valid_dates.max().date(), key="date_range")
        else:
            date_range = ()
        def choose_filter(column, label):
            options = sorted(df[column].dropna().astype(str).unique().tolist())
            return st.multiselect(label, options, default=options, key="filter_"+column)
        weather_sel = choose_filter("Weather","🌦️ Weather")
        traffic_sel = choose_filter("Traffic","🚦 Traffic")
        vehicle_sel = choose_filter("Vehicle","🚚 Vehicle type")
        area_sel = choose_filter("Area","📍 Area")
        category_sel = choose_filter("Category","📦 Product category")

        # Added numeric filters for agent age and rating.
        age_values = pd.to_numeric(df["Agent_Age"], errors="coerce").dropna()
        if not age_values.empty:
            age_min, age_max = int(age_values.min()), int(age_values.max())
            agent_age_range = st.slider(
                "👤 Agent age range",
                min_value=age_min,
                max_value=age_max,
                value=(age_min, age_max),
                key="agent_age_range"
            )
        else:
            agent_age_range = None

        rating_values = pd.to_numeric(df["Agent_Rating"], errors="coerce").dropna()
        if not rating_values.empty:
            rating_min = float(rating_values.min())
            rating_max = float(rating_values.max())
            if rating_min == rating_max:
                agent_rating_range = (rating_min, rating_max)
                st.caption(f"Agent rating: {rating_min:g} (only observed value)")
            else:
                agent_rating_range = st.slider(
                    "⭐ Agent rating range",
                    min_value=rating_min,
                    max_value=rating_max,
                    value=(rating_min, rating_max),
                    step=0.1,
                    key="agent_rating_range"
                )
        else:
            agent_rating_range = None

        order_search = st.text_input("Search Order ID", placeholder="Optional", key="order_search")

filtered = df.copy()
if len(date_range) == 2:
    start_date, end_date = date_range
    filtered = filtered[filtered["Order_Date"].isna() | filtered["Order_Date"].dt.date.between(start_date,end_date)]
if order_search.strip():
    filtered = filtered[filtered["Order_ID"].astype(str).str.contains(order_search.strip(),case=False,na=False)]
for col, selected in [("Weather",weather_sel),("Traffic",traffic_sel),("Vehicle",vehicle_sel),("Area",area_sel),("Category",category_sel)]:
    filtered = filtered[filtered[col].isin(selected)]

# Apply the added numeric filters. Missing values are excluded when a numeric range is active.
if agent_age_range is not None:
    age_numeric = pd.to_numeric(filtered["Agent_Age"], errors="coerce")
    filtered = filtered[age_numeric.between(agent_age_range[0], agent_age_range[1])]
if agent_rating_range is not None:
    rating_numeric = pd.to_numeric(filtered["Agent_Rating"], errors="coerce")
    filtered = filtered[rating_numeric.between(agent_rating_range[0], agent_rating_range[1])]

with main:
    if filtered.empty:
        st.warning("No records match these filters. Widen or reset your filters.")
        st.stop()
    times = pd.to_numeric(filtered["Delivery_Time"],errors="coerce").dropna()
    original_times = pd.to_numeric(df["Delivery_Time"],errors="coerce").dropna()
    average = times.mean() if len(times) else 0
    # Assignment definition: late delivery is above mean + one standard deviation.
    threshold = original_times.mean() + original_times.std() if len(original_times) > 1 else (
        original_times.mean() if len(original_times) == 1 else None
    )
    late_mask = times.gt(threshold) if threshold is not None else pd.Series(False, index=times.index)
    late_percentage = late_mask.mean() * 100 if len(times) and threshold is not None else 0
    late_count = int(late_mask.sum()) if threshold is not None else 0

    st.markdown("### ✨ Operations Overview")
    k1,k2,k3,k4 = st.columns(4)
    k1.metric("📦 Orders Analysed",f"{len(filtered):,}")
    k2.metric("⏱️ Average Delivery Time",f"{average:.2f}")
    k3.metric("⌛ Late Deliveries",f"{late_percentage:.1f}%")
    k4.metric("📍 Areas Covered",f"{filtered['Area'].nunique()}")
    st.caption(
        f"Late delivery = Delivery_Time > full-dataset mean + 1 standard deviation "
        f"(threshold: {threshold:.2f}; {late_count:,} late orders in the filtered records). "
        "Delivery-time units are not specified in the source CSV."
    )

    PALETTE = ["#087cff","#08d6b0","#8d5cff","#ff9f2e","#ed36d8","#19d6ed"]
    def style_chart(fig, height=300):
        fig.update_layout(height=height,paper_bgcolor="rgba(0,0,0,0)",plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif",color="#dceaff",size=10),
            margin=dict(l=12,r=12,t=45,b=16),title=dict(font=dict(size=14,color="#f4f8ff")),
            legend=dict(orientation="h",y=1.02,x=1,xanchor="right",bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="#183454",zerolinecolor="#183454"),
            yaxis=dict(gridcolor="#183454",zerolinecolor="#183454"))
        return fig
    def chart_heading(title, subtitle):
        st.markdown(f"### {title}")
        st.caption(subtitle)

    if page == "🏠  Dashboard":
        left,right = st.columns([1.08,1])
        with left:
            chart_heading("📈 Delivery Trend Over Time","Daily order volume for the selected date range.")
            dated = filtered.dropna(subset=["Order_Date"]).copy()
            if not dated.empty:
                dated["Date"] = dated["Order_Date"].dt.date
                daily = dated.groupby("Date").agg(Orders=("Order_ID","count")).reset_index()
                fig = go.Figure(go.Scatter(x=daily["Date"],y=daily["Orders"],name="Orders",mode="lines+markers",line=dict(color="#1685ff",width=3),fill="tozeroy",fillcolor="rgba(22,133,255,.13)"))
                fig.update_layout(title="Order Volume by Day")
                st.plotly_chart(style_chart(fig,300),use_container_width=True)
            else:
                st.info("No valid dates for the selected records.")
        with right:
            chart_heading("🗺️ Average Delivery Time by Area","Hover for the number of records in each area.")
            area_data = filtered.groupby("Area").agg(Average=("Delivery_Time","mean"),Records=("Order_ID","count")).reset_index().dropna(subset=["Average"]).sort_values("Average")
            if not area_data.empty:
                fig = px.bar(area_data,x="Average",y="Area",orientation="h",color="Average",color_continuous_scale=["#087cff","#17d9ec","#a448ff"],text="Records",title="Area Comparison")
                fig.update_traces(texttemplate="%{text} records",textposition="outside")
                st.plotly_chart(style_chart(fig,300),use_container_width=True)
        left,right = st.columns(2)
        with left:
            chart_heading("🌦️ Delivery Time by Weather & Traffic","Average time for each observed combination.")
            heat_data = filtered.dropna(subset=["Weather","Traffic","Delivery_Time"])
            if not heat_data.empty:
                matrix = heat_data.pivot_table(index="Weather",columns="Traffic",values="Delivery_Time",aggfunc="mean")
                fig = px.imshow(matrix,text_auto=".1f",aspect="auto",color_continuous_scale=["#087cff","#18d8ef","#ed28d8"],labels=dict(x="Traffic",y="Weather",color="Mean time"),title="Weather × Traffic")
                st.plotly_chart(style_chart(fig,315),use_container_width=True)
        with right:
            chart_heading("🚚 Average Delivery Time by Vehicle","Record counts provide context for small groups.")
            vehicle_data = filtered.dropna(subset=["Vehicle","Delivery_Time"])
            if not vehicle_data.empty:
                summary = vehicle_data.groupby("Vehicle").agg(Average=("Delivery_Time","mean"),Records=("Order_ID","count")).reset_index().sort_values("Average")
                fig = px.bar(summary,x="Average",y="Vehicle",orientation="h",color="Vehicle",color_discrete_sequence=PALETTE,text="Records",title="Fleet Comparison")
                fig.update_traces(texttemplate="%{text} records",textposition="outside")
                st.plotly_chart(style_chart(fig,315),use_container_width=True)
        left,right = st.columns(2)
        with left:
            chart_heading("👤 Agent Performance","Relationship between agent rating and delivery time.")
            agent_data = filtered.dropna(subset=["Agent_Rating","Delivery_Time","Agent_Age"]).copy()
            if not agent_data.empty:
                agent_data["Age Group"] = pd.cut(
                    agent_data["Agent_Age"], bins=[0, 25, 40, float("inf")],
                    labels=["Under 25", "25–40", "Over 40"], right=False, include_lowest=True
                )
                fig = px.scatter(agent_data,x="Agent_Rating",y="Delivery_Time",color="Age Group",color_discrete_sequence=PALETTE,opacity=.72,hover_data=["Order_ID","Area","Vehicle"],title="Rating vs Delivery Time by Agent Age Group")
                st.plotly_chart(style_chart(fig,315),use_container_width=True)
        with right:
            chart_heading("📦 Delivery Time by Category","Compare distributions, medians and outliers.")
            category_data = filtered.dropna(subset=["Category","Delivery_Time"])
            if not category_data.empty:
                fig = px.box(category_data,x="Category",y="Delivery_Time",color="Category",color_discrete_sequence=PALETTE,points="outliers",title="Category Distribution")
                st.plotly_chart(style_chart(fig,315),use_container_width=True)

    elif page == "📊  Delay Analysis":
        chart_heading("🌦️ Delay Analyzer", "Required bar chart: average delivery time for each weather and traffic combination.")
        data = filtered.dropna(subset=["Weather", "Traffic", "Delivery_Time"]).copy()
        if not data.empty:
            delay_summary = (
                data.groupby(["Weather", "Traffic"], as_index=False)
                .agg(Average_Time=("Delivery_Time", "mean"), Records=("Order_ID", "count"))
            )
            delay_summary["Weather × Traffic"] = (
                delay_summary["Weather"].astype(str) + " × " + delay_summary["Traffic"].astype(str)
            )
            delay_summary = delay_summary.sort_values("Average_Time", ascending=True)
            fig = px.bar(
                delay_summary, x="Weather × Traffic", y="Average_Time",
                color="Weather", hover_data=["Traffic", "Records"],
                color_discrete_sequence=PALETTE,
                labels={"Average_Time": "Average delivery time", "Weather × Traffic": "Weather × Traffic"},
                title="Average Delivery Time by Weather and Traffic"
            )
            fig.update_layout(xaxis_tickangle=-35)
            st.plotly_chart(style_chart(fig, 450), use_container_width=True)
            st.dataframe(
                delay_summary[["Weather", "Traffic", "Average_Time", "Records"]].round(2),
                use_container_width=True, hide_index=True
            )
        else:
            st.info("No delivery-time records match the selected filters.")

    elif page == "🚚  Vehicle Performance":
        chart_heading("🚚 Fleet Intelligence","Compare average and median delivery times with sample counts.")
        data = filtered.dropna(subset=["Vehicle","Delivery_Time"])
        summary = data.groupby("Vehicle").agg(Average=("Delivery_Time","mean"),Median=("Delivery_Time","median"),Records=("Order_ID","count")).reset_index().sort_values("Average")
        if not summary.empty:
            fig = px.bar(summary,x="Average",y="Vehicle",orientation="h",color="Average",color_continuous_scale=["#08d6b0","#087cff","#9c49ff"],text="Records",hover_data=["Median"],title="Average Delivery Time by Vehicle")
            fig.update_traces(texttemplate="%{text} records",textposition="outside")
            st.plotly_chart(style_chart(fig,410),use_container_width=True)
            st.dataframe(summary.round(2),use_container_width=True,hide_index=True)
            st.caption("Interpret small vehicle groups cautiously.")

    elif page == "👤  Agent Performance":
        chart_heading("👤 Agent Insights","Explore associations between rating, age and delivery time.")
        data = filtered.dropna(subset=["Agent_Rating","Delivery_Time","Agent_Age"]).copy()
        if not data.empty:
            data["Age Group"] = pd.cut(
                data["Agent_Age"], bins=[0, 25, 40, float("inf")],
                labels=["Under 25", "25–40", "Over 40"], right=False, include_lowest=True
            )
            fig = px.scatter(data,x="Agent_Rating",y="Delivery_Time",color="Age Group",color_discrete_sequence=PALETTE,opacity=.72,hover_data=["Order_ID","Area","Vehicle"],title="Agent Rating vs Delivery Time by Age Group")
            st.plotly_chart(style_chart(fig,410),use_container_width=True)
            st.caption("Association does not prove cause and effect.")
            age_summary = data.groupby("Age Group",observed=False).agg(Average=("Delivery_Time","mean"),Records=("Order_ID","count")).reset_index()
            fig = px.bar(age_summary,x="Age Group",y="Average",color="Age Group",color_discrete_sequence=PALETTE,hover_data=["Records"],title="Average Time by Agent Age Group")
            st.plotly_chart(style_chart(fig,320),use_container_width=True)

    elif page == "🗺️  Area Insights":
        chart_heading("🗺️ Regional Bottleneck Finder","Compare area and traffic combinations, with sample sizes.")
        data = filtered.dropna(subset=["Area","Traffic","Delivery_Time"])
        if not data.empty:
            matrix = data.pivot_table(index="Area",columns="Traffic",values="Delivery_Time",aggfunc="mean")
            fig = px.imshow(matrix,text_auto=".1f",aspect="auto",color_continuous_scale=["#087cff","#18d8ef","#ed28d8"],labels=dict(x="Traffic",y="Area",color="Mean time"),title="Area × Traffic Heatmap")
            st.plotly_chart(style_chart(fig,410),use_container_width=True)
            st.dataframe(data.groupby("Area").agg(Average=("Delivery_Time","mean"),Records=("Order_ID","count")).reset_index().sort_values("Average",ascending=False).round(2),use_container_width=True,hide_index=True)

    elif page == "📦  Category Analysis":
        chart_heading("📦 Category Watch","Compare delivery-time distributions across product categories.")
        data = filtered.dropna(subset=["Category","Delivery_Time"])
        if not data.empty:
            fig = px.box(data,x="Category",y="Delivery_Time",color="Category",color_discrete_sequence=PALETTE,points="outliers",title="Delivery Time Distribution by Category")
            st.plotly_chart(style_chart(fig,410),use_container_width=True)
            st.dataframe(data.groupby("Category").agg(Average=("Delivery_Time","mean"),Median=("Delivery_Time","median"),Orders=("Order_ID","count")).reset_index().sort_values("Average",ascending=False).round(2),use_container_width=True,hide_index=True)

    elif page == "🗂️  Data Explorer":
        chart_heading("🗂️ Dataset Explorer","Inspect filtered rows and data quality.")
        a,b,c = st.columns(3)
        a.metric("Filtered records",f"{len(filtered):,}")
        b.metric("Missing cells",f"{int(filtered.isna().sum().sum()):,}")
        c.metric("Duplicate rows",f"{int(filtered.duplicated().sum()):,}")
        st.dataframe(filtered.head(150),use_container_width=True,hide_index=True)
        st.download_button("⬇️ Download filtered CSV",filtered.to_csv(index=False).encode("utf-8"),"logisight_filtered_data.csv","text/csv")
        st.download_button(
            "⬇️ Download full original dataset",
            df.to_csv(index=False).encode("utf-8"),
            "logisight_full_dataset.csv",
            "text/csv"
        )
        with st.expander("Column types and missing values"):
            quality = pd.DataFrame({
                "Column": df.columns,
                "Data type": df.dtypes.astype(str).values,
                "Missing values": df.isna().sum().values,
                "Missing %": (df.isna().mean().values * 100).round(2)
            })
            st.dataframe(quality,use_container_width=True,hide_index=True)
            st.caption("Missing values are reported transparently. Weather blanks are labelled Unknown; other missing values are not silently replaced.")

st.markdown("<hr><div style='text-align:center;color:#7698c3;font-size:10px;letter-spacing:1px'>LOGISIGHT 360 · LAST-MILE DELIVERY INTELLIGENCE · INSIGHTS FROM THE SELECTED DATASET</div>",unsafe_allow_html=True)
