"""
SIERRA LEONE HEALTH EMERGENCIES DASHBOARD 
=======================================================
MSBA382 - Healthcare Analytics Individual Project
A comprehensive analysis of health emergencies, disease burden,
and health system access in Sierra Leone (2014-2024).

Pages:
  0. Password Landing
  1. Overview
  2. Ebola (2014-2016)
  3. COVID-19 (2020-2024)
  4. Disease Burden & WASH
  5. Malaria
  6. Health System Access
  7. Compare Emergencies
  8. Sierra Leone Map
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Sierra Leone Health Dashboard",
    page_icon="🇸🇱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM CSS
# ============================================================
st.markdown("""
<style>
    .main { background-color: #0e1117; }
    .metric-card {
        background-color: #1e2130;
        border-radius: 10px;
        padding: 20px;
        text-align: center;
        border-left: 4px solid #e74c3c;
    }
    .metric-card h2 { color: #ffffff; font-size: 2rem; margin: 0; }
    .metric-card p  { color: #a0a0a0; font-size: 0.9rem; margin: 0; }
    .insight-box {
        background-color: #1e2130;
        border-left: 4px solid #f39c12;
        padding: 15px 20px;
        border-radius: 5px;
        margin: 10px 0;
        color: #e0e0e0;
    }
    .section-header {
        color: #e74c3c;
        font-size: 1.1rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# PASSWORD PROTECTION
# ============================================================
PASSWORD = "sierraleone2026"

def check_password():
    if "password_correct" not in st.session_state:
        st.markdown("""
        <div style='text-align:center; padding: 60px 0 20px 0;'>
            <h1>🇸🇱 Sierra Leone Health Emergencies Dashboard</h1>
            <p style='color:#a0a0a0;'>MSBA382 Healthcare Analytics · AUB Suliman S. Olayan School of Business</p>
        </div>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            pwd = st.text_input("Enter access password", type="password",
                                key="pwd_input")
            if st.button("Access Dashboard", use_container_width=True):
                if pwd == PASSWORD:
                    st.session_state["password_correct"] = True
                    st.rerun()
                else:
                    st.error("Incorrect password. Please try again.")
        return False
    return st.session_state["password_correct"]

if not check_password():
    st.stop()

# ============================================================
# LOAD DATA
# ============================================================
@st.cache_data
def load_all_data():
    covid          = pd.read_csv("data/covid_sierra_leone_clean.csv",
                                  parse_dates=["date"])
    ebola          = pd.read_csv("data/ebola_sierra_leone_clean.csv",
                                  parse_dates=["report_date"])
    ebola_sub      = pd.read_csv("data/ebola_sierra_leone_subtypes.csv")
    ebola_district = pd.read_csv("data/ebola_district_sierra_leone.csv",
                                  parse_dates=["date"])
    causes         = pd.read_csv("data/causes_of_death_sierra_leone.csv")
    covid_district = pd.read_csv("data/covid_district_sierra_leone.csv",
                                  parse_dates=["date"])
    malaria_map    = pd.read_csv("data/malaria_spatial_sierra_leone.csv")
    malaria_ind    = pd.read_csv("data/malaria_indicators_sierra_leone.csv")
    access         = pd.read_csv("data/access_health_sierra_leone.csv")
    wash           = pd.read_csv("data/wash_sierra_leone.csv")
    return (covid, ebola, ebola_sub, ebola_district, causes,
            covid_district, malaria_map, malaria_ind, access, wash)

(covid_sl, ebola_sl, ebola_sub, ebola_dist, causes,
 covid_dist, malaria_map, malaria_ind, access, wash) = load_all_data()

# Pre-compute category summary
category_map = {
    'Malaria': 'Infectious Disease',
    'Lower respiratory infections': 'Infectious Disease',
    'Diarrhoeal diseases': 'Infectious Disease',
    'Tuberculosis': 'Infectious Disease',
    'HIV/AIDS': 'Infectious Disease',
    'Meningitis': 'Infectious Disease',
    'Stroke': 'Non-Communicable Disease',
    'Ischaemic heart disease': 'Non-Communicable Disease',
    'Cirrhosis of the liver': 'Non-Communicable Disease',
    'Diabetes mellitus': 'Non-Communicable Disease',
    'Preterm birth complications': 'Maternal & Child Health',
    'Birth asphyxia and birth trauma': 'Maternal & Child Health',
    'Protein-energy malnutrition': 'Maternal & Child Health',
    'Congenital anomalies': 'Maternal & Child Health',
    'Road injury': 'Injury'
}
causes['Category'] = causes['Cause'].map(category_map)
cat_summary = causes.groupby('Category')['Death_Rate_per_100k'].sum().reset_index()

# ============================================================
# SIDEBAR NAVIGATION
# ============================================================
st.sidebar.markdown("""
<div style='text-align:center; padding: 10px 0;'>
    <h2 style='color:#e74c3c;'>🇸🇱 Sierra Leone</h2>
    <p style='color:#a0a0a0; font-size:0.8rem;'>Health Emergencies Dashboard</p>
</div>
""", unsafe_allow_html=True)

page = st.sidebar.radio("Navigate", [
    " Overview",
    " Ebola (2014–2016)",
    " COVID-19 (2020–2024)",
    " Disease Burden & WASH",
    " Malaria",
    " Health System Access",
    " Compare Emergencies",
    "  Sierra Leone Map"
])

st.sidebar.markdown("---")
st.sidebar.markdown("""
<div style='color:#a0a0a0; font-size:0.75rem;'>
<b>Data Sources</b><br>
• WHO Ebola Situation Reports<br>
• Our World in Data (COVID-19)<br>
• WHO Global Health Estimates<br>
• DHS Program (Malaria/Access)<br>
• MOHS Sierra Leone (Subnational)<br>
• WHO WASH Data<br><br>
<b>Course:</b> MSBA382 Healthcare Analytics<br>
<b>Institution:</b> AUB – OSB<br>
<b>Period:</b> 2014–2024
</div>
""", unsafe_allow_html=True)


# ============================================================
# PAGE 1: OVERVIEW
# ============================================================
if page == " Overview":
    st.title("Sierra Leone Health Emergencies Dashboard")
    st.markdown("### A decade of crisis and resilience (2014–2024)")
    st.markdown(
        "This dashboard provides a comprehensive analytical view of Sierra Leone's "
        "major health emergencies over the past decade the 2014–2016 Ebola epidemic, "
        "the 2020–2024 COVID-19 pandemic alongside the country's everyday infectious "
        "disease burden, malaria patterns, WASH-related mortality, and health system "
        "access indicators."
    )

    st.markdown("---")

    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔴 Ebola Total Cases",
                   f"{int(ebola_sl['Total cases'].max()):,}")
        st.metric("Ebola Total Deaths",
                   f"{int(ebola_sl['Total deaths'].max()):,}",
                   delta=f"{ebola_sl['CFR_percent'].iloc[-1]:.1f}% CFR",
                   delta_color="off")
    with col2:
        st.metric("🔵 COVID-19 Total Cases",
                   f"{int(covid_sl['total_cases'].max()):,}")
        st.metric("COVID-19 Total Deaths",
                   f"{int(covid_sl['total_deaths'].max()):,}",
                   delta=f"{covid_sl['total_deaths'].max()/covid_sl['total_cases'].max()*100:.1f}% CFR",
                   delta_color="off")
    with col3:
        st.metric(" Top Cause of Death",
                   "Malaria",
                   delta="101.1 per 100k (2021)",
                   delta_color="off")
        st.metric("WASH Death Rate",
                   "69.5 per 100k",
                   delta="Males 78.9 vs Females 60.2",
                   delta_color="off")
    with col4:
        st.metric(" Facility Births",
                   "~87%",
                   delta="Up from 54% in 2008",
                   delta_color="normal")
        st.metric("Malaria Prevalence",
                   "Up to 78%",
                   delta="Koinadugu district (2016)",
                   delta_color="off")

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Disease burden by category (2021)")
        fig_pie = px.pie(
            cat_summary,
            values='Death_Rate_per_100k', names='Category',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            height=350, margin=dict(t=20, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font_color='white'
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col2:
        st.subheader("Key finding")
        st.markdown("""
        <div class='insight-box'>
        <b>Infectious disease dominates Sierra Leone's burden</b><br><br>
        54.4% of the top-15 causes of death in Sierra Leone are infectious diseases —
        more than double the share of non-communicable disease (25.1%). Malaria alone
        kills at a rate of 101 per 100,000 population annually.<br><br>
        <b>Ebola vs COVID-19:</b> While Ebola produced more total confirmed cases
        (14,122 vs 7,979 ), Ebola's 28% CFR was 17x higher than COVID-19's 1.6% CFR,
        demanding fundamentally different response strategies.<br><br>
        <b>Geographic inequality:</b> Malaria prevalence ranges from 78% in Koinadugu
        to just 3.8% in Western Urban — a 20x gap driven by access and infrastructure.
        </div>
        """, unsafe_allow_html=True)

        st.subheader("Dashboard guide")
        st.markdown("""
        | Page | What you'll find |
        |------|-----------------|
        |  Ebola | Timeline, CFR trend, district spread |
        |  COVID-19 | Waves, gender breakdown, vaccination |
        |  Disease Burden | Top causes, WASH gender gap |
        |  Malaria | District prevalence, ITN coverage |
        |  Health Access | Facility births, ANC, vaccination |
        |  Compare | Side-by-side emergency comparison |
        |  Map | Sierra Leone district map |
        """)


# ============================================================
# PAGE 2: EBOLA
# ============================================================
elif page == " Ebola (2014–2016)":
    st.title("Ebola Virus Disease Outbreak (2014–2016)")
    st.markdown(
        "Sierra Leone was the most affected country in the largest Ebola outbreak "
        "in history, recording more cases than any other nation in the epidemic."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Cases", f"{int(ebola_sl['Total cases'].max()):,}")
    with col2:
        st.metric("Total Deaths", f"{int(ebola_sl['Total deaths'].max()):,}")
    with col3:
        st.metric("Final CFR", f"{ebola_sl['CFR_percent'].iloc[-1]:.1f}%")
    with col4:
        duration = (ebola_sl['report_date'].max() - ebola_sl['report_date'].min()).days
        st.metric("Outbreak Duration", f"{duration} days")

    st.markdown("---")

    # Cumulative timeline
    st.subheader("Cumulative cases and deaths over time")
    fig_ebola = go.Figure()
    fig_ebola.add_trace(go.Scatter(
        x=ebola_sl['report_date'], y=ebola_sl['Total cases'],
        mode='lines', name='Total Cases',
        line=dict(color='#e74c3c', width=3),
        fill='tozeroy', fillcolor='rgba(231,76,60,0.15)'
    ))
    fig_ebola.add_trace(go.Scatter(
        x=ebola_sl['report_date'], y=ebola_sl['Total deaths'],
        mode='lines', name='Total Deaths',
        line=dict(color='#ffffff', width=2, dash='dash')
    ))
    fig_ebola.update_layout(
        xaxis_title='Report Date', yaxis_title='Cumulative Count',
        hovermode='x unified', template='plotly_dark', height=420,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(bgcolor='rgba(0,0,0,0)')
    )
    st.plotly_chart(fig_ebola, use_container_width=True)

    st.caption(
        "Note: Two minor downward revisions in WHO's reporting (Nov 2014, Aug 2015) "
        "reflect case reclassification and were smoothed using cumulative maximum "
        "methodology. Raw values are preserved in the underlying dataset."
    )

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Case fatality rate over time")
        fig_cfr = px.line(
            ebola_sl, x='report_date', y='CFR_percent',
            labels={'report_date': 'Date', 'CFR_percent': 'CFR (%)'}
        )
        fig_cfr.update_traces(line=dict(color='#f39c12', width=3))
        fig_cfr.update_layout(
            template='plotly_dark', height=380,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_cfr, use_container_width=True)
        st.markdown("""
        <div class='insight-box'>
        CFR started near <b>41%</b> in Aug 2014, reflecting limited treatment
        capacity. It declined as international response scaled, then rose again
        to ~32% during peak caseload (Apr–May 2015) before stabilizing at 28%.
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.subheader("Cases by classification (final report)")
        fig_sub = px.bar(
            ebola_sub, x='Case def.', y='Total cases',
            color='Case def.',
            color_discrete_map={
                'Confirmed': '#e74c3c',
                'Probable': '#f39c12',
                'Suspected': '#f1c40f'
            },
            text='Total cases'
        )
        fig_sub.update_traces(textposition='outside')
        fig_sub.update_layout(
            template='plotly_dark', height=380, showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_sub, use_container_width=True)

    st.markdown("---")
    st.subheader("Spread by district over time")

    # District filter
    all_districts = sorted(ebola_dist['district'].unique().tolist())
    selected_districts = st.multiselect(
        "Filter districts", all_districts, default=all_districts[:6]
    )

    ebola_dist_filtered = ebola_dist[
        ebola_dist['district'].isin(selected_districts)
    ]

    fig_dist_time = px.line(
        ebola_dist_filtered,
        x='date', y='cases', color='district',
        title='Ebola Weekly Cases by District',
        labels={'date': 'Date', 'cases': 'New Cases', 'district': 'District'}
    )
    fig_dist_time.update_layout(
        template='plotly_dark', height=420,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_dist_time, use_container_width=True)

    # Total by district bar
    st.subheader("Total cases by district (full outbreak)")
    dist_total = ebola_dist.groupby('district')['cases'].sum().reset_index()
    dist_total = dist_total.sort_values('cases', ascending=True)

    fig_dist_bar = px.bar(
        dist_total,
        x='cases', y='district', orientation='h',
        color='cases', color_continuous_scale='Reds',
        labels={'cases': 'Total Cases', 'district': 'District'},
        text='cases'
    )
    fig_dist_bar.update_traces(
        texttemplate='%{text:.0f}', textposition='outside'
    )
    fig_dist_bar.update_layout(
        template='plotly_dark', height=480,
        coloraxis_showscale=False,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_dist_bar, use_container_width=True)


# ============================================================
# PAGE 3: COVID-19
# ============================================================
elif page == " COVID-19 (2020–2024)":
    st.title("COVID-19 Pandemic (2020–2024)")
    st.markdown(
        "Sierra Leone experienced four distinct waves of COVID-19 infection. "
        "Despite limited testing capacity, the health system maintained "
        "a relatively low official CFR compared to Ebola."
    )

    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Cases", f"{int(covid_sl['total_cases'].max()):,}")
    with col2:
        st.metric("Total Deaths", f"{int(covid_sl['total_deaths'].max()):,}")
    with col3:
        cfr_covid = covid_sl['total_deaths'].max() / covid_sl['total_cases'].max() * 100
        st.metric("Overall CFR", f"{cfr_covid:.1f}%")
    with col4:
        vax_max = covid_sl['people_fully_vaccinated_per_hundred'].max()
        st.metric("Peak Vaccination", f"{vax_max:.1f}%")

    st.markdown("---")

    # Date slider
    min_date = covid_sl['date'].min().to_pydatetime()
    max_date = covid_sl['date'].max().to_pydatetime()
    date_range = st.slider(
        "Filter date range",
        min_value=min_date, max_value=max_date,
        value=(min_date, max_date)
    )

    covid_filtered = covid_sl[
        (covid_sl['date'] >= date_range[0]) &
        (covid_sl['date'] <= date_range[1])
    ]

    # Wave chart
    st.subheader("Daily new cases — four pandemic waves")
    fig_waves = px.area(
        covid_filtered, x='date', y='new_cases_smoothed',
        labels={'date': 'Date', 'new_cases_smoothed': 'New Cases (7-day avg)'}
    )
    fig_waves.update_traces(
        line=dict(color='#3498db', width=2),
        fillcolor='rgba(52,152,219,0.3)'
    )
    fig_waves.update_layout(
        template='plotly_dark', height=400,
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_waves, use_container_width=True)

    st.markdown("""
    <div class='insight-box'>
    Four distinct waves are visible. The <b>largest spike (mid-2021)</b> is
    consistent with the global Delta variant wave. Case counts dropped sharply
    after each wave, with a long quiet tail from 2022 onward.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cumulative cases & deaths")
        fig_cum = go.Figure()
        fig_cum.add_trace(go.Scatter(
            x=covid_filtered['date'], y=covid_filtered['total_cases'],
            name='Total Cases', line=dict(color='#3498db', width=3),
            fill='tozeroy', fillcolor='rgba(52,152,219,0.1)'
        ))
        fig_cum.add_trace(go.Scatter(
            x=covid_filtered['date'], y=covid_filtered['total_deaths'],
            name='Total Deaths', line=dict(color='white', width=2, dash='dash'),
            yaxis='y2'
        ))
        fig_cum.update_layout(
            yaxis=dict(title='Total Cases'),
            yaxis2=dict(title='Total Deaths', overlaying='y', side='right'),
            hovermode='x unified', template='plotly_dark', height=380,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_cum, use_container_width=True)

    with col2:
        st.subheader("Vaccination rollout")
        covid_vax = covid_sl[covid_sl['people_fully_vaccinated_per_hundred'].notnull()]
        fig_vax = px.line(
            covid_vax, x='date', y='people_fully_vaccinated_per_hundred',
            labels={'date': 'Date',
                    'people_fully_vaccinated_per_hundred': '% Fully Vaccinated'},
            markers=True
        )
        fig_vax.update_traces(
            line=dict(color='#2ecc71', width=3), marker=dict(size=5)
        )
        fig_vax.update_layout(
            template='plotly_dark', height=380,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_vax, use_container_width=True)

    st.markdown("---")
    st.subheader("Gender breakdown by province")

    gender_prov = covid_dist.groupby('region').agg(
        Female=('cases_female', 'sum'),
        Male=('cases_male', 'sum')
    ).reset_index()

    gender_long = gender_prov.melt(
        id_vars='region', var_name='Gender', value_name='Cases'
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        fig_gender = px.bar(
            gender_long, x='region', y='Cases', color='Gender',
            barmode='group',
            title='COVID-19 Cases by Province and Gender',
            labels={'region': 'Province', 'Cases': 'Total Cases'},
            color_discrete_map={'Female': '#e74c3c', 'Male': '#3498db'}
        )
        fig_gender.update_layout(
            template='plotly_dark', height=400,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_gender, use_container_width=True)

    with col2:
        total_female = covid_dist['cases_female'].sum()
        total_male   = covid_dist['cases_male'].sum()
        total_both   = total_female + total_male
        fig_pie_gender = px.pie(
            values=[total_female, total_male],
            names=['Female', 'Male'],
            color_discrete_sequence=['#e74c3c', '#3498db'],
            hole=0.4
        )
        fig_pie_gender.update_layout(
            template='plotly_dark', height=400,
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_pie_gender, use_container_width=True)
        st.metric("Female cases",
                   f"{total_female/total_both*100:.1f}%")
        st.metric("Male cases",
                   f"{total_male/total_both*100:.1f}%")


# ============================================================
# PAGE 4: DISEASE BURDEN & WASH
# ============================================================
elif page == " Disease Burden & WASH":
    st.title("Everyday Disease Burden & WASH")
    st.markdown(
        "Beyond acute emergencies, Sierra Leone faces a sustained burden of "
        "infectious and chronic disease. Unsafe water, sanitation, and hygiene "
        "(WASH) contribute significantly to this mortality."
    )

    col1, col2 = st.columns([3, 2])

    with col1:
        st.subheader("Top 15 causes of death (2021)")
        fig_causes = px.bar(
            causes.sort_values('Death_Rate_per_100k', ascending=True),
            x='Death_Rate_per_100k', y='Cause', orientation='h',
            color='Death_Rate_per_100k', color_continuous_scale='Reds',
            labels={'Death_Rate_per_100k': 'Deaths per 100,000', 'Cause': ''},
            text='Death_Rate_per_100k'
        )
        fig_causes.update_traces(
            texttemplate='%{text:.1f}', textposition='outside'
        )
        fig_causes.update_layout(
            template='plotly_dark', height=600,
            coloraxis_showscale=False,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_causes, use_container_width=True)

    with col2:
        st.subheader("Burden by category")
        fig_cat = px.pie(
            cat_summary,
            values='Death_Rate_per_100k', names='Category',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        fig_cat.update_traces(textposition='inside', textinfo='percent+label')
        fig_cat.update_layout(
            template='plotly_dark', height=380,
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_cat, use_container_width=True)

        st.markdown("""
        <div class='insight-box'>
        <b>54.4%</b> of the top-15 death burden comes from infectious
        disease — more than double the NCD share (25.1%). This confirms
        that routine disease control delivers more lives saved per dollar
        than emergency-only response capacity.
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("WASH-related mortality by gender")

    col1, col2 = st.columns([2, 1])
    with col1:
        wash_gender = wash[wash['Demographic Group'] != 'TOTAL NATIONAL BURDEN'].copy()
        wash_gender['Gender'] = wash_gender['Demographic Group'].str.replace(' Group', '')

        fig_wash = px.bar(
            wash_gender,
            x='Gender', y='Death Rate per 100k',
            color='Gender',
            color_discrete_map={'MALE': '#3498db', 'FEMALE': '#e74c3c'},
            text='Death Rate per 100k',
            title='WASH-Related Death Rate by Gender — Sierra Leone'
        )
        fig_wash.update_traces(
            texttemplate='%{text:.1f}', textposition='outside'
        )
        fig_wash.update_layout(
            template='plotly_dark', height=400, showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_wash, use_container_width=True)

    with col2:
        national_rate = wash[
            wash['Demographic Group'] == 'TOTAL NATIONAL BURDEN'
        ]['Death Rate per 100k'].values[0]

        st.metric("National WASH death rate", f"{national_rate:.1f} per 100k")
        st.metric("Male death rate", "78.9 per 100k")
        st.metric("Female death rate", "60.2 per 100k")

        st.markdown("""
        <div class='insight-box'>
        Males face a <b>31% higher</b> WASH-related death rate than females
        in Sierra Leone. This may reflect greater occupational exposure
        to unsafe water sources and lower health-seeking behavior among men.
        </div>
        """, unsafe_allow_html=True)


# ============================================================
# PAGE 5: MALARIA
# ============================================================
elif page == " Malaria":
    st.title("Malaria — Sierra Leone's Leading Cause of Death")
    st.markdown(
        "Malaria kills more people in Sierra Leone than any other single cause, "
        "at 101 deaths per 100,000 population annually. But this burden is "
        "not evenly distributed."
    )

    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Death rate", "101.1 per 100k", delta="#1 cause of death", delta_color="off")
    with col2:
        st.metric("Highest prevalence", "78.1% — Koinadugu", delta_color="off")
    with col3:
        st.metric("Lowest prevalence", "3.8% — Western Urban", delta_color="off")

    st.markdown("---")

    # Bubble map using scatter_mapbox
    st.subheader("Malaria prevalence by district (2016 DHS Survey)")
    try:
        fig_map = px.scatter_map(
            malaria_map,
            lat='lat', lon='lon',
            size='malaria_prevalence_pct',
            color='malaria_prevalence_pct',
            hover_name='district',
            hover_data={
                'malaria_prevalence_pct': ':.1f',
                'lat': False, 'lon': False
            },
            color_continuous_scale='Reds',
            size_max=35,
            zoom=6,
            center={'lat': 8.4606, 'lon': -11.7799},
            labels={'malaria_prevalence_pct': 'Prevalence (%)'}
        )
        fig_map.update_layout(
            mapbox_style='open-street-map',
            height=520,
            margin=dict(r=0, t=20, l=0, b=0)
        )
    except Exception:
        # Fallback for older Plotly versions
        fig_map = px.scatter_mapbox(
            malaria_map,
            lat='lat', lon='lon',
            size='malaria_prevalence_pct',
            color='malaria_prevalence_pct',
            hover_name='district',
            color_continuous_scale='Reds',
            size_max=35,
            zoom=6,
            center={'lat': 8.4606, 'lon': -11.7799},
            labels={'malaria_prevalence_pct': 'Prevalence (%)'}
        )
        fig_map.update_layout(
            mapbox_style='open-street-map',
            height=520,
            margin=dict(r=0, t=20, l=0, b=0)
        )

    st.plotly_chart(fig_map, use_container_width=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Malaria prevalence by district (bar chart)")
        malaria_rdt = malaria_ind[
            malaria_ind['Indicator'] == 'Malaria prevalence according to RDT'
        ].copy()

        if not malaria_rdt.empty:
            fig_rdt = px.bar(
                malaria_rdt.sort_values('Value', ascending=True),
                x='Value', y='Location', orientation='h',
                color='Value', color_continuous_scale='Reds',
                labels={'Value': 'Prevalence (%)', 'Location': 'District'},
                text='Value'
            )
            fig_rdt.update_traces(
                texttemplate='%{text:.1f}%', textposition='outside'
            )
            fig_rdt.update_layout(
                template='plotly_dark', height=550,
                coloraxis_showscale=False,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_rdt, use_container_width=True)

    with col2:
        st.subheader("ITN ownership by district")
        malaria_itn = malaria_ind[
            malaria_ind['Indicator'] == 'Households with at least one insecticide-treated mosquito net (ITN)'
        ].copy()

        if not malaria_itn.empty:
            fig_itn = px.bar(
                malaria_itn.sort_values('Value', ascending=True),
                x='Value', y='Location', orientation='h',
                color='Value', color_continuous_scale='Greens',
                labels={'Value': '% of Households', 'Location': 'District'},
                text='Value'
            )
            fig_itn.update_traces(
                texttemplate='%{text:.1f}%', textposition='outside'
            )
            fig_itn.update_layout(
                template='plotly_dark', height=550,
                coloraxis_showscale=False,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_itn, use_container_width=True)


# ============================================================
# PAGE 6: HEALTH SYSTEM ACCESS
# ============================================================
elif page == " Health System Access":
    st.title("Health System Access")
    st.markdown(
        "DHS survey data tracks key health access indicators across Sierra Leone's "
        "regions over multiple survey years, revealing trends in facility births, "
        "antenatal care coverage, and vaccination rates."
    )

    if not access.empty:
        # Indicator filter
        indicators = access['Indicator'].unique().tolist()
        selected_ind = st.selectbox(
            "Select indicator to explore",
            indicators,
            index=0
        )

        access_filtered = access[access['Indicator'] == selected_ind].copy()

        col1, col2 = st.columns(2)

        with col1:
            # Trend over time
            fig_access_trend = px.line(
                access_filtered.sort_values('SurveyYear'),
                x='SurveyYear', y='Value',
                color='Location',
                title=f'{selected_ind} — Trend Over Time',
                labels={'SurveyYear': 'Survey Year',
                        'Value': '% of Population',
                        'Location': 'Region'},
                markers=True
            )
            fig_access_trend.update_layout(
                template='plotly_dark', height=420,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(bgcolor='rgba(0,0,0,0)')
            )
            st.plotly_chart(fig_access_trend, use_container_width=True)

        with col2:
            # Latest survey year bar chart
            latest_year = access_filtered['SurveyYear'].max()
            access_latest = access_filtered[
                access_filtered['SurveyYear'] == latest_year
            ].sort_values('Value', ascending=True)

            fig_access_bar = px.bar(
                access_latest,
                x='Value', y='Location', orientation='h',
                color='Value', color_continuous_scale='Blues',
                title=f'{selected_ind} — Latest Survey ({latest_year})',
                labels={'Value': '% of Population', 'Location': 'Region'},
                text='Value'
            )
            fig_access_bar.update_traces(
                texttemplate='%{text:.1f}%', textposition='outside'
            )
            fig_access_bar.update_layout(
                template='plotly_dark', height=420,
                coloraxis_showscale=False,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_access_bar, use_container_width=True)

        st.markdown("---")
        st.subheader("Full data table")
        st.dataframe(
            access_filtered[['Location', 'SurveyYear', 'Indicator', 'Value']]
            .sort_values(['Location', 'SurveyYear'])
            .reset_index(drop=True),
            use_container_width=True
        )
    else:
        st.warning("Access to health data not available.")


# ============================================================
# PAGE 7: COMPARE EMERGENCIES
# ============================================================
elif page == " Compare Emergencies":
    st.title("Comparing Health Emergencies")
    st.markdown(
        "A side-by-side analytical comparison of Sierra Leone's two major "
        "health emergencies — Ebola (2014–2016) and COVID-19 (2020–2024)."
    )

    # Summary table
    ebola_cases  = int(ebola_sl['Total cases'].max())
    ebola_deaths = int(ebola_sl['Total deaths'].max())
    ebola_cfr    = ebola_sl['CFR_percent'].iloc[-1]
    ebola_days   = (ebola_sl['report_date'].max() - ebola_sl['report_date'].min()).days

    covid_cases  = int(covid_sl['total_cases'].max())
    covid_deaths = int(covid_sl['total_deaths'].max())
    covid_cfr    = covid_deaths / covid_cases * 100
    covid_days   = (covid_sl['date'].max() - covid_sl['date'].min()).days

    compare_df = pd.DataFrame({
        'Metric': ['Total Confirmed Cases', 'Total Deaths',
                   'Case Fatality Rate', 'Outbreak Duration'],
        'Ebola (2014–2016)': [f"{ebola_cases:,}", f"{ebola_deaths:,}",
                               f"{ebola_cfr:.1f}%", f"{ebola_days} days"],
        'COVID-19 (2020–2024)': [f"{covid_cases:,}", f"{covid_deaths:,}",
                                   f"{covid_cfr:.1f}%", f"{covid_days} days"]
    })

    st.table(compare_df.set_index('Metric'))

    st.markdown("""
    <div class='insight-box'>
    <b>Key finding:</b> While Ebola produced more total confirmed cases
    ({:,} vs {:,}), Ebola's CFR of {:.1f}% was <b>17x higher</b> than
    COVID-19's {:.1f}% CFR — reflecting Ebola's extreme severity even at
    lower case volumes. These two emergencies demanded fundamentally
    different public health responses.
    </div>
    """.format(covid_cases, ebola_cases, ebola_cfr, covid_cfr),
    unsafe_allow_html=True)

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Normalized timeline")
        st.markdown("Days since each outbreak started")

        ebola_norm = ebola_sl[['report_date', 'Total cases']].copy()
        ebola_norm['days'] = (
            ebola_norm['report_date'] - ebola_norm['report_date'].min()
        ).dt.days
        ebola_norm['outbreak'] = 'Ebola'
        ebola_norm = ebola_norm.rename(columns={'Total cases': 'cases'})

        covid_norm = covid_sl[['date', 'total_cases']].copy()
        covid_norm['days'] = (
            covid_norm['date'] - covid_norm['date'].min()
        ).dt.days
        covid_norm['outbreak'] = 'COVID-19'
        covid_norm = covid_norm.rename(columns={'total_cases': 'cases'})

        combined = pd.concat([
            ebola_norm[['days', 'cases', 'outbreak']],
            covid_norm[['days', 'cases', 'outbreak']]
        ])

        fig_norm = px.line(
            combined, x='days', y='cases', color='outbreak',
            color_discrete_map={
                'Ebola': '#e74c3c',
                'COVID-19': '#3498db'
            },
            labels={'days': 'Days Since Outbreak Start',
                    'cases': 'Cumulative Cases',
                    'outbreak': 'Emergency'}
        )
        fig_norm.update_layout(
            template='plotly_dark', height=400,
            hovermode='x unified',
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_norm, use_container_width=True)

    with col2:
        st.subheader("CFR comparison")
        cfr_df = pd.DataFrame({
            'Emergency': ['Ebola (2014–2016)', 'COVID-19 (2020–2024)'],
            'CFR (%)': [ebola_cfr, covid_cfr],
            'Color': ['#e74c3c', '#3498db']
        })

        fig_cfr_comp = px.bar(
            cfr_df, x='Emergency', y='CFR (%)',
            color='Emergency',
            color_discrete_map={
                'Ebola (2014–2016)': '#e74c3c',
                'COVID-19 (2020–2024)': '#3498db'
            },
            text='CFR (%)'
        )
        fig_cfr_comp.update_traces(
            texttemplate='%{text:.1f}%', textposition='outside'
        )
        fig_cfr_comp.update_layout(
            template='plotly_dark', height=400, showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_cfr_comp, use_container_width=True)


# ============================================================
# PAGE 8: SIERRA LEONE MAP
# ============================================================
elif page == "🗺️ Sierra Leone Map":
    st.title("Sierra Leone — Geographic Overview")
    st.markdown(
        "Sierra Leone is divided into 4 provinces and 16 districts. "
        "This map provides geographic context for the subnational health "
        "data explored throughout this dashboard."
    )

    # Country-level context metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Population", "~8.6 million")
    with col2:
        st.metric("Districts", "16")
    with col3:
        st.metric("Provinces", "4")
    with col4:
        st.metric("Capital", "Freetown")

    st.markdown("---")

    # Map layer selector
    map_layer = st.selectbox(
        "Select data layer to display on map",
        ["Malaria Prevalence (2016 DHS)",
         "Ebola Total Cases by District",
         "District Locations"]
    )

    if map_layer == "Malaria Prevalence (2016 DHS)":
        fig_sl_map = px.scatter_mapbox(
            malaria_map,
            lat='lat', lon='lon',
            size='malaria_prevalence_pct',
            color='malaria_prevalence_pct',
            hover_name='district',
            hover_data={'malaria_prevalence_pct': ':.1f%',
                        'lat': False, 'lon': False},
            color_continuous_scale='Reds',
            size_max=40,
            zoom=6.5,
            center={'lat': 8.4606, 'lon': -11.7799},
            title='Malaria Prevalence by District — Sierra Leone (2016)',
            labels={'malaria_prevalence_pct': 'Prevalence (%)'}
        )

    elif map_layer == "Ebola Total Cases by District":
        dist_total = ebola_dist.groupby('district')['cases'].sum().reset_index()
        dist_total = dist_total.merge(
            malaria_map[['district', 'lat', 'lon']],
            on='district', how='left'
        )
        dist_total = dist_total.dropna(subset=['lat', 'lon'])

        fig_sl_map = px.scatter_mapbox(
            dist_total,
            lat='lat', lon='lon',
            size='cases',
            color='cases',
            hover_name='district',
            hover_data={'cases': ':,.0f', 'lat': False, 'lon': False},
            color_continuous_scale='Reds',
            size_max=40,
            zoom=6.5,
            center={'lat': 8.4606, 'lon': -11.7799},
            title='Total Ebola Cases by District — Sierra Leone',
            labels={'cases': 'Total Cases'}
        )

    else:
        fig_sl_map = px.scatter_mapbox(
            malaria_map,
            lat='lat', lon='lon',
            hover_name='district',
            zoom=6.5,
            center={'lat': 8.4606, 'lon': -11.7799},
            title='Sierra Leone — District Locations'
        )
        fig_sl_map.update_traces(marker=dict(size=12, color='#e74c3c'))

    fig_sl_map.update_layout(
        mapbox_style='open-street-map',
        height=580,
        margin=dict(r=0, t=30, l=0, b=0),
        paper_bgcolor='rgba(0,0,0,0)'
    )
    st.plotly_chart(fig_sl_map, use_container_width=True)

    st.markdown("---")
    st.subheader("District reference data")

    display_df = malaria_map.rename(columns={
        'district': 'District',
        'lat': 'Latitude',
        'lon': 'Longitude',
        'malaria_prevalence_pct': 'Malaria Prevalence (%)'
    }).sort_values('Malaria Prevalence (%)', ascending=False)

    st.dataframe(display_df, use_container_width=True)
    st.caption(
        "Coordinates represent district centroids. "
        "Malaria prevalence from 2016 DHS survey (most recent available at district level)."
    )
