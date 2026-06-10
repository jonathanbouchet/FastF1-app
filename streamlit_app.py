import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="F1 Data Visualization",
    page_icon="🏁",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_BASE_URL = "http://localhost:8000"


@st.cache_data
def get_races_for_year(year: int) -> list[str]:
    """Fetch race names for a given year."""
    try:
        response = requests.get(f"{API_BASE_URL}/years/{year}/races", timeout=10)
        if response.status_code == 200:
            return response.json()["races"]
        else:
            st.error(f"Error fetching races: {response.status_code}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return []


@st.cache_data
def get_race_schedule(year: int, race_name: str) -> dict:
    """Fetch race schedule for a given year and race name."""
    try:
        response = requests.get(
            f"{API_BASE_URL}/years/{year}/races/{race_name}/schedule", timeout=10
        )
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"Error fetching schedule: {response.status_code}")
            return {}
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to connect to API: {e}")
        return {}


# Sidebar for year selection
st.sidebar.header("⚙️ Filters")
year = st.sidebar.selectbox("Select Year", range(2025, 2017, -1), index=1)

# Navigation pages
page = st.sidebar.radio("Select Page", ["🏁 Race Names", "📅 Race Schedule"])

if page == "🏁 Race Names":
    st.title("🏁 F1 Race Names")
    st.markdown(f"### Season {year}")

    races = get_races_for_year(year)
    if races:
        col1, col2 = st.columns([2, 1])
        with col1:
            st.markdown("#### Available Races")
            for i, race in enumerate(races, 1):
                st.write(f"{i}. {race}")
        with col2:
            st.metric("Total Races", len(races))
    else:
        st.warning("No races found for this year.")

elif page == "📅 Race Schedule":
    st.title("📅 F1 Race Schedule")
    st.markdown(f"### Season {year}")

    races = get_races_for_year(year)
    if races:
        # Filter out non-main races like Pre-Season Testing
        main_races = [r for r in races if r not in ["Pre-Season Testing", "Winter Testing"]]
        if not main_races:
            main_races = races

        selected_race = st.sidebar.selectbox("Select Race", main_races)

        if selected_race:
            schedule_data = get_race_schedule(year, selected_race)
            if schedule_data and "sessions" in schedule_data:
                st.subheader(f"{selected_race}")

                sessions = schedule_data["sessions"]
                if sessions:
                    for session in sessions:
                        col1, col2 = st.columns([2, 2])
                        with col1:
                            st.write(f"**{session['name']}**")
                        with col2:
                            date_obj = datetime.fromisoformat(session["date_utc"])
                            st.write(
                                f"{date_obj.strftime('%Y-%m-%d %H:%M UTC')}"
                            )
                else:
                    st.info("No sessions found for this race.")
            else:
                st.warning("Failed to load schedule data.")
    else:
        st.warning("No races found for this year.")
