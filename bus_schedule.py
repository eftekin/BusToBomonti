from datetime import datetime

import pytz
import requests
import streamlit as st
from bs4 import BeautifulSoup

# Translations for different languages
TRANSLATIONS = {
    "en": {
        "title": "Bus Schedule: Alibeyköy → Bomonti",
        "current_time": "Current time",
        "select_line": "Select your bus line:",
        "all_lines": "Show all lines",
        "minutes_until": "minutes until departure",
        "crowded": "Might be crowded 🫂",
        "moderate": "Moderate crowd 😊",
        "empty": "Plenty of seats available 👍",
        "no_bus": "No more buses today 😔",
        "check_tomorrow": "Check back tomorrow! 🚌",
        "days": {
            "monday": "Monday",
            "tuesday": "Tuesday",
            "wednesday": "Wednesday",
            "thursday": "Thursday",
            "friday": "Friday",
            "saturday": "Saturday",
            "sunday": "Sunday",
        },
    },
    "tr": {
        "title": "Otobüs Saatleri: Alibeyköy → Bomonti",
        "current_time": "Şu anki saat",
        "select_line": "Otobüs hattınızı seçin:",
        "all_lines": "Tüm hatları göster",
        "minutes_until": "dakika sonra kalkacak",
        "crowded": "Kalabalık olabilir 🫂",
        "moderate": "Orta yoğunluk 😊",
        "empty": "Bolca boş koltuk var 👍",
        "no_bus": "Bugün başka otobüs yok 😔",
        "check_tomorrow": "Yarın tekrar kontrol edin! 🚌",
        "days": {
            "monday": "Pazartesi",
            "tuesday": "Salı",
            "wednesday": "Çarşamba",
            "thursday": "Perşembe",
            "friday": "Cuma",
            "saturday": "Cumartesi",
            "sunday": "Pazar",
        },
    },
}


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


def estimate_crowd(time_str):
    """Estimate crowd density based on time."""
    hour = int(time_str.split(":")[0])
    if hour in [7, 8, 9, 17, 18, 19]:  # Peak hours
        return "crowded", "#f87171"  # Daha canlı kırmızı
    elif hour in [10, 11, 12, 13, 14, 15, 16]:  # Moderate hours
        return "moderate", "#fbbf24"  # Daha canlı turuncu
    return "empty", "#34d399"  # Daha canlı yeşil


def set_custom_style():
    st.markdown(
        """
        <style>
        .bus-card {
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            border-radius: 12px;
            padding: 24px;
            margin: 20px 0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
            transition: all 0.2s ease;
            border: 1px solid #e5e7eb;
        }
        .bus-card:hover {
            transform: translateY(-2px);
            background: linear-gradient(135deg, #ffffff 0%, #f1f5f9 100%);
            box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
        }
        .bus-time {
            font-size: 32px;
            font-weight: 700;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            color: #1e40af;
        }
        .bus-time span {
            background: linear-gradient(135deg, #1e40af 0%, #3b82f6 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .bus-label {
            font-size: 18px;
            color: #3b82f6;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #dbeafe 0%, #eff6ff 100%);
            padding: 6px 14px;
            border-radius: 20px;
            display: inline-block;
            margin: 8px 0;
            font-weight: 500;
            border: 1px solid #bfdbfe;
        }
        .next-bus {
            background: linear-gradient(135deg, #fafafa 0%, #f8fafc 100%);
            border: 2px solid #bfdbfe;
            transition: all 0.2s ease;
        }
        .next-bus:hover {
            border: 2px solid #3b82f6;
        }
        .header-container {
            background: linear-gradient(135deg, #2563eb 0%, #1d4ed8 100%);
            padding: 24px;
            margin-bottom: 40px;
            text-align: center;
            border-radius: 16px;
            box-shadow: 0 10px 15px -3px rgba(59, 130, 246, 0.3);
        }
        .header-container h1 {
            color: white;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-weight: 700;
            font-size: 2em;
            margin-bottom: 8px;  /* Reduced from 16px to 8px */
        }
        .header-container p {
            color: white;
            font-size: 1.2em;    /* Increased from 1em to 1.2em */
            margin: 0;           /* Remove default margins */
        }
        .no-bus-message {
            text-align: center;
            padding: 48px;
            background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
            color: #1f2937;
            border-radius: 12px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border: 1px solid #e5e7eb;
        }
        .crowd-indicator {
            display: inline-block;
            padding: 6px 12px;
            border-radius: 20px;
            font-weight: 500;
            margin-top: 12px;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            font-size: 14px;
            background: linear-gradient(135deg, rgba(255,255,255,0.8) 0%, rgba(255,255,255,0.4) 100%);
            backdrop-filter: blur(4px);
        }
        /* Mobile optimization */
        @media (max-width: 768px) {
            .bus-card {
                padding: 12px;
                margin: 8px 0;
            }
            .bus-time {
                font-size: 20px;
            }
            .bus-label {
                font-size: 12px;
                padding: 3px 8px;
            }
            .header-container {
                padding: 16px;
                margin-bottom: 16px;
                border-radius: 8px;
            }
            .header-container h1 {
                font-size: 1.2em;
            }
            .header-container p {
                font-size: 1em;
                padding: 4px 8px;
            }
            .crowd-indicator {
                font-size: 12px;
                padding: 4px 8px;
                margin-top: 8px;
            }
            .no-bus-message {
                padding: 24px;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def format_time_difference(minutes, lang):
    """
    Format time difference in hours and minutes when over 60 minutes.

    Args:
        minutes (int): Time difference in minutes
        lang (str): Language code ('en' or 'tr')

    Returns:
        str: Formatted time string
    """
    if minutes < 60:
        return f"{minutes}"

    hours = minutes // 60
    remaining_minutes = minutes % 60

    if lang == "tr":
        if remaining_minutes == 0:
            return f"{hours} saat"
        return f"{hours} saat {remaining_minutes} dakika"
    else:
        if remaining_minutes == 0:
            return f"{hours} hour{'s' if hours > 1 else ''}"
        return f"{hours} hour{'s' if hours > 1 else ''} {remaining_minutes} minutes"


def main():
    """
    Main function to run the Streamlit app.
    """
    st.set_page_config(page_title="Bus Schedule: Alibeyköy → Bomonti", page_icon="🚌")

    set_custom_style()

    # Language selection
    lang = st.sidebar.selectbox(
        "Language/Dil",
        ["en", "tr"],
        format_func=lambda x: "English" if x == "en" else "Türkçe",
    )
    t = TRANSLATIONS[lang]

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

    # Line filtering
    selected_line = st.sidebar.selectbox(
        t["select_line"],
        ["all", "50L", "50T"],
        format_func=lambda x: t["all_lines"] if x == "all" else x,
    )

    # Parse bus schedule data
    schedules = parse_url(urls)

    # Get current time and day automatically from system's local time
    current_time, current_day = get_current_time()

    # Filtering logic
    if selected_line != "all":
        for schedule_type in schedules:
            schedules[schedule_type] = [
                (time, label)
                for time, label in schedules[schedule_type]
                if label == selected_line
            ]

    # Display page title
    current_day_translated = t["days"][current_day]
    page_title = t["title"].format(current_day_translated)
    st.markdown(
        f"""
        <div class="header-container">
            <h1>{page_title}</h1>
            <p>{t["current_time"]}: {current_time}</p>
        </div>
        """,
        unsafe_allow_html=True,
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

    # Show loading spinner while fetching data
    with st.spinner("Fetching bus schedules..."):
        # Display schedule
        bus_found = False
        first_bus = True
        for time, label in sorted(selected_schedule):
            current_time_minutes = convert_to_minutes(current_time)
            bus_time_minutes = convert_to_minutes(time)

            if current_time_minutes is not None and bus_time_minutes is not None:
                if current_time_minutes <= bus_time_minutes:
                    time_diff = bus_time_minutes - current_time_minutes
                    crowd_status, crowd_color = estimate_crowd(time)
                    card_class = "bus-card next-bus" if first_bus else "bus-card"

                    formatted_time = format_time_difference(time_diff, lang)
                    time_text = f"{formatted_time} " + (
                        t["minutes_until"]
                        if time_diff < 60
                        else ("kaldı" if lang == "tr" else "until departure")
                    )

                    st.markdown(
                        f"""
                        <div class="{card_class}">
                            <div class="bus-time">🚌 <span>{time}</span></div>
                            <div class="bus-label">{"Line" if lang == "en" else "Hat"} {label}</div>
                            <div style="color: #666; margin-top: 5px;">
                                {time_text}
                            </div>
                            <div class="crowd-indicator" style="background-color: {crowd_color}20; color: {crowd_color}">
                                {t[crowd_status]}
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )
                    bus_found = True
                    first_bus = False

        # Display message if no buses are available
        if not bus_found:
            st.markdown(
                f"""
                <div class="no-bus-message">
                    <h3>🚫 {t["no_bus"]}</h3>
                    <p>{t["check_tomorrow"]}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )


if __name__ == "__main__":
    main()
