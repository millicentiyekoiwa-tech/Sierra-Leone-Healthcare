"""
SIERRA LEONE HEALTH EMERGENCIES DASHBOARD - VERSION 3 (SINGLE PAGE)
=======================================================
MSBA382 - Healthcare Analytics Individual Project
A comprehensive analysis of health emergencies, disease burden,
and health system access in Sierra Leone (2014-2024).
 

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
    initial_sidebar_state="collapsed"
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
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #1e2130;
        border-radius: 6px 6px 0 0;
        padding: 10px 20px;
        font-weight: 600;
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
 
# Precompute shared Ebola/COVID summary stats (used across tabs)
ebola_cases  = int(ebola_sl['Total cases'].max())
ebola_deaths = int(ebola_sl['Total deaths'].max())
ebola_cfr    = ebola_sl['CFR_percent'].iloc[-1]
ebola_days   = (ebola_sl['report_date'].max() - ebola_sl['report_date'].min()).days
 
covid_cases  = int(covid_sl['total_cases'].max())
covid_deaths = int(covid_sl['total_deaths'].max())
covid_cfr    = covid_deaths / covid_cases * 100
covid_days   = (covid_sl['date'].max() - covid_sl['date'].min()).days
 
# ============================================================
# HEADER (shared across the whole single page)
# ============================================================
st.title("Sierra Leone Health Emergencies Dashboard")
st.markdown("### A decade of crisis and resilience (2014–2024)")
st.markdown(
    "This dashboard provides a comprehensive analytical view of Sierra Leone's "
    "major health emergencies over the past decade — the 2014–2016 Ebola epidemic, "
    "the 2020–2024 COVID-19 pandemic — alongside the country's everyday infectious "
    "disease burden, malaria patterns, WASH-related mortality, and health system "
    "access indicators."
)
 
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 10px 0;'>
        <h2 style='color:#e74c3c;'>🇸🇱 Sierra Leone</h2>
        <p style='color:#a0a0a0; font-size:0.8rem;'>Health Emergencies Dashboard</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
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
 
st.markdown("---")
 
# ============================================================
# SINGLE-PAGE TAB NAVIGATION (no page reload, one URL)
# ============================================================
tab1, tab2, tab3 = st.tabs([
    "🏠 Overview & Disease Burden",
    "🦠 Outbreaks: Ebola vs COVID-19",
    "🦟 Malaria, Access & Map"
])
 
# ============================================================
# TAB 1: OVERVIEW & DISEASE BURDEN (incl. WASH)
# ============================================================
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("🔴 Ebola Total Cases", f"{ebola_cases:,}")
        st.metric("Ebola Total Deaths", f"{ebola_deaths:,}",
                   delta=f"{ebola_cfr:.1f}% CFR", delta_color="off")
    with col2:
        st.metric("🔵 COVID-19 Total Cases", f"{covid_cases:,}")
        st.metric("COVID-19 Total Deaths", f"{covid_deaths:,}",
                   delta=f"{covid_cfr:.1f}% CFR", delta_color="off")
    with col3:
        st.metric("🦟 Top Cause of Death", "Malaria",
                   delta="101.1 per 100k (2021)", delta_color="off")
        st.metric("WASH Death Rate", "69.5 per 100k",
                   delta="Males 78.9 vs Females 60.2", delta_color="off")
    with col4:
        st.metric("🏥 Facility Births", "~87%",
                   delta="Up from 54% in 2008", delta_color="normal")
        st.metric("Malaria Prevalence", "Up to 78%",
                   delta="Koinadugu district (2016)", delta_color="off")
 
    st.markdown("---")
 
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
            template='plotly_dark', height=420,
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
            template='plotly_dark', height=260, margin=dict(t=10, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_cat, use_container_width=True)
 
        st.markdown("""
        <div class='insight-box'>
        <b>Infectious disease dominates Sierra Leone's burden</b><br><br>
        54.4% of the top-15 causes of death are infectious diseases — more
        than double the NCD share (25.1%). Malaria alone kills at 101 per
        100,000 population annually.
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
            template='plotly_dark', height=350, showlegend=False,
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
    <b>Geographic inequality:</b> Malaria prevalence ranges from 78% in
    Koinadugu to just 3.8% in Western Urban — a 20x gap driven by access
    and infrastructure. See the Malaria tab for the full district map.
    </div>
    """, unsafe_allow_html=True)
 
 
# ============================================================
# TAB 2: OUTBREAKS - EBOLA VS COVID-19 (incl. comparison)
# ============================================================
with tab2:
    sub_ebola, sub_covid, sub_compare = st.tabs(
        ["Ebola (2014–2016)", "COVID-19 (2020–2024)", "Side-by-Side Comparison"]
    )
 
    # ---------------- Ebola ----------------
    with sub_ebola:
        st.markdown(
            "Sierra Leone was the most affected country in the largest Ebola "
            "outbreak in history, recording more cases than any other nation "
            "in the epidemic."
        )
 
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Cases", f"{ebola_cases:,}")
        with c2:
            st.metric("Total Deaths", f"{ebola_deaths:,}")
        with c3:
            st.metric("Final CFR", f"{ebola_cfr:.1f}%")
        with c4:
            st.metric("Outbreak Duration", f"{ebola_days} days")
 
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
            hovermode='x unified', template='plotly_dark', height=380,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
            legend=dict(bgcolor='rgba(0,0,0,0)')
        )
        st.plotly_chart(fig_ebola, use_container_width=True)
        st.caption(
            "Note: Two minor downward revisions in WHO's reporting (Nov 2014, "
            "Aug 2015) reflect case reclassification and were smoothed using "
            "cumulative maximum methodology. Raw values are preserved in the "
            "underlying dataset."
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
                template='plotly_dark', height=340,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_cfr, use_container_width=True)
 
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
                template='plotly_dark', height=340, showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_sub, use_container_width=True)
 
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
            template='plotly_dark', height=420,
            coloraxis_showscale=False,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_dist_bar, use_container_width=True)
 
    # ---------------- COVID-19 ----------------
    with sub_covid:
        st.markdown(
            "Sierra Leone experienced four distinct waves of COVID-19 "
            "infection. Despite limited testing capacity, the health system "
            "maintained a relatively low official CFR compared to Ebola."
        )
 
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Total Cases", f"{covid_cases:,}")
        with c2:
            st.metric("Total Deaths", f"{covid_deaths:,}")
        with c3:
            st.metric("Overall CFR", f"{covid_cfr:.1f}%")
        with c4:
            vax_max = covid_sl['people_fully_vaccinated_per_hundred'].max()
            st.metric("Peak Vaccination", f"{vax_max:.1f}%")
 
        st.subheader("Daily new cases — four pandemic waves")
        fig_waves = px.area(
            covid_sl, x='date', y='new_cases_smoothed',
            labels={'date': 'Date', 'new_cases_smoothed': 'New Cases (7-day avg)'}
        )
        fig_waves.update_traces(
            line=dict(color='#3498db', width=2),
            fillcolor='rgba(52,152,219,0.3)'
        )
        fig_waves.update_layout(
            template='plotly_dark', height=350,
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_waves, use_container_width=True)
 
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Cumulative cases & deaths")
            fig_cum = go.Figure()
            fig_cum.add_trace(go.Scatter(
                x=covid_sl['date'], y=covid_sl['total_cases'],
                name='Total Cases', line=dict(color='#3498db', width=3),
                fill='tozeroy', fillcolor='rgba(52,152,219,0.1)'
            ))
            fig_cum.add_trace(go.Scatter(
                x=covid_sl['date'], y=covid_sl['total_deaths'],
                name='Total Deaths', line=dict(color='white', width=2, dash='dash'),
                yaxis='y2'
            ))
            fig_cum.update_layout(
                yaxis=dict(title='Total Cases'),
                yaxis2=dict(title='Total Deaths', overlaying='y', side='right'),
                hovermode='x unified', template='plotly_dark', height=350,
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
                template='plotly_dark', height=350,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_vax, use_container_width=True)
 
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
                labels={'region': 'Province', 'Cases': 'Total Cases'},
                color_discrete_map={'Female': '#e74c3c', 'Male': '#3498db'}
            )
            fig_gender.update_layout(
                template='plotly_dark', height=350,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(bgcolor='rgba(0,0,0,0)')
            )
            st.plotly_chart(fig_gender, use_container_width=True)
        with col2:
            total_female = covid_dist['cases_female'].sum()
            total_male   = covid_dist['cases_male'].sum()
            total_both   = total_female + total_male
            st.metric("Female cases", f"{total_female/total_both*100:.1f}%")
            st.metric("Male cases", f"{total_male/total_both*100:.1f}%")
 
    # ---------------- Comparison ----------------
    with sub_compare:
        st.markdown(
            "A side-by-side analytical comparison of Sierra Leone's two major "
            "health emergencies — Ebola (2014–2016) and COVID-19 (2020–2024)."
        )
 
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
        ({:,} vs {:,}), its CFR of {:.1f}% was <b>17x higher</b> than
        COVID-19's {:.1f}% CFR — reflecting Ebola's extreme severity even at
        lower case volumes. These two emergencies demanded fundamentally
        different public health responses.
        </div>
        """.format(ebola_cases, covid_cases, ebola_cfr, covid_cfr),
        unsafe_allow_html=True)
 
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
                color_discrete_map={'Ebola': '#e74c3c', 'COVID-19': '#3498db'},
                labels={'days': 'Days Since Outbreak Start',
                        'cases': 'Cumulative Cases', 'outbreak': 'Emergency'}
            )
            fig_norm.update_layout(
                template='plotly_dark', height=380,
                hovermode='x unified',
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                legend=dict(bgcolor='rgba(0,0,0,0)')
            )
            st.plotly_chart(fig_norm, use_container_width=True)
 
        with col2:
            st.subheader("CFR comparison")
            cfr_df = pd.DataFrame({
                'Emergency': ['Ebola (2014–2016)', 'COVID-19 (2020–2024)'],
                'CFR (%)': [ebola_cfr, covid_cfr]
            })
            fig_cfr_comp = px.bar(
                cfr_df, x='Emergency', y='CFR (%)', color='Emergency',
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
                template='plotly_dark', height=380, showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_cfr_comp, use_container_width=True)
 
 
# ============================================================
# TAB 3: MALARIA, HEALTH ACCESS & MAP
# ============================================================
with tab3:
    sub_malaria, sub_access, sub_map = st.tabs(
        ["Malaria", "Health System Access", "Sierra Leone Map"]
    )
 
    # ---------------- Malaria ----------------
    with sub_malaria:
        st.markdown(
            "Malaria kills more people in Sierra Leone than any other single "
            "cause, at 101 deaths per 100,000 population annually. But this "
            "burden is not evenly distributed."
        )
 
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Death rate", "101.1 per 100k", delta="#1 cause of death", delta_color="off")
        with c2:
            st.metric("Highest prevalence", "78.1% — Koinadugu", delta_color="off")
        with c3:
            st.metric("Lowest prevalence", "3.8% — Western Urban", delta_color="off")
 
        st.subheader("Malaria prevalence by district (2016 DHS Survey)")
        try:
            fig_map = px.scatter_map(
                malaria_map,
                lat='lat', lon='lon',
                size='malaria_prevalence_pct',
                color='malaria_prevalence_pct',
                hover_name='district',
                hover_data={'malaria_prevalence_pct': ':.1f', 'lat': False, 'lon': False},
                color_continuous_scale='Reds',
                size_max=35, zoom=6,
                center={'lat': 8.4606, 'lon': -11.7799},
                labels={'malaria_prevalence_pct': 'Prevalence (%)'}
            )
        except Exception:
            fig_map = px.scatter_mapbox(
                malaria_map,
                lat='lat', lon='lon',
                size='malaria_prevalence_pct',
                color='malaria_prevalence_pct',
                hover_name='district',
                color_continuous_scale='Reds',
                size_max=35, zoom=6,
                center={'lat': 8.4606, 'lon': -11.7799},
                labels={'malaria_prevalence_pct': 'Prevalence (%)'}
            )
        fig_map.update_layout(
            mapbox_style='open-street-map', height=440,
            margin=dict(r=0, t=20, l=0, b=0)
        )
        st.plotly_chart(fig_map, use_container_width=True)
 
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Prevalence by district (bar)")
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
                fig_rdt.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig_rdt.update_layout(
                    template='plotly_dark', height=420,
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
                fig_itn.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig_itn.update_layout(
                    template='plotly_dark', height=420,
                    coloraxis_showscale=False,
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_itn, use_container_width=True)
 
    # ---------------- Health Access ----------------
    with sub_access:
        st.markdown(
            "DHS survey data tracks key health access indicators across "
            "Sierra Leone's regions over multiple survey years, revealing "
            "trends in facility births, antenatal care coverage, and "
            "vaccination rates."
        )
 
        if not access.empty:
            indicators = access['Indicator'].unique().tolist()
            selected_ind = st.selectbox(
                "Select indicator to explore", indicators, index=0
            )
            access_filtered = access[access['Indicator'] == selected_ind].copy()
 
            col1, col2 = st.columns(2)
            with col1:
                fig_access_trend = px.line(
                    access_filtered.sort_values('SurveyYear'),
                    x='SurveyYear', y='Value', color='Location',
                    title=f'{selected_ind} — Trend Over Time',
                    labels={'SurveyYear': 'Survey Year', 'Value': '% of Population',
                            'Location': 'Region'},
                    markers=True
                )
                fig_access_trend.update_layout(
                    template='plotly_dark', height=400,
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                    legend=dict(bgcolor='rgba(0,0,0,0)')
                )
                st.plotly_chart(fig_access_trend, use_container_width=True)
 
            with col2:
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
                fig_access_bar.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                fig_access_bar.update_layout(
                    template='plotly_dark', height=400,
                    coloraxis_showscale=False,
                    paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_access_bar, use_container_width=True)
 
            with st.expander("View full data table"):
                st.dataframe(
                    access_filtered[['Location', 'SurveyYear', 'Indicator', 'Value']]
                    .sort_values(['Location', 'SurveyYear'])
                    .reset_index(drop=True),
                    use_container_width=True
                )
        else:
            st.warning("Access to health data not available.")
 
    # ---------------- Map ----------------
    with sub_map:
        st.markdown(
            "Sierra Leone is divided into 4 provinces and 16 districts. "
            "This map provides geographic context for the subnational health "
            "data explored throughout this dashboard."
        )
 
        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.metric("Population", "~8.6 million")
        with c2:
            st.metric("Districts", "16")
        with c3:
            st.metric("Provinces", "4")
        with c4:
            st.metric("Capital", "Freetown")
 
        map_layer = st.selectbox(
            "Select data layer to display on map",
            ["Malaria Prevalence (2016 DHS)",
             "Ebola Total Cases by District",
             "District Locations"]
        )
 
        if map_layer == "Malaria Prevalence (2016 DHS)":
            fig_sl_map = px.scatter_mapbox(
                malaria_map, lat='lat', lon='lon',
                size='malaria_prevalence_pct', color='malaria_prevalence_pct',
                hover_name='district',
                hover_data={'malaria_prevalence_pct': ':.1f%', 'lat': False, 'lon': False},
                color_continuous_scale='Reds', size_max=40, zoom=6.5,
                center={'lat': 8.4606, 'lon': -11.7799},
                title='Malaria Prevalence by District — Sierra Leone (2016)',
                labels={'malaria_prevalence_pct': 'Prevalence (%)'}
            )
        elif map_layer == "Ebola Total Cases by District":
            dist_total = ebola_dist.groupby('district')['cases'].sum().reset_index()
            dist_total = dist_total.merge(
                malaria_map[['district', 'lat', 'lon']], on='district', how='left'
            )
            dist_total = dist_total.dropna(subset=['lat', 'lon'])
            fig_sl_map = px.scatter_mapbox(
                dist_total, lat='lat', lon='lon',
                size='cases', color='cases',
                hover_name='district',
                hover_data={'cases': ':,.0f', 'lat': False, 'lon': False},
                color_continuous_scale='Reds', size_max=40, zoom=6.5,
                center={'lat': 8.4606, 'lon': -11.7799},
                title='Total Ebola Cases by District — Sierra Leone',
                labels={'cases': 'Total Cases'}
            )
        else:
            fig_sl_map = px.scatter_mapbox(
                malaria_map, lat='lat', lon='lon',
                hover_name='district', zoom=6.5,
                center={'lat': 8.4606, 'lon': -11.7799},
                title='Sierra Leone — District Locations'
            )
            fig_sl_map.update_traces(marker=dict(size=12, color='#e74c3c'))
 
        fig_sl_map.update_layout(
            mapbox_style='open-street-map', height=480,
            margin=dict(r=0, t=30, l=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)'
        )
        st.plotly_chart(fig_sl_map, use_container_width=True)
 
        with st.expander("View district reference data"):
            display_df = malaria_map.rename(columns={
                'district': 'District', 'lat': 'Latitude', 'lon': 'Longitude',
                'malaria_prevalence_pct': 'Malaria Prevalence (%)'
            }).sort_values('Malaria Prevalence (%)', ascending=False)
            st.dataframe(display_df, use_container_width=True)
            st.caption(
                "Coordinates represent district centroids. Malaria prevalence "
                "from 2016 DHS survey (most recent available at district level)."
            )
