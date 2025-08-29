import datetime
import json
import pathlib
import os

import polyline
import stravalib.client
from ipyleaflet import Map, Polyline, basemaps

STRAVA_ACCESS_TOKEN = os.getenv("STRAVA_ACCESS_TOKEN")
STRAVA_EXPIRES_AT = os.getenv("STRAVA_EXPIRES_AT")
STRAVA_REFRESH_TOKEN = os.getenv("STRAVA_REFRESH_TOKEN")


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
    client = stravalib.client.Client(
        access_token=STRAVA_ACCESS_TOKEN,
        refresh_token=STRAVA_REFRESH_TOKEN,
        token_expires=STRAVA_EXPIRES_AT,
    )

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
