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
    # Lat
    y: float
    # Long
    x: float
    # Elevation
    ele: float


point_list = []

for track in gpx.tracks:
    for segment in track.segments:
        for point in segment.points:
            # Kind of just assuming this shit is in order.
            point_list.append(
                (
                    point.time,
                    Point(y=point.latitude, x=point.longitude, ele=point.elevation),
                )
            )

def find_closest_points(image_time_utc: datetime, points: List) -> List[Point]:
    # LOL so inefficient
    start = None
    end = None
    for i, p in enumerate(points):
        if p[0] < image_datetime < points[i + 1][0]:
            next_point = points[i + 1]
            print("point: {} [{}, {}]".format(p[0], p[1]["y"], p[1]["x"]))
            print("image: {}".format(image_time_utc))
            print(
                "point: {} [{}, {}]".format(
                    next_point[0], next_point[1]["y"], next_point[1]["x"]
                )
            )


# find_closest_points(image_time_utc, point_list)