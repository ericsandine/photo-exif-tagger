import datetime
import os
from typing import List, TypedDict
import pytz

import gpxpy
import gpxpy.gpx
from exif import Image

base_directory = os.path.expanduser("~") + "/Pictures/"
current_image = base_directory + "DSC00572.jpg"

with open(current_image, "rb") as image_file:
    exif_image = Image(image_file)
    image_datetime = datetime.datetime.strptime(
        exif_image.datetime_original + " " + exif_image.offset_time,
        "%Y:%m:%d %H:%M:%S %z",
    )
    # Is this right? I hate timezones, I'm pretty sure datetime comparison works anyway
    # without making this UTC, but I don't care to look it up right now.
    image_time_utc = (image_datetime - image_datetime.utcoffset()).replace(
        tzinfo=pytz.UTC
    )

gpx_file = open(base_directory + "bon-tempe-lake-lagunitas.gpx", "r")

gpx = gpxpy.parse(gpx_file)


class Point(TypedDict):
    latitude: float
    longitude: float


point_list = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            # Kind of just assuming this shit is in order.
            point_list.append(
                (
                    point.time,
                    Point(latitude=point.latitude, longitude=point.longitude),
                )
            )


def find_closest_points(image_time_utc: datetime, points: List) -> tuple:
    # LOL so inefficient
    start = None
    end = None
    for i, p in enumerate(points):
        # TODO handle the beginning / end of this list
        if p[0] < image_datetime < points[i + 1][0]:
            next_point = points[i + 1]
            # Earth is flat, screw it
            mid_point_y = (p[1]["latitude"] + next_point[1]["latitude"]) / 2
            mid_point_x = (p[1]["longitude"] + next_point[1]["longitude"]) / 2
    return (mid_point_y, mid_point_x)


print(find_closest_points(image_time_utc, point_list))