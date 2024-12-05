from datetime import datetime

import pandas as pd
import pytz
import requests
import streamlit as st
from bs4 import BeautifulSoup


def parse_url(url_list):
    """
    Parses the URLs to extract bus schedule data.

    Args:
        url_list (list): List of tuples containing URL and corresponding bus label.

    Returns:
        dict: Dictionary of bus times and labels.
    """
    weekdays_list = {}

    for url, label in url_list:
        try:
            data = requests.get(url).text
            soup = BeautifulSoup(data, "html.parser")
            table = soup.find("table", class_="line-table")

            if table and table.tbody:
                for row in table.tbody.find_all("tr"):
                    columns = row.find_all("td")
                    if columns and len(columns) > 0:
                        time_str = columns[0].text.strip()
                        if ":" in time_str:
                            weekdays_list[time_str] = label
        except Exception as e:
            st.error(f"Error parsing URL {url}: {e}")
    return weekdays_list


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
    Gets the current time in Turkey's timezone.

    Returns:
        str: Current time in HH:MM format.
    """
    turkey_timezone = pytz.timezone("Europe/Istanbul")
    utc_now = datetime.utcnow()
    turkey_now = utc_now.replace(tzinfo=pytz.utc).astimezone(tz=turkey_timezone)
    return turkey_now.strftime("%H:%M")


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
    weekdays_hour_list = parse_url(urls)

    # Sort bus schedule data
    weekdays_hour_list_sorted = dict(sorted(weekdays_hour_list.items()))

    # Get current time
    current_time = get_current_time()

    # Display page title
    page_title = "Weekday Bus Schedule: Alibeyköy to Bomonti"
    st.markdown(
        f"<h1 style='text-align:center;'>{page_title}</h1>", unsafe_allow_html=True
    )

    # Display bus schedule
    bus_found = False
    for time, label in weekdays_hour_list_sorted.items():
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
        no_bus_message = "No bus available right now."
        st.markdown(
            f"<h3 style='text-align:center;'>{no_bus_message}</h3>",
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
