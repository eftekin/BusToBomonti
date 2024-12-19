# BusToBomonti 🚍

## About 📍

Ever found yourself juggling between two different bus schedules, trying to catch the right one home from school every day? That was me until I decided to simplify my routine. This project emerged from my daily struggle of checking two different websites for bus schedules from **Alibeyköy** to **Bomonti**.

## Features 🌟

- Scrapes bus schedule data from two different websites.
- Combines and sorts the schedules for easy viewing.
- Displays the upcoming bus schedule based on the current time using **Streamlit**.
- User-friendly interface to help you plan your commute efficiently.
- Estimates crowd density based on the time of day.

## Prerequisites ⚙️

To get started with the project, you'll need the following dependencies:

- **Streamlit** – For running the app.
- **Requests** – For fetching data from the websites.
- **BeautifulSoup** – For parsing the HTML data.
- **Pytz** – For handling time zones.
- **Altair** – For data visualization (if needed).

Ensure these dependencies are installed before running the project.

## How to Run 🏃‍♂️

1. Clone the repository:

   ```bash
   git clone https://github.com/eftekin/BusToBomonti.git
   ```

2. Navigate to the project directory:

   ```bash
   cd BusToBomonti
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Run the app:

   ```bash
   streamlit run bus_schedule.py
   ```

## Screenshots 📸

Here’s a sneak peek at the app interface:

<img src="https://github.com/user-attachments/assets/5e0a12ff-c7b3-4490-a022-8e3ccde09369" alt="Bus Schedule Screenshot" width="600">

## Contributions 🤝

Contributions are welcome! Whether it’s fixing bugs, improving features, or adding new functionalities, feel free to open an issue or submit a pull request. Let’s work together to improve the tool! 🚀

## License 📄

This project is licensed under the [MIT License](LICENSE). Feel free to use, modify, and distribute it in accordance with the terms of the license.
