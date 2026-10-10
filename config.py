# RTD Commute Tracker
# Stop IDs from RTD's stops.txt file

STOPS = {
    "morning": {
        "bus_board": "11960",
        "bus_exit": "26258",
        "train_board": "23060",
        "train_exit": "25973"
    },
    "afternoon": {
        "train_board": "34005",
        "train_exit": "23042",
        "bus_board": "26257",
        "bus_exit": "11961"
    }
}

TRANSFER_RULES = {
    "comfortable": 5,
    "tight": 3
}
