import datetime
import json
import pathlib

import polyline
import stravalib.client
from ipyleaflet import Map, Polyline, basemaps

TOKEN_FILE = pathlib.Path(__file__).parent / "strava_tokens.json"


def generate_map(
    start_date: datetime.datetime,
    end_date: datetime.datetime,
) -> Map:
    """
    Authenticate with Strava, fetch activities, and return an ipyleaflet map.

    Parameters
    ----------
    start_date
        The start date for fetching activities.
    end_date
        The end date for fetching activities.

    Returns
    -------
        An ipyleaflet map with the activity routes plotted.
    """
    try:
        with pathlib.Path.open(TOKEN_FILE) as f:
            token_data = json.load(f)

        client = stravalib.client.Client(
            access_token=token_data["access_token"],
            refresh_token=token_data["refresh_token"],
            token_expires=token_data["expires_at"],
        )
    except FileNotFoundError:
        print("Error: Strava tokens not found. Please run authentication.")
        return Map(center=(51.5, -0.1), zoom=5)

    m = Map(
        basemap=basemaps.OpenStreetMap.Mapnik,
        center=(51.5, -0.1),
        zoom=10,
    )
    all_points = []

    try:
        activities = client.get_activities(after=start_date, before=end_date)
        for activity in activities:
            if activity.map.summary_polyline:
                points = polyline.decode(activity.map.summary_polyline)
                all_points.extend(points)
                line = Polyline(
                    locations=points,
                    color="purple",
                    weight=4,
                    fill=False,
                )
                m.add(line)

        if all_points:
            latitudes = [p[0] for p in all_points]
            longitudes = [p[1] for p in all_points]
            bounds = (
                (min(latitudes), min(longitudes)),
                (max(latitudes), max(longitudes)),
            )
            m.fit_bounds(bounds)

    except Exception as e:
        print(f"Error fetching or plotting activities: {e}")

    return m
