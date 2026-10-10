from fastapi import FastAPI, HTTPException
from datetime import datetime
from zoneinfo import ZoneInfo
import requests
from google.transit import gtfs_realtime_pb2

app = FastAPI()

RTD_URL = (
    "https://open-data.rtd-denver.com/"
    "files/gtfs-rt/rtd/TripUpdate.pb"
)

@app.get("/")
def home():
    return {
        "project": "RTD Commute Tracker",
        "status": "running",
        "current_time": datetime.now(
            ZoneInfo("America/Denver")
        ).isoformat()
    }

@app.get("/inspect")
def inspect_feed():
    try:
        response = requests.get(
            RTD_URL,
            timeout=20
        )
        response.raise_for_status()

        feed = gtfs_realtime_pb2.FeedMessage()
        feed.ParseFromString(response.content)

        trips = [
            entity.trip_update
            for entity in feed.entity
            if entity.HasField("trip_update")
        ]

        return {
            "feed_timestamp": (
                datetime.fromtimestamp(
                    feed.header.timestamp,
                    ZoneInfo("America/Denver")
                ).isoformat()
                if feed.header.HasField("timestamp")
                else None
            ),
            "total_trips": len(trips),
            "sample_trips": [
                {
                    "route_id": trip.trip.route_id,
                    "trip_id": trip.trip.trip_id,
                    "direction_id": trip.trip.direction_id,
                    "stop_count": len(
                        trip.stop_time_update
                    )
                }
                for trip in trips[:5]
            ]
        }

    except (requests.RequestException, ValueError) as error:
        raise HTTPException(
            status_code=502,
            detail=str(error)
        )
