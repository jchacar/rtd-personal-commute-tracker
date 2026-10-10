
import csv
from datetime import datetime
from pathlib import Path


def load_csv(filename):
    path = Path(__file__).parent / "data" / filename

    with open(path, newline="", encoding="utf-8-sig") as file:
        return list(csv.DictReader(file))


def get_active_services(target_date):
    calendar = load_csv("calendar.txt")
    exceptions = load_csv("calendar_dates.txt")

    date_string = target_date.strftime("%Y%m%d")
    weekday = target_date.strftime("%A").lower()

    active = set()

    # Identify regularly scheduled services
    for service in calendar:
        within_dates = (
            service["start_date"] <= date_string
            <= service["end_date"]
        )

        runs_today = service[weekday] == "1"

        if within_dates and runs_today:
            active.add(service["service_id"])

    # Apply special schedule exceptions
    for exception in exceptions:
        if exception["date"] == date_string:
            service_id = exception["service_id"]

            if exception["exception_type"] == "1":
                active.add(service_id)

            elif exception["exception_type"] == "2":
                active.discard(service_id)

    return sorted(active)


def get_route_trips(route_id, target_date):
    active_services = get_active_services(target_date)
    trips = load_csv("trips.txt")

    matching_trips = []

    for trip in trips:
        if (
            trip["route_id"] == route_id
            and trip["service_id"] in active_services
        ):
            matching_trips.append(trip)

    return matching_trips
