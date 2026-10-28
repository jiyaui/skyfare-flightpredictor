import streamlit as st
import pandas as pd
import joblib
import altair as alt
 
st.set_page_config(page_title="SkyFare | Flight Fare Predictor", page_icon="✈️", layout="wide")
 
# ---------------------------------------------------------------- styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
 
html, body, [class*="css"], .stApp { font-family: 'Poppins', sans-serif; }
.stApp { background: linear-gradient(180deg, #EEF4FF 0%, #F8FAFF 40%, #FFFFFF 100%); }
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem; max-width: 1150px; }
 
/* Hero */
.hero {
    background: linear-gradient(135deg, #1E3A8A 0%, #2563EB 55%, #38BDF8 100%);
    border-radius: 28px; padding: 46px 48px; color: white; margin-bottom: 28px;
    box-shadow: 0 20px 45px rgba(37, 99, 235, 0.28); position: relative; overflow: hidden;
}
.hero:after {
    content: "✈"; position: absolute; right: 40px; top: -10px; font-size: 190px;
    opacity: 0.12; transform: rotate(-12deg);
}
.hero h1 { font-size: 2.8rem; font-weight: 800; margin: 0 0 6px 0; color: white; letter-spacing: -1px; }
.hero p { font-size: 1.05rem; opacity: 0.92; margin: 0; max-width: 620px; font-weight: 400; }
.badges { margin-top: 20px; }
.badge {
    display: inline-block; background: rgba(255,255,255,0.18); border: 1px solid rgba(255,255,255,0.35);
    padding: 6px 14px; border-radius: 999px; font-size: 0.8rem; margin-right: 8px; font-weight: 500;
}
 
/* Section titles */
.section-title { font-size: 1.15rem; font-weight: 700; color: #0F172A; margin: 8px 0 12px 0; }
.muted { color: #64748B; font-size: 0.88rem; }
 
/* Bordered containers act as cards */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: white; border-radius: 20px !important; border: 1px solid #E2E8F0 !important;
    box-shadow: 0 6px 24px rgba(15, 23, 42, 0.06);
}
 
/* Tabs */
.stTabs [data-baseweb="tab-list"] { gap: 8px; background: #E8EEFB; padding: 6px; border-radius: 14px; }
.stTabs [data-baseweb="tab"] { border-radius: 10px; padding: 10px 22px; font-weight: 600; color: #475569; background: transparent; }
.stTabs [aria-selected="true"] { background: white !important; color: #1D4ED8 !important; box-shadow: 0 2px 8px rgba(0,0,0,0.08); }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }
 
/* Buttons */
.stButton > button {
    background: linear-gradient(135deg, #2563EB, #1D4ED8); color: white; border: none;
    border-radius: 12px; padding: 12px 28px; font-weight: 600; font-size: 1rem;
    box-shadow: 0 8px 20px rgba(37, 99, 235, 0.3); transition: all 0.2s ease;
}
.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 12px 26px rgba(37, 99, 235, 0.4); color: white; border: none; }
 
/* KPI cards */
.kpi { background: white; border: 1px solid #E2E8F0; border-radius: 18px; padding: 20px 22px; box-shadow: 0 6px 20px rgba(15,23,42,0.06); height: 100%; }
.kpi.accent { background: linear-gradient(135deg, #2563EB, #38BDF8); border: none; color: white; }
.kpi-label { font-size: 0.78rem; text-transform: uppercase; letter-spacing: 0.8px; color: #64748B; font-weight: 600; }
.kpi.accent .kpi-label { color: rgba(255,255,255,0.85); }
.kpi-value { font-size: 2rem; font-weight: 800; color: #0F172A; line-height: 1.2; margin-top: 4px; }
.kpi.accent .kpi-value { color: white; }
.kpi-sub { font-size: 0.82rem; color: #94A3B8; margin-top: 2px; }
.kpi.accent .kpi-sub { color: rgba(255,255,255,0.85); }
 
/* Rank cards */
.rank { background: white; border: 1px solid #E2E8F0; border-radius: 18px; padding: 18px 20px; box-shadow: 0 6px 20px rgba(15,23,42,0.06); }
.rank.gold { border: 2px solid #F59E0B; background: linear-gradient(180deg, #FFFBEB, #FFFFFF); }
.rank-medal { font-size: 1.6rem; }
.rank-airline { font-size: 1.1rem; font-weight: 700; color: #0F172A; margin-top: 2px; }
.rank-detail { font-size: 0.82rem; color: #64748B; margin-top: 2px; }
.rank-price { font-size: 1.7rem; font-weight: 800; color: #1D4ED8; margin-top: 8px; }
 
/* Callouts */
.tip { background: #ECFDF5; border-left: 5px solid #10B981; border-radius: 12px; padding: 14px 18px; color: #065F46; font-size: 0.92rem; margin-top: 14px; }
.info { background: #EFF6FF; border-left: 5px solid #3B82F6; border-radius: 12px; padding: 14px 18px; color: #1E3A8A; font-size: 0.92rem; margin-top: 14px; }
 
.footer { text-align: center; color: #94A3B8; font-size: 0.82rem; margin-top: 40px; padding: 18px; }
 
 
/* ---------- Cards (works across Streamlit versions) ---------- */
[class*="st-key-card_"] {
    background: white; border: 1px solid #E2E8F0; border-radius: 20px;
    padding: 1.4rem 1.6rem; box-shadow: 0 6px 24px rgba(15, 23, 42, 0.07);
}
 
/* ---------- Light inputs, even if the system uses dark mode ---------- */
.stApp, .stApp p, .stApp label { color: #1E293B; }
div[data-baseweb="select"] > div { background: #F1F5F9 !important; border: 1px solid #CBD5E1 !important; border-radius: 12px !important; }
div[data-baseweb="select"] * { color: #0F172A !important; }
div[data-baseweb="popover"] ul { background: white !important; }
div[data-baseweb="popover"] li { background: white !important; color: #0F172A !important; }
div[data-baseweb="popover"] li:hover { background: #E0ECFF !important; }
.stSelectbox label p, .stSlider label p { font-weight: 600; color: #334155 !important; }
 
/* ---------- Responsive: large screens (laptops / desktops) ---------- */
@media (min-width: 993px) {
    .block-container { max-width: 1320px; padding-top: 2rem; }
    .hero { padding: 64px 64px; border-radius: 32px; }
    .hero:after { font-size: 260px; right: 60px; }
    .hero h1 { font-size: 3.8rem; }
    .hero p { font-size: 1.3rem; max-width: 760px; }
    .badge { font-size: 1rem; padding: 8px 18px; }
    .section-title { font-size: 1.5rem; }
    .stSelectbox label p, .stSlider label p { font-size: 1.05rem !important; }
    div[data-baseweb="select"] > div { min-height: 54px; font-size: 1.05rem; }
    .stButton > button { font-size: 1.15rem; padding: 14px 36px; }
    .stTabs [data-baseweb="tab"] { font-size: 1.1rem; padding: 14px 30px; }
    .kpi { padding: 26px 28px; }
    .kpi-label { font-size: 0.9rem; }
    .kpi-value { font-size: 2.6rem; }
    .kpi-sub { font-size: 0.95rem; }
    .rank { padding: 24px 26px; }
    .rank-airline { font-size: 1.35rem; }
    .rank-detail { font-size: 1rem; }
    .rank-price { font-size: 2.1rem; }
    .tip, .info { font-size: 1.05rem; padding: 18px 22px; }
    .footer { font-size: 0.95rem; }
}
 
/* ---------- Responsive: tablet ---------- */
@media (max-width: 992px) {
    .block-container { padding-left: 1.5rem; padding-right: 1.5rem; }
    .hero { padding: 36px 32px; }
    .hero h1 { font-size: 2.3rem; }
    .kpi-value { font-size: 1.7rem; }
}
 
/* ---------- Responsive: phone ---------- */
@media (max-width: 640px) {
    .block-container { padding: 0.8rem 0.8rem 2rem 0.8rem; }
    .hero { padding: 26px 20px; border-radius: 20px; margin-bottom: 18px; }
    .hero:after { font-size: 110px; right: 6px; top: 0; }
    .hero h1 { font-size: 1.8rem; letter-spacing: -0.5px; }
    .hero p { font-size: 0.92rem; }
    .badge { font-size: 0.7rem; padding: 4px 10px; margin: 0 4px 6px 0; }
    .section-title { font-size: 1.02rem; }
    .kpi { padding: 14px 16px; border-radius: 14px; margin-bottom: 10px; }
    .kpi-value { font-size: 1.5rem; }
    .rank { padding: 14px 16px; margin-bottom: 10px; }
    .rank-price { font-size: 1.4rem; }
    .stTabs [data-baseweb="tab-list"] { gap: 4px; padding: 4px; }
    .stTabs [data-baseweb="tab"] { padding: 8px 10px; font-size: 0.82rem; }
    .stButton > button { width: 100%; padding: 12px 10px; }
    .tip, .info { font-size: 0.85rem; padding: 12px 14px; }
    .footer { font-size: 0.74rem; margin-top: 24px; }
}
</style>
""", unsafe_allow_html=True)
 
 
# ---------------------------------------------------------------- model
@st.cache_resource
def load_model():
    model = joblib.load("rf_model.pkl")
    columns = joblib.load("model_columns.pkl")
    options = pd.read_csv("route_options.csv")
    return model, columns, options
 
 
model, columns, options = load_model()
 
 
def make_row(airline, cls, source, destination, departure, arrival, stops, duration, days_left):
    row = pd.DataFrame(0, index=[0], columns=columns)
    row["Duration"] = duration
    row["Days_left"] = days_left
    for col, val in [("Airline", airline), ("Class", cls), ("Source", source),
                     ("Destination", destination), ("Departure", departure),
                     ("Arrival", arrival), ("Total_stops", stops)]:
        name = f"{col}_{val}"
        if name in row.columns:
            row[name] = 1
    return row
 
 
def kpi(label, value, sub="", accent=False):
    cls = "kpi accent" if accent else "kpi"
    return f'<div class="{cls}"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-sub">{sub}</div></div>'
 
 
# ---------------------------------------------------------------- hero
st.markdown("""
<div class="hero">
    <h1>SkyFare ✈️</h1>
    <p>Find out the smartest time to book your flight, and the cheapest options when you need to fly in a hurry.</p>
    <div class="badges">
        <span class="badge">🤖 Random Forest model</span>
        <span class="badge">📊 4.4 lakh+ fares</span>
        <span class="badge">🗓️ Jan-Mar 2023 data</span>
    </div>
</div>
""", unsafe_allow_html=True)
 
# ---------------------------------------------------------------- route selection
with st.container(border=True, key="card_route"):
    st.markdown('<div class="section-title">🧭 Plan your trip</div>', unsafe_allow_html=True)
    cities = sorted(options["Source"].unique())
    c1, c2, c3 = st.columns(3)
    source = c1.selectbox("From", cities, index=cities.index("Delhi") if "Delhi" in cities else 0)
    destination = c2.selectbox("To", [c for c in cities if c != source])
    cls = c3.selectbox("Class", ["Economy", "Business", "Premium Economy"])
 
route = options[(options["Source"] == source) & (options["Destination"] == destination)
                & (options["Class"] == cls)]
 
st.write("")
if route.empty:
    st.warning("No data available for this route and class. Please try another combination.")
    st.stop()
 
tab1, tab2 = st.tabs(["📅  Best Time to Book", "⚡  Emergency Mode"])
 
# ---------------------------------------------------------------- tab 1
with tab1:
    with st.container(border=True, key="card_flight"):
        st.markdown('<div class="section-title">Choose your flight</div>', unsafe_allow_html=True)
        a1, a2 = st.columns(2)
        airline = a1.selectbox("Airline", sorted(route["Airline"].unique()))
        r1 = route[route["Airline"] == airline]
        stops = a2.selectbox("Stops", sorted(r1["Total_stops"].unique()))
        r2 = r1[r1["Total_stops"] == stops]
        a3, a4 = st.columns(2)
        departure = a3.selectbox("Departure time", sorted(r2["Departure"].unique()))
        r3 = r2[r2["Departure"] == departure]
        arrival = a4.selectbox("Arrival time", sorted(r3["Arrival"].unique()))
        duration = r3[r3["Arrival"] == arrival]["Duration_in_hours"].mean()
        go = st.button("🔍  Find best time to book", key="btn_best")
 
    if go:
        days = list(range(1, 51))
        rows = pd.concat([make_row(airline, cls, source, destination, departure,
                                   arrival, stops, duration, d) for d in days], ignore_index=True)
        res = pd.DataFrame({"days_left": days, "predicted_fare": model.predict(rows)})
        cheapest = res.loc[res["predicted_fare"].idxmin()]
        practical = int(res[res["predicted_fare"] <= cheapest["predicted_fare"] * 1.03]["days_left"].min())
        fare_practical = res.loc[res["days_left"] == practical, "predicted_fare"].iloc[0]
        fare_last = res.loc[res["days_left"] == 1, "predicted_fare"].iloc[0]
        saving = fare_last - fare_practical
 
        st.write("")
        k1, k2, k3 = st.columns(3)
        k1.markdown(kpi("Book at least", f"{practical} days", "before departure", accent=True), unsafe_allow_html=True)
        k2.markdown(kpi("Fare at that point", f"₹{fare_practical:,.0f}", "predicted"), unsafe_allow_html=True)
        k3.markdown(kpi("You save vs last-minute", f"₹{saving:,.0f}", f"1-day fare ₹{fare_last:,.0f}"), unsafe_allow_html=True)
 
        st.write("")
        with st.container(border=True, key="card_chart"):
            st.markdown('<div class="section-title">📈 How the fare changes as departure gets closer</div>', unsafe_allow_html=True)
            base = alt.Chart(res).encode(
                x=alt.X("days_left:Q", title="Days before departure"),
                y=alt.Y("predicted_fare:Q", title="Predicted fare (₹)", scale=alt.Scale(zero=False)),
                tooltip=[alt.Tooltip("days_left:Q", title="Days left"),
                         alt.Tooltip("predicted_fare:Q", title="Fare (₹)", format=",.0f")],
            )
            area = base.mark_area(opacity=0.15, color="#2563EB")
            line = base.mark_line(color="#2563EB", strokeWidth=3,
                                  point=alt.OverlayMarkDef(color="#2563EB", size=45))
            rule = alt.Chart(pd.DataFrame({"x": [practical]})).mark_rule(
                color="#EF4444", strokeDash=[6, 4], strokeWidth=2).encode(x="x:Q")
            st.altair_chart((area + line + rule).properties(height=340), use_container_width=True)
            st.markdown(f'<div class="muted">Red dashed line = practical best time ({practical} days before). '
                        f'After this point the fare stays almost flat.</div>', unsafe_allow_html=True)
 
        st.markdown(f'<div class="tip">💡 <b>Tip:</b> Booking {practical}+ days ahead instead of 1 day before '
                    f'could save you around <b>₹{saving:,.0f}</b> on this flight.</div>', unsafe_allow_html=True)
 
# ---------------------------------------------------------------- tab 2
with tab2:
    with st.container(border=True, key="card_emergency"):
        st.markdown('<div class="section-title">Need to fly soon?</div>', unsafe_allow_html=True)
        days_left = st.slider("Days until departure", 1, 7, 1)
        go2 = st.button("⚡  Find cheapest options", key="btn_emergency")
 
    if go2:
        combos = route[route["Airline"] != "GO FIRST"].groupby(
            ["Airline", "Total_stops", "Departure", "Arrival"])["Duration_in_hours"].mean().reset_index()
        rows = pd.concat([make_row(r.Airline, cls, source, destination, r.Departure, r.Arrival,
                                   r.Total_stops, r.Duration_in_hours, days_left)
                          for r in combos.itertuples()], ignore_index=True)
        combos["predicted_fare"] = model.predict(rows).round(0)
        combos = combos.sort_values("predicted_fare").reset_index(drop=True)
 
        st.write("")
        st.markdown('<div class="section-title">🏆 Top 3 cheapest options</div>', unsafe_allow_html=True)
        medals = ["🥇", "🥈", "🥉"]
        cols = st.columns(3)
        for i, col in enumerate(cols[:min(3, len(combos))]):
            r = combos.iloc[i]
            gold = " gold" if i == 0 else ""
            col.markdown(
                f'<div class="rank{gold}"><div class="rank-medal">{medals[i]}</div>'
                f'<div class="rank-airline">{r["Airline"]}</div>'
                f'<div class="rank-detail">{r["Total_stops"]} · {r["Departure"]} → {r["Arrival"]}</div>'
                f'<div class="rank-detail">{r["Duration_in_hours"]:.1f} hrs</div>'
                f'<div class="rank-price">₹{r["predicted_fare"]:,.0f}</div></div>',
                unsafe_allow_html=True)
 
        by_stops = combos.groupby("Total_stops")["predicted_fare"].min()
        if "non-stop" in by_stops.index and "1-stop" in by_stops.index:
            diff = by_stops["1-stop"] - by_stops["non-stop"]
            msg = (f"A 1-stop flight costs about <b>₹{diff:,.0f} more</b> than non-stop on this route."
                   if diff > 0 else
                   f"A 1-stop flight is about <b>₹{abs(diff):,.0f} cheaper</b> than non-stop on this route.")
            st.markdown(f'<div class="info">✈️ {msg}</div>', unsafe_allow_html=True)
 
        by_slot = combos.groupby("Departure")["predicted_fare"].min().sort_values()
        st.markdown(f'<div class="tip">🕒 Cheapest departure slot: <b>{by_slot.index[0]}</b> '
                    f'(about ₹{by_slot.iloc[0]:,.0f}). Travelling on a Sunday is usually more expensive in this dataset.</div>',
                    unsafe_allow_html=True)
 
        st.write("")
        with st.expander("See all options"):
            show = combos.rename(columns={"Total_stops": "Stops", "Duration_in_hours": "Duration (hrs)",
                                          "predicted_fare": "Fare (₹)"}).head(15)
            st.dataframe(show, use_container_width=True, hide_index=True,
                         column_config={"Duration (hrs)": st.column_config.NumberColumn(format="%.1f"),
                                        "Fare (₹)": st.column_config.NumberColumn(format="₹%d")})
 
# ---------------------------------------------------------------- footer
st.markdown(
    '<div class="footer">'
    '<div style="font-size:1rem; font-weight:600; color:#1D4ED8; margin-bottom:6px;">Made by Jiya</div>'
    'College data science project · Trained on Jan-Mar 2023 Indian domestic fares · '
    'Estimates show patterns, not live prices'
    '</div>', unsafe_allow_html=True)