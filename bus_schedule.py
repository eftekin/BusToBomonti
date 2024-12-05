from datetime import datetime

import pytz
import requests
import streamlit as st
from bs4 import BeautifulSoup


def parse_url(url_list):
    """
    Parses the URLs to extract bus schedule data for weekdays, Saturday, and Sunday.

    Args:
        url_list (list): List of tuples containing URL and corresponding bus label.

    Returns:
        dict: Dictionary of schedules with separate keys for weekdays, Saturday, and Sunday.
    """
    schedules = {"weekdays": [], "saturday": [], "sunday": []}

    for url, label in url_list:
        try:
            data = requests.get(url).text
            soup = BeautifulSoup(data, "html.parser")
            table = soup.find("table", class_="line-table")

            if table and table.tbody:
                # Extracting all rows from the table
                rows = table.find_all("tr")

                # Loop through each row and extract the relevant times
                for row in rows:
                    columns = row.find_all("td")
                    if len(columns) == 3:  # Ensure the row has 3 columns for each day
                        weekday_time = columns[0].text.strip()
                        saturday_time = columns[1].text.strip()
                        sunday_time = columns[2].text.strip()

                        if weekday_time:
                            schedules["weekdays"].append((weekday_time, label))
                        if saturday_time:
                            schedules["saturday"].append((saturday_time, label))
                        if sunday_time:
                            schedules["sunday"].append((sunday_time, label))

        except Exception as e:
            st.error(f"Error parsing URL {url}: {e}")

    return schedules


def convert_to_minutes(time_str):
    """
    Converts a time string in HH:MM format to minutes.

    Args:
        time_str (str): Time string in HH:MM format.

    Returns:
        int: Total minutes.
    """
    try:
        hours, minutes = map(int, time_str.split(":"))
        return hours * 60 + minutes
    except ValueError:
        return None


def get_current_time():
    """
    Gets the current time and day in Turkey's timezone (Istanbul).

    Returns:
        tuple: Current time in HH:MM format and the current day name.
    """
    turkey_timezone = pytz.timezone("Europe/Istanbul")
    utc_now = datetime.utcnow()
    turkey_now = utc_now.replace(tzinfo=pytz.utc).astimezone(tz=turkey_timezone)
    current_time = turkey_now.strftime("%H:%M")
    current_day = turkey_now.strftime("%A").lower()  # Lowercased day for comparison
    return current_time, current_day


def main():
    """
    Main function to run the Streamlit app.
    """
    # URLs and labels for bus schedules
    urls = [
        (
            "https://otobussaatleri.net/50l-alibeykoy-metro-besiktas-otobus-saatleri/",
            "50L",
        ),
        (
            "https://otobussaatleri.net/50t-alibeykoy-metro-taksim-otobus-saatleri/",
            "50T",
        ),
    ]

    # Parse bus schedule data
    schedules = parse_url(urls)

    # Get current time and day automatically from system's local time
    current_time, current_day = get_current_time()

    # Display page title
    page_title = f"Bus Schedule for {current_day.capitalize()}: Alibeyköy to Bomonti"
    st.markdown(
        f"<h1 style='text-align:center;'>{page_title}</h1>", unsafe_allow_html=True
    )

    # Determine which schedule to show
    if current_day in ["monday", "tuesday", "wednesday", "thursday", "friday"]:
        selected_schedule = schedules["weekdays"]
    elif current_day == "saturday":
        selected_schedule = schedules["saturday"]
    elif current_day == "sunday":
        selected_schedule = schedules["sunday"]
    else:
        selected_schedule = []

    # Display schedule
    bus_found = False
    for time, label in sorted(selected_schedule):
        current_time_minutes = convert_to_minutes(current_time)
        bus_time_minutes = convert_to_minutes(time)

        if current_time_minutes is not None and bus_time_minutes is not None:
            if current_time_minutes <= bus_time_minutes:
                st.markdown(
                    f"<h3 style='text-align:center; font-size:24px;'>{time} <span style='color:slategray; font-style:italic;'> &ensp; ({label})</span></h3>",
                    unsafe_allow_html=True,
                )
                bus_found = True

    # Display message if no buses are available
    if not bus_found:
        st.markdown(
            "<h3 style='text-align:center;'>No bus available right now.</h3>",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
