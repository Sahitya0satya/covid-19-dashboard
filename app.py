import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


st.set_page_config(
    page_title="COVID-19 Analytics",
    page_icon="🦠",
    layout="wide"
)


st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

.block-container {
    padding-top: 2rem;
}

.main-title {
    font-size: 42px;
    font-weight: 700;
    color: #172554;
}

.subtitle {
    color: #64748b;
    font-size: 17px;
    margin-bottom: 30px;
}

.card {
    background: white;
    padding: 22px;
    border-radius: 15px;
    box-shadow: 0px 3px 12px rgba(0,0,0,0.08);
}

.card-title {
    color: #64748b;
    font-size: 14px;
}

.card-number {
    color: #172554;
    font-size: 28px;
    font-weight: bold;
}

.section {
    color: #172554;
    font-size: 25px;
    font-weight: 600;
    margin-top: 30px;
}

</style>
""", unsafe_allow_html=True)



daily = pd.read_csv("day_wise.csv")

country = pd.read_csv("country_wise_latest.csv")

clean = pd.read_csv("covid_19_clean_complete.csv")

grouped = pd.read_csv("full_grouped.csv")



st.sidebar.title("🦠 COVID-19")

st.sidebar.markdown("### Dashboard")

page = st.sidebar.radio(
    "Navigate",
    [
        "Overview",
        "Daily Trends",
        "Country Analysis",
        "Data Explorer"
    ]
)



if page == "Overview":

    st.markdown(
        '<div class="main-title">COVID-19 Analytics Dashboard</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="subtitle">'
        'Global COVID-19 data analysis and visualization'
        '</div>',
        unsafe_allow_html=True
    )

    latest = daily.iloc[-1]

    confirmed = int(latest["Confirmed"])
    deaths = int(latest["Deaths"])
    recovered = int(latest["Recovered"])
    active = int(latest["Active"])



    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            f"""
            <div class="card">
            <div class="card-title">Confirmed Cases</div>
            <div class="card-number">{confirmed:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"""
            <div class="card">
            <div class="card-title">Deaths</div>
            <div class="card-number">{deaths:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"""
            <div class="card">
            <div class="card-title">Recovered</div>
            <div class="card-number">{recovered:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            f"""
            <div class="card">
            <div class="card-title">Active Cases</div>
            <div class="card-number">{active:,}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


    st.markdown(
        '<div class="section">📈 Global COVID-19 Trend</div>',
        unsafe_allow_html=True
    )

    daily["Date"] = pd.to_datetime(daily["Date"])

    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(
        daily["Date"],
        daily["Confirmed"],
        label="Confirmed"
    )

    ax.plot(
        daily["Date"],
        daily["Deaths"],
        label="Deaths"
    )

    ax.plot(
        daily["Date"],
        daily["Recovered"],
        label="Recovered"
    )

    ax.legend()

    ax.set_xlabel("Date")
    ax.set_ylabel("Cases")

    ax.grid(alpha=0.2)

    plt.xticks(rotation=45)

    st.pyplot(fig)

    

    st.markdown(
        '<div class="section">🌍 Top Countries by Confirmed Cases</div>',
        unsafe_allow_html=True
    )

    top = country.sort_values(
        "Confirmed",
        ascending=False
    ).head(10)

    fig2, ax2 = plt.subplots(figsize=(12,5))

    ax2.bar(
        top["Country/Region"],
        top["Confirmed"]
    )

    ax2.set_xlabel("Country")

    ax2.set_ylabel("Confirmed Cases")

    plt.xticks(rotation=45)

    st.pyplot(fig2)



elif page == "Daily Trends":

    st.markdown(
        '<div class="main-title">📈 Daily COVID-19 Trends</div>',
        unsafe_allow_html=True
    )

    daily["Date"] = pd.to_datetime(daily["Date"])

    

    st.subheader("Confirmed Cases")

    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(
        daily["Date"],
        daily["Confirmed"]
    )

    ax.set_xlabel("Date")
    ax.set_ylabel("Confirmed Cases")

    ax.grid(alpha=0.2)

    st.pyplot(fig)

    # Deaths

    st.subheader("Deaths")

    fig2, ax2 = plt.subplots(figsize=(12,5))

    ax2.plot(
        daily["Date"],
        daily["Deaths"]
    )

    ax2.set_xlabel("Date")
    ax2.set_ylabel("Deaths")

    ax2.grid(alpha=0.2)

    st.pyplot(fig2)

    

    st.subheader("Recovered")

    fig3, ax3 = plt.subplots(figsize=(12,5))

    ax3.plot(
        daily["Date"],
        daily["Recovered"]
    )

    ax3.set_xlabel("Date")
    ax3.set_ylabel("Recovered")

    ax3.grid(alpha=0.2)

    st.pyplot(fig3)



elif page == "Country Analysis":

    st.markdown(
        '<div class="main-title">🌍 Country Analysis</div>',
        unsafe_allow_html=True
    )

    countries = sorted(
        clean["Country/Region"].dropna().unique()
    )

    selected = st.selectbox(
        "Select a country",
        countries
    )

    country_data = clean[
        clean["Country/Region"] == selected
    ].copy()

    country_data["Date"] = pd.to_datetime(
        country_data["Date"]
    )

    country_data = country_data.groupby(
        "Date",
        as_index=False
    )[
        ["Confirmed", "Deaths", "Recovered", "Active"]
    ].sum()

    latest_country = country_data.iloc[-1]

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Confirmed",
        f"{int(latest_country['Confirmed']):,}"
    )

    c2.metric(
        "Deaths",
        f"{int(latest_country['Deaths']):,}"
    )

    c3.metric(
        "Recovered",
        f"{int(latest_country['Recovered']):,}"
    )

    c4.metric(
        "Active",
        f"{int(latest_country['Active']):,}"
    )

    

    st.subheader(
        f"COVID-19 Trend — {selected}"
    )

    fig, ax = plt.subplots(figsize=(12,5))

    ax.plot(
        country_data["Date"],
        country_data["Confirmed"],
        label="Confirmed"
    )

    ax.plot(
        country_data["Date"],
        country_data["Deaths"],
        label="Deaths"
    )

    ax.plot(
        country_data["Date"],
        country_data["Recovered"],
        label="Recovered"
    )

    ax.legend()

    ax.set_xlabel("Date")
    ax.set_ylabel("Cases")

    ax.grid(alpha=0.2)

    plt.xticks(rotation=45)

    st.pyplot(fig)




elif page == "Data Explorer":

    st.markdown(
        '<div class="main-title">📋 Data Explorer</div>',
        unsafe_allow_html=True
    )

    dataset = st.selectbox(
        "Choose Dataset",
        [
            "Daily Data",
            "Country Data",
            "Clean Complete Data",
            "Grouped Data"
        ]
    )

    if dataset == "Daily Data":
        st.dataframe(
            daily,
            use_container_width=True
        )

    elif dataset == "Country Data":
        st.dataframe(
            country,
            use_container_width=True
        )

    elif dataset == "Clean Complete Data":
        st.dataframe(
            clean,
            use_container_width=True
        )

    elif dataset == "Grouped Data":
        st.dataframe(
            grouped,
            use_container_width=True
        )

st.markdown("---")

st.markdown(
    """
    <center>
    <p style="color:#64748b;">
    COVID-19 Analytics Dashboard | Data Analysis Project
    </p>
    </center>
    """,
    unsafe_allow_html=True
)
