import datetime
import json
import pathlib

import polyline
import stravalib.client
from ipyleaflet import Map, Polyline, basemaps

TOKEN_FILE = pathlib.Path(__file__).parents[1] / "strava_tokens.json"


def generate_map(
    *,
    center: tuple[float, float],
    zoom: int,
    start_date: datetime.datetime,
    end_date: datetime.datetime,
) -> Map:
    """
    Authenticate with Strava, fetch activities, and return an ipyleaflet map.

    Parameters
    ----------
    center
        The geographical center of the map.
    zoom
        The initial zoom level of the map.
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
        return Map(center=center, zoom=zoom)

    m = Map(
        basemap=basemaps.OpenStreetMap.Mapnik,
        center=center,
        zoom=zoom,
    )
    all_points = []

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

    return m
